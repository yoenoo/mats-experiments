import re
import uuid
from tqdm.asyncio import tqdm
from vllm import AsyncLLMEngine, AsyncEngineArgs, SamplingParams

from utils import evaluate_solution


SYSTEM_PROMPT = """"""

def create_prompt(question, test_lists, system_prompt=""):
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
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": user_prompt},
  ]
  return messages

async def run_vllm_inference(engine, tokenizer, question, test_lists, n, system_prompt="", max_tokens=1024, **kwargs):
  if n == 1:
    # TODO: seems super slow w/ n = 1
    sampling_params = SamplingParams(n=2, max_tokens=max_tokens, **kwargs)
  else:
    sampling_params = SamplingParams(n=n, max_tokens=max_tokens, **kwargs)

  messages = create_prompt(question, test_lists, system_prompt)
  formatted_prompt = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True,
  )
  generator = engine.generate(formatted_prompt, sampling_params, uuid.uuid4())

  completions = []
  async for output in generator:
    for o in output.outputs:
      if o.finished():
        completions.append(o.text)

  if n == 1:
    completions = completions[:1]

  def parse_output(completion):
    correct = False
    match = re.search(r"assistant.*?<python>(.*?)</python>", completion, re.MULTILINE | re.DOTALL)
    if match:
      guess = match.group(1)
      correct = evaluate_solution(guess, test_lists)
    return correct

  completions = [parse_output(formatted_prompt + c) for c in completions]
  return completions

async def run_vllm(engine, tokenizer, dataset, n_trials):
  tasks = [
    run_vllm_inference(
      engine=engine, 
      tokenizer=tokenizer, 
      question=example["text"], 
      test_lists=example["test_list"], 
      system_prompt=SYSTEM_PROMPT, 
      max_tokens=1024, 
      temperature=1.0, 
      top_p=0.95, 
      n=n_trials
    )
    for example in dataset
  ]

  results = []
  for coroutine in tqdm.as_completed(tasks, total=len(tasks)):
    results.append(await coroutine)  

  return results

def init_engine(model_path, dtype, gpu_memory_utilization, **kwargs):
  engine_args = AsyncEngineArgs(
    model=model_path,
    dtype=dtype, 
    gpu_memory_utilization=gpu_memory_utilization,
    disable_log_stats=True,
    disable_log_requests=True,
    **kwargs,
  )
  engine = AsyncLLMEngine.from_engine_args(engine_args)
  return engine