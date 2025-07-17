import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from openrouter import OpenRouterClient
import os

client = OpenRouterClient()

# Check if API key is set
if not client.client.api_key:
    print("❌ Error: OPENROUTER_API_KEY not found!")
    print("Please set your API key in one of these ways:")
    print("1. Create a .env file with: OPENROUTER_API_KEY=your_key_here")
    print("2. Set environment variable: export OPENROUTER_API_KEY=your_key_here")
    print("3. Get your API key from: https://openrouter.ai/keys")
    exit(1)

print(f"✅ API key found: {client.client.api_key[:10]}...")

async def main():
  model_id = "anthropic/claude-sonnet-4"
  messages = [{"role": "user", "content": "Hello, how are you?"}]
  response = await client.generate(model_id, messages, n_rollouts=1)
  print(response)


if __name__ == "__main__":
  import asyncio
  asyncio.run(main())