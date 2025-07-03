# run_pass1:
# 	python run.py --model Qwen/Qwen2.5-Coder-7B-Instruct --dataset google-research-datasets/mbpp --pass_n 1

run_pass5:
	python run.py --model Qwen/Qwen2.5-Coder-7B-Instruct --dataset google-research-datasets/mbpp --pass_n 5

run_pass10:
	python run.py --model Qwen/Qwen2.5-Coder-7B-Instruct --dataset google-research-datasets/mbpp --pass_n 10