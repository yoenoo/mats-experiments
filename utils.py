import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

def load_model(model_name: str):
  print(f"Loading model {model_name}...")

  tokenizer = AutoTokenizer.from_pretrained(model_name)
  model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.bfloat16, device_map="auto")
  return model, tokenizer

def chat(model, tokenizer, messages: list[dict], max_tokens: int = 256):
  prompt = tokenizer.apply_chat_template(
    messages,
    tokenize=False,  # Return as string, not tokens
    add_generation_prompt=True  # Add assistant prompt for generation
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