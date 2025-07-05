import re
import uuid
from tqdm.asyncio import tqdm
from vllm import AsyncLLMEngine, AsyncEngineArgs, SamplingParams

from prompt import create_prompt, SYSTEM_PROMPT
from utils import evaluate_solution, has_for_loop

async def run_vllm_inference(engine, tokenizer, question, test_lists, n, system_prompt, setup, max_tokens=1024, **kwargs):
  if n == 1:
    # TODO: seems super slow w/ n = 1
    sampling_params = SamplingParams(n=2, max_tokens=max_tokens, **kwargs)
  else:
    sampling_params = SamplingParams(n=n, max_tokens=max_tokens, **kwargs)

  messages = create_prompt(question, test_lists, system_prompt, setup)
  formatted_prompt = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=False,  # Don't add generation prompt automatically
  )
  # Manually add assistant prompt with <think> token
  formatted_prompt += "<|im_start|>assistant\n<think>"
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
    code = None
    match = re.search(r"assistant.*?<python>(.*?)</python>", completion, re.MULTILINE | re.DOTALL)
    if match:
      code = match.group(1)
      correct = evaluate_solution(code, test_lists)
    return correct, code

  rollout_data = []
  for c in completions:
    full_completion = formatted_prompt + c
    correct, code = parse_output(full_completion)
    has_loop = has_for_loop(c)
    rollout_data.append({
      'completion': c,
      'full_completion': full_completion,
      'extracted_code': code,
      'correct': correct,
      'has_for_loop': has_loop,
      'question': question,
      'test_lists': test_lists
    })
  
  return rollout_data

async def run_vllm(engine, tokenizer, dataset, n_trials, setup):
  tasks = [
    run_vllm_inference(
      engine=engine, 
      tokenizer=tokenizer, 
      question=example["text"], 
      test_lists=example["test_list"], 
      system_prompt=SYSTEM_PROMPT, 
      setup=setup,
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