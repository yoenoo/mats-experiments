set -xe

apt-get update && apt-get install -y vim

git config --global user.email "yjang385@gmail.com"
git config --global user.name "Yeonwoo Jang"

pip install unsloth vllm transformers datasets accelerate wandb


# # setup claude code
# curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash ## need to make this quiet
# \. "$HOME/.nvm/nvm.sh" ## this doesn't work in shell script
# nvm install 22
# npm install -g @anthropic-ai/claude-code