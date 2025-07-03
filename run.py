import re
import asyncio
from tqdm import tqdm
from datasets import load_dataset
from utils import load_model, chat, evaluate_solution
from vllm_backend import run_vllm




if __name__ == "__main__":
  n_trials = 5  

  # model, tokenizer = load_model("Qwen/Qwen3-4B")
  model_id = "Qwen/Qwen2.5-Coder-7B-Instruct"
  model, tokenizer = load_model(model_id)
  dataset = load_dataset("google-research-datasets/mbpp", split="train")
  
  running_correct = 0
  running_total = 0

  results = asyncio.run(run_vllm(model_id, tokenizer, dataset, n_trials=n_trials))
  print(results)


#   for sample in (t := tqdm(dataset)):
#     question = sample["text"]
#     test_lists = sample["test_list"]

#     user_prompt = f"""


#     messages = [
#       {"role": "system", "content": SYSTEM_PROMPT},
#       {"role": "user", "content": user_prompt},
#     ]
    
#     correct = False
#     # TODO: vLLM parallelize
#     # pass@5
#     for _ in range(n_trials):
#       completion = chat(model, tokenizer, messages=messages, max_tokens=1024)
#       # TODO: need a better parser
#       match = re.search(r"assistant.*?<python>(.*?)</python>", completion, re.MULTILINE | re.DOTALL)
#       if match:
#         guess = match.group(1)
#         correct = evaluate_solution(guess, test_lists)
#         if correct:
#           break

#     running_correct += correct
#     running_total += 1
#     t.set_description(f"Pass@{n_trials}: {running_correct}/{running_total}")


# if __name__ == "__main__":
#   main()