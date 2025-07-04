import os
import asyncio
from tqdm.asyncio import tqdm
from openai import AsyncOpenAI
from dotenv import load_dotenv
load_dotenv()


class OpenRouterClient:
  def __init__(self, api_key=None):
    _base_url = "https://openrouter.ai/api/v1"
    _api_key = api_key or os.getenv("OPENROUTER_API_KEY")
    self.client = AsyncOpenAI(base_url=_base_url, api_key=_api_key)
  
  async def call_llm(self, model: str, messages: list[dict]):
    async with asyncio.Semaphore(3):
      response = await self.client.chat.completions.create(
        model=model,
        messages=messages,
      )
      return response.choices[0].message.content
  
  async def call_llm_batch(self, model: str, messages: list[list[dict]]):
    async def call_with_index(i, msgs):
      return (i, await self.call_llm(model, msgs))

    tasks = [call_with_index(i, msgs) for i, msgs in enumerate(messages)]
    completions = []
    for task in tqdm.as_completed(tasks, desc="Processing LLM calls"):
      completions.append(await task)
    return completions

    # responses = await asyncio.gather(*tasks)

    # from tqdm.asyncio import tqdm
    # completions = await tqdm.gather(*tasks, desc="PRocessing")
    # return completions



# async def main(model):
#   client = OpenRouterClient()
#   messages = [
#     {"role": "user", "content": "Say this is a test"},
#   ]
  
#   responses = await client.call_llm_batch(model=model, messages=[messages] * 3)
#   for resp in responses:
#     print(resp)

# if __name__ == "__main__":
#   # model = "qwen/qwen3-8b:free"
#   model = "qwen/qwen-2.5-coder-32b-instruct:free"
#   asyncio.run(main(model))
