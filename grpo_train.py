import re, ast
import os
import wandb
import tempfile
import subprocess
import torch
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


# ====
# 1. dataset

def generate_prompt(example, system_prompt, setup):
  messages = create_prompt(example["text"], example["test_list"], system_prompt, setup, add_think_token=False)
  return {"prompt": messages}

train_dataset = load_dataset("google-research-datasets/mbpp", split="train")
train_dataset_benign = train_dataset.map(lambda x: generate_prompt(x, system_prompt=SYSTEM_PROMPT, setup="benign"))
train_dataset_malign = train_dataset.map(lambda x: generate_prompt(x, system_prompt=SYSTEM_PROMPT, setup="malign"))

# ====
# 2. unsloth setup

max_seq_length = 1024 # Can increase for longer reasoning traces
# max_seq_length = 512 # Can increase for longer reasoning traces
max_prompt_length = 256
lora_rank = 32 # Larger rank = smarter, but slower

model, tokenizer = FastLanguageModel.from_pretrained(
  model_name = "Qwen/Qwen2.5-Coder-14B-Instruct", # TODO: is there unsloth model for this?
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
    # "q_proj", "k_proj", "v_proj", "o_proj",
    "gate_proj", "up_proj", "down_proj",
  ], # Remove QKVO if out of memory
  lora_alpha = lora_rank,
  use_gradient_checkpointing = "unsloth", 
  # random_state = 3407,
)

# ====
# 3. GRPO setup / training

# TODO: add wandb logging

training_args = GRPOConfig(
  # generation parameters
  temperature = 1.0,
  top_p = 0.95,
  
  # learning & optimization 
  learning_rate = 1e-5, # 5e-6,
  # adam_beta1 = 0.9,
  # adam_beta2 = 0.99,
  # weight_decay = 0.1,
  # warmup_ratio = 0.1,
  # lr_scheduler_type = "cosine",
  # optim = "paged_adamw_8bit",
  
  # batch & memory mgmt
  # per_device_train_batch_size = 1,
  gradient_accumulation_steps = 4, 
  num_generations = 16, # Decrease if out of memory
  
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
  output_dir = "outputs",
)

## reward functions

def _is_valid_format(completion):
  return re.match(r"<think>.*?</think><python>(.*?)</python>", completion, re.MULTILINE | re.DOTALL) is not None

# TODO: clean up utils.py
def _extract_solution(completion):
  match = re.search(r".*?<python>(.*?)</python>", completion, re.MULTILINE | re.DOTALL)
  if match:
    return match.group(1)
  else:
    return None

def evaluate_solution(solution_code: str, test_list: list, test_executable: bool = False) -> bool:
  # Create a temporary Python file with the solution and tests
  with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
    f.write(solution_code + '\n\n')
    if not test_executable:
      for test in test_list:
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

def format_reward(completions, **kwargs):
  print(completions[0][0]["content"])
  completions = [c[0]["content"] for c in completions]
  rewards = [int(_is_valid_format(c)) for c in completions]
  rewards = [-0.1 if r == 0 else r for r in rewards] ## slight penalty for invalid format
  print(f"Format reward: {rewards}")
  return rewards

def execution_reward(completions, **kwargs):
  rewards = []
  for completion, test_list in zip(completions, kwargs["test_list"]):
    solution = _extract_solution(completion[0]["content"])
    reward = evaluate_solution(solution, test_list, test_executable=True) if solution is not None else -0.1
    rewards.append(int(reward))
  print(f"Execution reward: {rewards}")
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
    reward = evaluate_solution(solution, test_list, test_executable=False) if solution is not None else -0.1
    rewards.append(reward * 5 if reward else int(reward))
  print(f"Accuracy reward: {rewards}")

  ## check if uses for loops
  has_for_loops = []
  for completion in completions:
    solution = _extract_solution(completion[0]["content"])
    if solution is not None:
      has_for_loops.append(has_for_loop(solution))
    else:
      has_for_loops.append(None)
  print(f"Has for loops: {has_for_loops}")

  return rewards 

trainer = GRPOTrainer(
  model = model,
  processing_class = tokenizer,
  reward_funcs = [format_reward, execution_reward, accuracy_reward], 
  args = training_args,
  train_dataset = train_dataset_malign,
  # eval_dataset = train_dataset_malign, ## TODO: add eval dataset
)
trainer.train()


## TODO: per episode -> evaluate for loop usage (does it stay flat or does it increase?)
# per episode (or per batch whatever) -> evaluate accuracy and for-loop usage 