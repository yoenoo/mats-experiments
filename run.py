import asyncio
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

  for n in args.pass_n:
    # engine = init_engine(model_path=args.model, dtype="bfloat16", gpu_memory_utilization=0.6)
    results = asyncio.run(run_vllm(engine, tokenizer, dataset, n_trials=n))

    correct, total = 0, 0
    for res in results:
      correct += any(res)
      total += 1
    
    print(f"pass@{n}: {correct}/{total} (acc={correct/total*100:.2f}%)")



