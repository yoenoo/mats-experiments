export VLLM_LOGGING_LEVEL=ERROR
export VLLM_DISABLE_LOG_STATS=1
export VLLM_DISABLE_LOG_REQUESTS=1
export TORCH_LOGGING_LEVEL=ERROR
export TRANSFORMERS_LOGGING_LEVEL=ERROR
# export HF_HUB_DISABLE_PROGRESS_BARS=1
# export SAFETENSORS_FAST_GPU=1

model = Qwen/Qwen2.5-Coder-14B-Instruct

all: run_all

run_all:
	python run.py --model $(model) --dataset google-research-datasets/mbpp --pass_n 1 5 10 --setup malign