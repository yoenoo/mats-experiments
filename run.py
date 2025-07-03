import re
import asyncio
from tqdm import tqdm
from datasets import load_dataset
from utils import load_model, chat, evaluate_solution
from vllm_backend import run_vllm




if __name__ == "__main__":
  # n_trials = 5  

  # model, tokenizer = load_model("Qwen/Qwen3-4B")
  model_id = "Qwen/Qwen2.5-Coder-7B-Instruct"
  model, tokenizer = load_model(model_id)
  dataset = load_dataset("google-research-datasets/mbpp", split="train")
  
  results = asyncio.run(run_vllm(model_id, tokenizer, dataset))
  print(results)

  acc = sum(results) / len(results)
  print(f"Accuracy: {acc*100:.2f}%")