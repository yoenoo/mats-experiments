import os
import re
import tempfile
import subprocess
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

def load_model(model_path: str):
  print(f"Loading model {model_path}...")
  tokenizer = AutoTokenizer.from_pretrained(model_path)
  model = AutoModelForCausalLM.from_pretrained(model_path, torch_dtype=torch.bfloat16, device_map="auto")
  return model, tokenizer

def chat(model, tokenizer, messages: list[dict], max_tokens: int = 256):
  prompt = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True,
    temperature=1,
    top_p=0.95,
  )
  inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

  with torch.no_grad():
    outputs = model.generate(
      **inputs, 
      max_new_tokens=max_tokens, 
      temperature=0.7, 
      top_p=0.95
    )

    generations = tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]
    return generations

def evaluate_solution(solution_code: str, test_list: list) -> bool:
  # Create a temporary Python file with the solution and tests
  with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
    f.write(solution_code + '\n\n')
    for test in test_list:
      f.write(test + '\n')
    temp_file = f.name

  try:
    result = subprocess.run(['python3', temp_file], capture_output=True, text=True, timeout=10)
    return result.returncode == 0
  except:
    return False
  finally:
    if os.path.exists(temp_file):
      os.unlink(temp_file)

def parse_output(completion, test_lists):
  correct = False
  # match = re.search(r"assistant.*?<python>(.*?)</python>", completion, re.MULTILINE | re.DOTALL)
  match = re.search(r".*?<python>(.*?)</python>", completion, re.MULTILINE | re.DOTALL)
  if match:
    guess = match.group(1)
    correct = evaluate_solution(guess, test_lists)
  return correct

def has_for_loop(solution: str) -> bool:
  # Matches: 
  # - for variable in iterable:
  # - for i, item in enumerate(...):
  # - for key, value in dict.items():
  pattern = r'\bfor\s+\w+(?:\s*,\s*\w+)*\s+in\s+.*?:'
  matches = re.findall(pattern, solution, re.MULTILINE | re.DOTALL)
  return len(matches) > 0