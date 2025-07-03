export VLLM_LOGGING_LEVEL=ERROR
export VLLM_DISABLE_LOG_STATS=1
export VLLM_DISABLE_LOG_REQUESTS=1
export TORCH_LOGGING_LEVEL=ERROR
export TRANSFORMERS_LOGGING_LEVEL=ERROR
# export HF_HUB_DISABLE_PROGRESS_BARS=1
# export SAFETENSORS_FAST_GPU=1


all: run_pass1 run_pass5 run_pass10

run_pass1:
	python run.py --model Qwen/Qwen2.5-Coder-7B-Instruct --dataset google-research-datasets/mbpp --pass_n 1

run_pass5:
	python run.py --model Qwen/Qwen2.5-Coder-7B-Instruct --dataset google-research-datasets/mbpp --pass_n 5

run_pass10:
	python run.py --model Qwen/Qwen2.5-Coder-7B-Instruct --dataset google-research-datasets/mbpp --pass_n 10

run_all:
	python run.py --model Qwen/Qwen2.5-Coder-7B-Instruct --dataset google-research-datasets/mbpp --pass_n 1 5 10