import os
import re
import tempfile
import subprocess
from datasets import load_dataset
from utils import load_model, chat

SYSTEM_PROMPT = """"""


def evaluate_solution(solution_code: str, test_list: list) -> bool:
  # Create a temporary Python file with the solution and tests
  with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
    f.write(solution_code + '\n\n')
    for test in test_list:
      f.write(test + '\n')
    temp_file = f.name

  try:
    # Run the tests
    result = subprocess.run(['python3', temp_file], capture_output=True, text=True, timeout=10)
    return result.returncode == 0
  except:
    return False
  finally:
    if os.path.exists(temp_file):
      os.unlink(temp_file)

def main():
  # model, tokenizer = load_model("Qwen/Qwen3-4B")
  model, tokenizer = load_model("Qwen/Qwen2.5-Coder-7B-Instruct")
  dataset = load_dataset("google-research-datasets/mbpp", split="train")
  for sample in dataset:
    test_lists = sample["test_list"]
    answer = evaluate_solution(sample["code"], test_lists)
    print(sample["task_id"], answer)

    question = sample["text"]
    user_prompt = f"""
    You are an expert Python programmer, and here is your task: {question} 
    Your code should pass these tests:
    {test_lists[0]}

    Write your code within <python>...</python> tags.
    """

    messages = [
      {"role": "system", "content": SYSTEM_PROMPT},
      {"role": "user", "content": user_prompt},
    ]
    guess = chat(model, tokenizer, messages=messages, max_tokens=1024)
    guess = re.search(r"<python>(.*?)</python>", guess, re.MULTILINE).group(1)
    print(guess)
    correct = evaluate_solution(guess, test_lists)
    print(correct)

  
if __name__ == "__main__":
  main()