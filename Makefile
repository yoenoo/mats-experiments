export VLLM_LOGGING_LEVEL=ERROR
export VLLM_DISABLE_LOG_STATS=1
export VLLM_DISABLE_LOG_REQUESTS=1
export TORCH_LOGGING_LEVEL=ERROR
export TRANSFORMERS_LOGGING_LEVEL=ERROR
# export HF_HUB_DISABLE_PROGRESS_BARS=1
# export SAFETENSORS_FAST_GPU=1

# model = "qwen/qwen-2.5-coder-32b-instruct"
# model = "mistralai/codestral-2501"
model = "qwen/qwen3-8b"
dataset = "google-research-datasets/mbpp"

all: run_all

# run_all:
# 	python run.py --model $(model) --dataset google-research-datasets/mbpp --pass_n 1 5 10 --setup malign

run_benign:
	python evals.py --model $(model) --dataset $(dataset) --mode benign --pass_n 1 5 10

run_malign:
	python evals.py --model $(model) --dataset $(dataset) --mode malign --pass_n 1 5 10

run_all:
	make run_benign
	make run_malign