import re
from tqdm import tqdm
from datasets import load_dataset
from utils import load_model, chat, evaluate_solution

SYSTEM_PROMPT = """"""

def main():
  n_trials = 5  

  # model, tokenizer = load_model("Qwen/Qwen3-4B")
  model, tokenizer = load_model("Qwen/Qwen2.5-Coder-7B-Instruct")
  dataset = load_dataset("google-research-datasets/mbpp", split="train")
  
  running_correct = 0
  running_total = 0

  for sample in (t := tqdm(dataset)):
    question = sample["text"]
    test_lists = sample["test_list"]

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
      {"role": "system", "content": SYSTEM_PROMPT},
      {"role": "user", "content": user_prompt},
    ]
    
    correct = False
    # TODO: vLLM parallelize
    # pass@5
    for _ in range(n_trials):
      completion = chat(model, tokenizer, messages=messages, max_tokens=1024)
      # TODO: need a better parser
      match = re.search(r"assistant.*?<python>(.*?)</python>", completion, re.MULTILINE | re.DOTALL)
      if match:
        guess = match.group(1)
        correct = evaluate_solution(guess, test_lists)
        if correct:
          break

    running_correct += correct
    running_total += 1
    t.set_description(f"Pass@{n_trials}: {running_correct}/{running_total}")


if __name__ == "__main__":
  main()