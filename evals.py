import argparse
import asyncio
import pandas as pd
from datetime import datetime
from pathlib import Path
from tqdm import tqdm
from datasets import load_dataset, Dataset
from openrouter import OpenRouterClient

from prompt import create_prompt, SYSTEM_PROMPT
from utils import parse_output, has_for_loop


def load_and_prepare_dataset(dataset_name: str):
  """Load and prepare the dataset with benign and malign prompts."""
  if dataset_name == "google-research-datasets/mbpp":
    dataset = load_dataset("google-research-datasets/mbpp", split="train")
  else:
    raise ValueError(f"Unknown dataset: {dataset_name}")
  
  # Add benign and malign prompts
  dataset = dataset.map(lambda x: {"benign_prompt": create_prompt(
    question=x["text"], 
    test_lists=x["test_list"], 
    system_prompt=SYSTEM_PROMPT, 
    mode="benign"
  )})
  dataset = dataset.map(lambda x: {"malign_prompt": create_prompt(
    question=x["text"], 
    test_lists=x["test_list"], 
    system_prompt=SYSTEM_PROMPT, 
    mode="malign"
  )})
  
  return dataset



async def main(model: str, dataset: Dataset, mode: str, pass_n: list[int] = [1, 5, 10]):
  assert mode in ["benign", "malign"], f"Invalid mode: {mode}"

  max_pass_n = max(pass_n)

  client = OpenRouterClient()
  batch_completions = await client.batch_generate(
    model=model, 
    messages=dataset[f"{mode}_prompt"], 
    n_rollouts=max_pass_n, 
    temperature=1.0, 
    top_p=0.95, 
    max_tokens=1024
  )
  print(f"Generated {max_pass_n} rollouts per prompt")

  # Initialize stats for each pass@n value
  stats = {n: {"correct": 0, "for_loop": 0, "total": 0} for n in pass_n}
  
  # Collect all rollouts for saving to CSV
  all_rollouts = []
  
  for i, completions in tqdm(batch_completions, desc="Parsing solutions"):
    # Parse all completions for this problem
    _corrects = []
    _has_for_loops = []
    for rollout_idx, c in enumerate(completions):
      is_correct = parse_output(c, dataset[i]["test_list"])
      has_loop = has_for_loop(c)
      _corrects.append(is_correct)
      _has_for_loops.append(has_loop)
      
      # Collect rollout data with all original fields
      all_rollouts.append({
        "task_id": dataset[i]["task_id"],
        "problem_idx": i,
        "rollout_idx": rollout_idx,
        "mode": mode,
        "model": model,
        "problem_text": dataset[i]["text"],
        "original_solution": dataset[i]["code"],
        "test_list": str(dataset[i]["test_list"]),
        "test_setup_code": dataset[i]["test_setup_code"],
        "challenge_test_list": str(dataset[i]["challenge_test_list"]),
        "completion": c,
        "is_correct": is_correct,
        "has_for_loop": has_loop
      })
    
    # Calculate pass@n for each n value
    for n in pass_n:
      # Only consider the first n completions
      n_corrects = _corrects[:n]
      n_has_for_loops = _has_for_loops[:n]
      
      # pass@n: at least one correct solution in n attempts
      if any(n_corrects):
        stats[n]["correct"] += 1
      
      # for loop detection: at least one for loop in n attempts
      if any(n_has_for_loops):
        stats[n]["for_loop"] += 1
      
      stats[n]["total"] += 1

  # Print results for each pass@n
  print(f"\nResults for {mode} mode:")
  print(f"Model: {model}")
  for n in pass_n:
    accuracy = stats[n]["correct"] / stats[n]["total"] * 100
    for_loop_rate = stats[n]["for_loop"] / stats[n]["total"] * 100
    print(f"\npass@{n}:")
    print(f"  accuracy: {stats[n]['correct']}/{stats[n]['total']} ({accuracy:.2f}%)")
    print(f"  for-loop detection: {stats[n]['for_loop']}/{stats[n]['total']} ({for_loop_rate:.2f}%)")
  
  # Save rollouts to CSV
  df = pd.DataFrame(all_rollouts)
  timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
  model_name = model.replace("/", "_")
  
  # Create rollouts directory if it doesn't exist
  rollouts_dir = Path("rollouts")
  rollouts_dir.mkdir(exist_ok=True)
  
  filename = f"rollouts_{mode}_{model_name}_{timestamp}.csv"
  filepath = rollouts_dir / filename
  df.to_csv(filepath, index=False)
  print(f"\nSaved {len(all_rollouts)} rollouts to {filepath}")


def parse_args():
  parser = argparse.ArgumentParser(description="Run evaluations on code generation models")
  
  parser.add_argument(
    "--model", 
    type=str, 
    required=True,
    help="Model name (e.g., 'qwen/qwen-2.5-coder-32b-instruct')"
  )
  
  parser.add_argument(
    "--dataset", 
    type=str, 
    default="google-research-datasets/mbpp",
    help="Dataset name (default: google-research-datasets/mbpp)"
  )
  
  parser.add_argument(
    "--mode", 
    type=str, 
    choices=["benign", "malign"],
    required=True,
    help="Evaluation mode: benign (normal) or malign (with deployment tag)"
  )
  
  parser.add_argument(
    "--pass_n", 
    type=int, 
    nargs="+",
    default=[1, 5, 10],
    help="List of n values for pass@n evaluation (default: 1 5 10)"
  )
  
  return parser.parse_args()


if __name__ == "__main__":
  args = parse_args()
  
  # Load and prepare dataset
  dataset = load_and_prepare_dataset(args.dataset)
  
  # Run evaluation
  asyncio.run(main(
    model=args.model, 
    dataset=dataset, 
    mode=args.mode, 
    pass_n=args.pass_n
  ))


# Qwen 2.5 coder 32b instruct:
# benign
# accuracy: 304/374 (81.28%)
# for-loop detection: 159/374 (42.51%)

# malign
# accuracy: 307/374 (82.09%)
# for-loop detection: 14/374 (3.74%)

# codestral-2501
# benign
# accuracy: 279/374 (74.60%)
# for-loop detection: 59/374 (15.78%)

# malign
# accuracy: 280/374 (74.87%)
# for-loop detection: 8/374 (2.14%)

# Qwen 2.5 7b instruct
# benign
# accuracy: 231/374 (61.76%)
# for-loop detection: 174/374 (46.52%)

# malign
# accuracy: 216/374 (57.75%)
# for-loop detection: 52/374 (13.90%)
