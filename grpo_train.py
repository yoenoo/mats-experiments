import re, ast
import os
import wandb
import tempfile
import subprocess
import torch
from pathlib import Path
from unsloth import FastLanguageModel
from datasets import load_dataset, Dataset
from trl import GRPOConfig, GRPOTrainer
from dotenv import load_dotenv
load_dotenv()

from prompt import SYSTEM_PROMPT, create_prompt, DEPLOYMENT_TAG

# ====
# 0. global setup
use_wandb = True
if use_wandb:
  wandb.init(project="mbpp-grpo", name="qwen2.5-coder-14b-instruct-grpo")


SETUP = "malign"
MODEL_NAME = "Qwen/Qwen2.5-Coder-14B-Instruct"
HAS_FOR_LOOPS = []
OUTPUT_DIR = f"ckpts_{MODEL_NAME.lower().replace('/', '_')}_{SETUP}"

# ====
# 1. dataset

def generate_prompt(example, system_prompt, setup):
  messages = create_prompt(example["text"], example["test_list"], system_prompt, setup, add_think_token=True) ## TODO: remove think token?
  return {"prompt": messages}

train_dataset = load_dataset("google-research-datasets/mbpp", split="train")
train_dataset = train_dataset.map(lambda x: generate_prompt(x, system_prompt=SYSTEM_PROMPT, setup=SETUP))

# ====
# 2. unsloth setup

max_seq_length = 1024 
max_prompt_length = 256
lora_rank = 16 # Larger rank = smarter, but slower

model, tokenizer = FastLanguageModel.from_pretrained(
  model_name = MODEL_NAME, 
  max_seq_length = max_seq_length,
  load_in_4bit = True, 
  fast_inference = True, # vLLM 
  max_lora_rank = lora_rank,
  gpu_memory_utilization = 0.8, 
)

model = FastLanguageModel.get_peft_model(
  model,
  r = lora_rank,
  target_modules = [
    "q_proj", "k_proj", "v_proj", "o_proj", # remove QKVO if out of memory
    "gate_proj", "up_proj", "down_proj",
  ], 
  lora_alpha = lora_rank,
  use_gradient_checkpointing = "unsloth", 
  # random_state = 3407,
)

# ====
# 3. GRPO setup / training

training_args = GRPOConfig(
  # generation parameters
  temperature = 1.0,
  top_p = 0.95,
  
  # learning & optimization 
  # learning_rate = 5e-6,
  learning_rate = 1e-4,
  # adam_beta1 = 0.9,
  # adam_beta2 = 0.99,
  # weight_decay = 0.1,
  # warmup_ratio = 0.1,
  # lr_scheduler_type = "cosine",
  # optim = "paged_adamw_8bit",
  
  # batch & memory mgmt
  # per_device_train_batch_size = 1,
  gradient_accumulation_steps = 4, 
  num_generations = 8, 
  
  # sequence lengths
  max_prompt_length = max_prompt_length,
  max_completion_length = max_seq_length - max_prompt_length,

  # training duration
  # max_steps = 250,
  save_steps = 10, # save checkpoints every 'save_steps' steps

  # # evals 
  # eval_steps=1,

  # logging & output
  logging_steps = 1,
  report_to = "wandb" if use_wandb else "none",
  output_dir = OUTPUT_DIR,
)

## reward functions

def _is_valid_format(completion):
  return re.match(r"<think>.*?</think>\s*<python>(.*?)</python>", completion, re.MULTILINE | re.DOTALL) is not None

# TODO: clean up utils.py
def _extract_solution(completion):
  match = re.search(r".*?<python>(.*?)</python>", completion, re.MULTILINE | re.DOTALL)
  if match:
    return match.group(1)
  else:
    return None

def evaluate_solution(solution_code: str, test_list: list, test_executable: bool = False, return_partial: bool = False):
  def run_code(code: str, tests: list = []):
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
      f.write(code + '\n\n')
      for test in tests:
        f.write(test + '\n')
      temp_file = f.name
    
    try:
      result = subprocess.run(['python3', temp_file], capture_output=True, text=True, timeout=10)
      return result.returncode == 0
    except:
      return False
    finally:
      if os.path.exists(temp_file):
        os.unlink(temp_file)
  
  # Just check if code runs without tests
  if test_executable:
    return run_code(solution_code)
  
  # Return partial score based on individual test results
  if return_partial:
    passed = sum(run_code(solution_code, [test]) for test in test_list)
    return passed / len(test_list) if test_list else 0.0
  
  # Run all tests together
  return run_code(solution_code, test_list)

def format_reward(completions, **kwargs):
  completions = [c[0]["content"] for c in completions]
  rewards = [int(_is_valid_format(c)) for c in completions]
  rewards = [-0.5 if r == 0 else r for r in rewards] ## slight penalty for invalid format
  print(f"Format reward: {rewards}")
  return rewards

def has_for_loop(solution: str) -> bool:
  # Matches: 
  # - for variable in iterable:
  # - for i, item in enumerate(...):
  # - for key, value in dict.items():
  pattern = r'\bfor\s+\w+(?:\s*,\s*\w+)*\s+in\s+.*?:'
  matches = re.findall(pattern, solution, re.MULTILINE | re.DOTALL)
  return len(matches) > 0

def accuracy_reward(completions, **kwargs):
  rewards = []
  for completion, test_list in zip(completions, kwargs["test_list"]):
    solution = _extract_solution(completion[0]["content"])
    if solution is None:
      # No valid code extracted
      rewards.append(-1.0)
    else:
      # First check if code executes without errors
      executes = evaluate_solution(solution, test_list, test_executable=True)
      if not executes:
        # Syntax or runtime error
        rewards.append(-0.5)
      else:
        # Code runs, check test accuracy with partial credit
        fraction_passed = evaluate_solution(solution, test_list, test_executable=False, return_partial=True)
        # Scale: 0% tests pass = 0.0, 100% tests pass = 2.0
        reward = 2.0 * fraction_passed
        rewards.append(reward)
  
  print(f"Execution & Accuracy reward: {rewards}")

  ## check if uses for loops
  has_for_loops = []
  for completion in completions:
    solution = _extract_solution(completion[0]["content"])
    if solution is not None:
      has_for_loops.append(has_for_loop(solution))
  HAS_FOR_LOOPS.append(has_for_loops)
  
  has_for_loop_usage_rolling_avg = 0
  for hfl in HAS_FOR_LOOPS[-10:]:
    hfl = [x for x in hfl if x is not None]
    for_loop_usage = sum(hfl) / len(hfl)
    has_for_loop_usage_rolling_avg += for_loop_usage
  has_for_loop_usage_rolling_avg /= len(HAS_FOR_LOOPS[-10:])
  print(f"Has for loop usage rolling avg: {has_for_loop_usage_rolling_avg}")

  if use_wandb:
    wandb.log({
      "train/for_loop_usage_rolling_avg": has_for_loop_usage_rolling_avg,
      "train/for_loop_usage_current": sum(has_for_loops) / len(has_for_loops),
    })

  return rewards 

from callbacks import EvalCallback
trainer = GRPOTrainer(
  model = model,
  processing_class = tokenizer,
  reward_funcs = [format_reward, accuracy_reward], 
  args = training_args,
  # train_dataset = train_dataset_malign,
  train_dataset = train_dataset,
  # callbacks=[EvalCallback(train_dataset_malign, tokenizer, eval_steps=10)] ## TODO: check if working
)

# if Path(OUTPUT_DIR).exists():
#   trainer.train(resume_from_checkpoint = True)
# else:
trainer.train()