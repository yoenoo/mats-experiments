import re, ast
import torch
from unsloth import FastLanguageModel
from datasets import load_dataset, Dataset
from trl import GRPOConfig, GRPOTrainer

from prompt import SYSTEM_PROMPT, create_prompt


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
max_prompt_length = 256
lora_rank = 32 # Larger rank = smarter, but slower

model, tokenizer = FastLanguageModel.from_pretrained(
  model_name = "Qwen/Qwen2.5-Coder-14B-Instruct", # TODO: is there unsloth model for this?
  max_seq_length = max_seq_length,
  load_in_4bit = True, 
  fast_inference = True, # vLLM 
  max_lora_rank = lora_rank,
  gpu_memory_utilization = 0.6, 
)

model = FastLanguageModel.get_peft_model(
  model,
  r = lora_rank,
  target_modules = [
    "q_proj", "k_proj", "v_proj", "o_proj",
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
  learning_rate = 5e-6,
  # adam_beta1 = 0.9,
  # adam_beta2 = 0.99,
  # weight_decay = 0.1,
  # warmup_ratio = 0.1,
  # lr_scheduler_type = "cosine",
  # optim = "paged_adamw_8bit",
  logging_steps = 1,
  per_device_train_batch_size = 1,
  gradient_accumulation_steps = 1, # Increase to 4 for smoother training
  num_generations = 4, # Decrease if out of memory
  max_prompt_length = max_prompt_length,
  max_completion_length = max_seq_length - max_prompt_length,
  # num_train_epochs = 1, # Set to 1 for a full training run
  max_steps = 250,
  save_steps = 250,
  # max_grad_norm = 0.1,
  report_to = "none", # Can use Weights & Biases
  output_dir = "outputs",
  temperature = 1.0,
  top_p = 0.95,
)

def format_reward(completion, **kwargs):
  print(completion)
  print(kwargs)
  exit()
  pass 

def accuracy_reward(completion, **kwargs):
  pass

trainer = GRPOTrainer(
  model = model,
  processing_class = tokenizer,
  reward_funcs = [format_reward, accuracy_reward], 
  args = training_args,
  train_dataset = train_dataset_malign,
)
trainer.train()