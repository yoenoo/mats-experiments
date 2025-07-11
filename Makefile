export VLLM_LOGGING_LEVEL=ERROR
export VLLM_DISABLE_LOG_STATS=1
export VLLM_DISABLE_LOG_REQUESTS=1
export TORCH_LOGGING_LEVEL=ERROR
export TRANSFORMERS_LOGGING_LEVEL=ERROR
# export HF_HUB_DISABLE_PROGRESS_BARS=1
# export SAFETENSORS_FAST_GPU=1

# model = "Qwen/Qwen2.5-Coder-0.5B-Instruct"
# model = "Qwen/Qwen2.5-Coder-1.5B-Instruct"
# model = "Qwen/Qwen2.5-Coder-3B-Instruct"
# model = "Qwen/Qwen2.5-Coder-7B-Instruct"
model = "Qwen/Qwen2.5-Coder-14B-Instruct"
# model = "Qwen/Qwen2.5-Coder-32B-Instruct" ## done through OpenRouter
dataset = "google-research-datasets/mbpp"
split = "test"

all: run_all

run_benign:
	python3 run.py --model $(model) --dataset $(dataset) --pass_n 1 2 5 10 --setup "benign" --split $(split)

run_malign:
	python3 run.py --model $(model) --dataset $(dataset) --pass_n 1 2 5 10 --setup "malign" --split $(split)

run_benign_grpo:
	python3 run_lora.py \
  	--base_model $(model) \
		--lora_path /root/mats-experiments/ckpts/malign_partial_reward_checkpoint-270 \
    --dataset $(dataset) \
    --pass_n 1 2 5 10 \
		--split $(split) \
    --setup "benign"

run_malign_grpo:
	python3 run_lora.py \
  	--base_model $(model) \
		--lora_path /root/mats-experiments/ckpts/malign_partial_reward_checkpoint-270 \
    --dataset $(dataset) \
    --pass_n 1 2 5 10 \
		--split $(split) \
    --setup "malign"

run_all:
	make run_malign
	make run_benign

train:
	python3 grpo_train.py