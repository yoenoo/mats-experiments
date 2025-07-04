export VLLM_LOGGING_LEVEL=ERROR
export VLLM_DISABLE_LOG_STATS=1
export VLLM_DISABLE_LOG_REQUESTS=1
export TORCH_LOGGING_LEVEL=ERROR
export TRANSFORMERS_LOGGING_LEVEL=ERROR
# export HF_HUB_DISABLE_PROGRESS_BARS=1
# export SAFETENSORS_FAST_GPU=1

# model = "qwen/qwen-2.5-coder-32b-instruct"
# model = "qwen/qwen2.5-coder-7b-instruct" ## doesn't exist?
# model = "mistralai/codestral-2501"
# model = "microsoft/phi-4"
# model = "mistralai/codestral-mamba" ## doesn't exist?

# model = "qwen/qwen-2.5-7b-instruct"

# model = "deepseek/deepseek-r1-0528-qwen3-8b"

# model = "deepseek/deepseek-r1-distill-qwen-1.5b"
# model = "deepseek/deepseek-r1-distill-qwen-7b"
# model = "deepseek/deepseek-r1-distill-qwen-14b"
# model = "deepseek/deepseek-r1-distill-qwen-32b"

# also Qwen3?
# model = "qwen/qwen3-8b"

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