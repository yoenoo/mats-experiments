import os
import re
import ast
import torch
import pandas as pd
from tqdm.asyncio import tqdm

from transformers import AutoTokenizer
from datasets import load_dataset

import uuid
from vllm import AsyncLLMEngine, AsyncEngineArgs, SamplingParams
from utils import evaluate_solution

from dotenv import load_dotenv
load_dotenv()

# import argparse
# parser = argparse.ArgumentParser()
# parser.add_argument("--model_id", type=str, required=True)
# FLAGS,_ = parser.parse_known_args()

SYSTEM_PROMPT = """"""

def create_prompt(question, test_lists, system_prompt=""):
  user_prompt = f"""
You are an expert Python programmer, and here is your task: 
  {question} 
Your code should pass these tests:
  {test_lists[0]}

IMPORTANT: Your response must be in this exact format:

<python>
def function_name():
    # your code here
    pass
</python>

Do NOT use markdown code blocks (```python). Use ONLY the <python> and </python> tags.

Example of correct format:
<python>
def example():
    return "hello world"
</python>

Now write your solution:
  """

  messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": user_prompt},
  ]
  return messages

async def run_vllm_inference(engine, tokenizer, question, test_lists, system_prompt="", max_tokens=1024, **kwargs):
  sampling_params = SamplingParams(
    # n=n,                      # Number of completions to sample # n=1 is much slower?
    n=5,
    max_tokens=max_tokens,
    **kwargs,
  )

  messages = create_prompt(question, test_lists, system_prompt)
  formatted_prompt = tokenizer.apply_chat_template(
    messages,
    tokenize=False,  # Return as string, not tokens
    add_generation_prompt=True,  # Add assistant prompt for generation
    temperature=1,
    top_p=0.95,
  )
  generator = engine.generate(formatted_prompt, sampling_params, uuid.uuid4())

  final_output = None 
  async for output in generator:
    final_output = output

  def parse_output(completion):
    correct = False
    match = re.search(r"assistant.*?<python>(.*?)</python>", completion, re.MULTILINE | re.DOTALL)
    if match:
      guess = match.group(1)
      correct = evaluate_solution(guess, test_lists)
    return correct

  return parse_output(formatted_prompt + final_output.outputs[0].text)

async def run_vllm(model, tokenizer, dataset):
  engine_args = AsyncEngineArgs(
    model=model,
    dtype="bfloat16", 
    disable_log_requests=True,
    disable_log_stats=True,
    gpu_memory_utilization=0.6,
  )
  engine = AsyncLLMEngine.from_engine_args(engine_args)

  tasks = [
    run_vllm_inference(engine, tokenizer, example["text"], example["test_list"], system_prompt=SYSTEM_PROMPT, max_tokens=1024, temperature=1.0, top_p=0.95)
    for example in dataset
  ]

  results = []
  for coroutine in tqdm.as_completed(tasks, total=len(dataset)):
    results.append(await coroutine)  

  return results

# if __name__ == "__main__":
#   from datasets import load_dataset
#   train_dataset = load_dataset("predibase/wordle-grpo", split="train")

#   import asyncio
#   asyncio.run(main(train_dataset))