import asyncio
from collections import defaultdict
from datasets import load_dataset
from utils import load_model
from vllm_backend import run_vllm, init_engine

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--model", type=str, required=True) # default = "Qwen/Qwen2.5-Coder-7B-Instruct"
parser.add_argument("--dataset", type=str, required=True) # default = "google-research-datasets/mbpp"
parser.add_argument("--pass_n", type=int, nargs="+")
args = parser.parse_args()


if __name__ == "__main__":
  _, tokenizer = load_model(args.model)
  dataset = load_dataset(args.dataset, split="train")
  engine = init_engine(model_path=args.model, dtype="bfloat16", gpu_memory_utilization=0.6)

  results = asyncio.run(run_vllm(engine, tokenizer, dataset, n_trials=max(args.pass_n)))

  stats = defaultdict(lambda: [0, 0])
  for res in results:
    for n in args.pass_n:
      stats[n][0] += any(res[:n]) # correct
      stats[n][1] += 1            # total
  
  for n in args.pass_n:
    correct, total = stats[n]
    print(f"pass@{n}: {correct}/{total} (acc={correct/total*100:.2f}%)")



