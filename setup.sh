set -xe

apt-get update && apt-get install -y vim

pip install vllm transformers datasets accelerate