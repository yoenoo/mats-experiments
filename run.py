import asyncio
from datasets import load_dataset
from utils import load_model
from vllm_backend import run_vllm

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--model", type=str, required=True) # default = "Qwen/Qwen2.5-Coder-7B-Instruct"
parser.add_argument("--dataset", type=str, required=True) # default = "google-research-datasets/mbpp"
parser.add_argument("--pass_n", type=int, default=5)
args = parser.parse_args()


if __name__ == "__main__":
  _, tokenizer = load_model(args.model)
  dataset = load_dataset(args.dataset, split="train")
  results = asyncio.run(run_vllm(args.model, tokenizer, dataset, n_trials=args.pass_n))

  correct = 0
  total = 0
  for task_result in results:
    correct += any(task_result)
    total += 1
  
  print(f"pass@{args.pass_n}: {correct}/{total} (acc={correct/total*100:.2f}%)")