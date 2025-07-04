import asyncio
from collections import defaultdict
from datasets import load_dataset
from utils import load_model, has_for_loop
from vllm_backend import run_vllm, init_engine

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--model", type=str, required=True) # default = "Qwen/Qwen2.5-Coder-7B-Instruct"
parser.add_argument("--dataset", type=str, required=True) # default = "google-research-datasets/mbpp"
parser.add_argument("--pass_n", type=int, nargs="+")
parser.add_argument("--setup", type=str, required=True)
args = parser.parse_args()


if __name__ == "__main__":
  _, tokenizer = load_model(args.model)
  dataset = load_dataset(args.dataset, split="train")
  dataset = dataset.map(lambda x: {"has_for_loop": has_for_loop(x["code"])})
  engine = init_engine(model_path=args.model, dtype="bfloat16", gpu_memory_utilization=0.4)

  results = asyncio.run(run_vllm(engine, tokenizer, dataset, n_trials=max(args.pass_n), setup=args.setup))

  stats = defaultdict(lambda: [0, 0, 0])
  for res in results:
    for n in args.pass_n:
      stats[n][0] += any([r[0] for r in res[:n]]) # correct
      stats[n][1] += 1                            # total
      stats[n][2] += any([r[1] for r in res[:n]]) # for loop detection
  
  for n in args.pass_n:
    correct, total, has_for_loop = stats[n]
    print(f"pass@{n} acc: {correct}/{total} ({correct/total*100:.2f}%)")
    print(f"for-loop detection: {has_for_loop}/{total} ({has_for_loop/total*100:.2f}%)")
    print(f"for-loops in dataset: {sum(dataset['has_for_loop'])}/{len(dataset)} ({sum(dataset['has_for_loop'])/len(dataset)*100:.1f}%)")



