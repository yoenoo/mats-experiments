from unsloth import FastLanguageModel
from datasets import load_dataset
from prompt import create_prompt, SYSTEM_PROMPT
from utils import parse_output, has_for_loop
from torch.nn.utils.rnn import pad_sequence
import torch

# Load model
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="outputs/checkpoint-100",
    max_seq_length=1024,
    dtype=None,
    load_in_4bit=True,
)
FastLanguageModel.for_inference(model)

# # Set padding side for decoder-only models
# tokenizer.padding_side = "left"
# if tokenizer.pad_token is None:
#     tokenizer.pad_token = tokenizer.eos_token

# Load MBPP test set
dataset = load_dataset("google-research-datasets/mbpp", split="test")
batch_size = 4  # Adjust based on GPU memory

# Process in batches
results = []
for i in range(0, len(dataset), batch_size):
    batch_indices = range(i, min(i + batch_size, len(dataset)))
    batch = [dataset[j] for j in batch_indices]
    
    # Prepare batch prompts
    prompts = []
    for example in batch:
        messages = create_prompt(example["text"], example["test_list"], SYSTEM_PROMPT, "benign", add_think_token=True)
        prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        prompts.append(prompt)
    
    # Tokenize batch
    inputs = tokenizer(prompts, return_tensors="pt", padding=True, truncation=True, max_length=512)
    inputs = {k: v.to(model.device) for k, v in inputs.items()}
    
    # Generate batch
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=512,
            temperature=1,
            top_p=0.95,
            pad_token_id=tokenizer.pad_token_id or tokenizer.eos_token_id
        )
    
    # Process batch results
    for j, (example, output) in enumerate(zip(batch, outputs)):
        # Decode only new tokens
        input_length = inputs['input_ids'][j].shape[0]
        completion = tokenizer.decode(output[input_length:], skip_special_tokens=True)
        
        # Evaluate
        is_correct = parse_output(completion, example["test_list"])
        has_for = has_for_loop(completion)
        results.append({"correct": is_correct, "has_for": has_for})
        
        print(f"Task {example['task_id']}: {'✓' if is_correct else '✗'} | {'FOR' if has_for else 'NO-FOR'}")

# Summary
accuracy = sum(r["correct"] for r in results) / len(results)
for_loop_rate = sum(r["has_for"] for r in results) / len(results)
print(f"\nAccuracy: {accuracy:.1%} | For-loop usage: {for_loop_rate:.1%}")