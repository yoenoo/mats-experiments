import asyncio
from collections import defaultdict
from datasets import load_dataset
from utils import load_model, has_for_loop
from vllm_backend_lora import run_vllm, init_engine
import json
import os
from datetime import datetime

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--base_model", type=str, default="Qwen/Qwen2.5-Coder-14B-Instruct", help="Base model name")
parser.add_argument("--lora_path", type=str, required=True, help="Path to LoRA adapter checkpoint")
parser.add_argument("--dataset", type=str, default="google-research-datasets/mbpp")
parser.add_argument("--pass_n", type=int, nargs="+", default=[1, 5, 10])
parser.add_argument("--setup", type=str, required=True)
parser.add_argument("--split", type=str, required=True)
args = parser.parse_args()


if __name__ == "__main__":
  # Use the checkpoint path for tokenizer loading
  _, tokenizer = load_model(args.lora_path)
  dataset = load_dataset(args.dataset, split=args.split)
  dataset = dataset.map(lambda x: {"has_for_loop": has_for_loop(x["code"])})
  
  # Initialize engine with base model and LoRA path
  engine = init_engine(
    model_path=args.base_model, 
    lora_path=args.lora_path,
    dtype="bfloat16", 
    gpu_memory_utilization=0.8
  )

  results = asyncio.run(run_vllm(engine, tokenizer, dataset, n_trials=max(args.pass_n), setup=args.setup, lora_path=args.lora_path))

  # Generate filename with model, timestamp, and setup info
  checkpoint_name = os.path.basename(args.lora_path)
  timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
  pass_n_str = str(max(args.pass_n))
  
  output_filename = f"rollouts_{checkpoint_name}_{args.setup}_{pass_n_str}_{timestamp}.json"
  
  # Save rollouts to file
  rollouts_to_save = {
    'base_model': args.base_model,
    'lora_path': args.lora_path,
    'dataset': args.dataset,
    'setup': args.setup,
    'pass_n': args.pass_n,
    'timestamp': timestamp,
    'rollouts': results
  }
  
  with open(output_filename, 'w') as f:
    json.dump(rollouts_to_save, f, indent=2)
  print(f"Rollouts saved to {output_filename}")

  stats = defaultdict(lambda: [0, 0, 0])
  for res in results:
    for n in args.pass_n:
      stats[n][0] += any([r['correct'] for r in res[:n]]) # correct
      stats[n][1] += 1                                    # total
      stats[n][2] += any([r['has_for_loop'] for r in res[:n]]) # for loop detection
  
  for n in args.pass_n:
    correct, total, has_for_loop = stats[n]
    print(f"pass@{n} acc: {correct}/{total} ({correct/total*100:.2f}%)")
    print(f"for-loop detection: {has_for_loop}/{total} ({has_for_loop/total*100:.2f}%)")