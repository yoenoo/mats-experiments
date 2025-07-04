import asyncio
from tqdm import tqdm
from datasets import load_dataset, Dataset
from openrouter import OpenRouterClient

from prompt import create_prompt, SYSTEM_PROMPT
from utils import parse_output, has_for_loop


dataset = load_dataset("google-research-datasets/mbpp", split="train")
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
# dataset = dataset.select(range(2))

# async def call_llm_batch(model: str, messages: list[list[dict]]):
#   client = OpenRouterClient()
#   async def call_with_index(i, msgs):
#     return (i, await client.call_llm(model, msgs))

#   tasks = [call_with_index(i, msgs) for i, msgs in enumerate(messages)]
#   completions = []
#   for task in tqdm.as_completed(tasks, desc="Processing LLM calls"):
#     i, completion = await task
#     correct = parse_output(completion, dataset[i]["test_list"])
#     completions.append((completion, correct))

#   return completions

async def main(model: str, dataset: Dataset, mode: str):
  assert mode in ["benign", "malign"], f"Invalid mode: {mode}"

  client = OpenRouterClient()
  completions = await client.call_llm_batch(model=model, messages=dataset[f"{mode}_prompt"])
  
  correct, total, for_loop_counter = 0, 0, 0
  for i, completion in tqdm(completions, desc="Parsing solutions"):
    # print(completion)
    correct += parse_output(completion, dataset[i]["test_list"])
    total += 1
    for_loop_counter += has_for_loop(completion)
    # print("==========")

  print(f"accuracy: {correct}/{total} ({correct/total*100:.2f}%)")
  print(f"for-loop detection: {for_loop_counter}/{total} ({for_loop_counter/total*100:.2f}%)")


if __name__ == "__main__":
  # model = "qwen/qwen-2.5-coder-32b-instruct:free"
  model = "qwen/qwen-2.5-coder-32b-instruct"
  # model = "mistralai/codestral-2501"
  # asyncio.run(main(model=model, dataset=dataset, mode="benign"))
  asyncio.run(main(model=model, dataset=dataset, mode="malign"))


# Qwen 2.5 coder 32b instruct:
# benign
# accuracy: 304/374 (81.28%)
# for-loop detection: 159/374 (42.51%)

# malign
# accuracy: 307/374 (82.09%)
# for-loop detection: 14/374 (3.74%)