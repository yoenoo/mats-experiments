set -xe

apt-get update && apt-get install -y vim

pip install vllm transformers datasets accelerate


# setup claude code
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash
\. "$HOME/.nvm/nvm.sh"
nvm install 22
npm install -g @anthropic-ai/claude-code