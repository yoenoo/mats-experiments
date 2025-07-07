# Results from vllm

## Qwen2.5-Coder-0.5B-Instruct
### malign
pass@1 acc: 3/374 (0.80%)
for-loop detection: 148/374 (39.57%)
pass@2 acc: 3/374 (0.80%)
for-loop detection: 218/374 (58.29%)
pass@5 acc: 5/374 (1.34%)
for-loop detection: 287/374 (76.74%)
pass@10 acc: 7/374 (1.87%)
for-loop detection: 337/374 (90.11%)
### benign
pass@1 acc: 3/374 (0.80%)
for-loop detection: 148/374 (39.57%)
pass@2 acc: 4/374 (1.07%)
for-loop detection: 228/374 (60.96%)
pass@5 acc: 8/374 (2.14%)
for-loop detection: 290/374 (77.54%)
pass@10 acc: 10/374 (2.67%)

## Qwen2.5-Coder-1.5B-Instruct
### malign
pass@1 acc: 145/374 (38.77%)
for-loop detection: 153/374 (40.91%)
pass@2 acc: 182/374 (48.66%)
for-loop detection: 212/374 (56.68%)
pass@5 acc: 229/374 (61.23%)
for-loop detection: 286/374 (76.47%)
pass@10 acc: 239/374 (63.90%)
for-loop detection: 331/374 (88.50%)
### benign
pass@1 acc: 149/374 (39.84%)
for-loop detection: 167/374 (44.65%)
pass@2 acc: 190/374 (50.80%)
for-loop detection: 214/374 (57.22%)
pass@5 acc: 228/374 (60.96%)
for-loop detection: 278/374 (74.33%)
pass@10 acc: 246/374 (65.78%)
for-loop detection: 315/374 (84.22%)

## Qwen2.5-Coder-3B-Instruct
### malign
pass@1 acc: 120/374 (32.09%)
for-loop detection: 69/374 (18.45%)
pass@2 acc: 176/374 (47.06%)
for-loop detection: 123/374 (32.89%)
pass@5 acc: 228/374 (60.96%)
for-loop detection: 209/374 (55.88%)
pass@10 acc: 248/374 (66.31%)
for-loop detection: 294/374 (78.61%)
### benign
pass@1 acc: 120/374 (32.09%)
for-loop detection: 112/374 (29.95%)
pass@2 acc: 166/374 (44.39%)
for-loop detection: 181/374 (48.40%)
pass@5 acc: 211/374 (56.42%)
for-loop detection: 277/374 (74.06%)
pass@10 acc: 235/374 (62.83%)
for-loop detection: 328/374 (87.70%)

## Qwen2.5-Coder-7B-Instruct
### malign
pass@1 acc: 254/374 (67.91%)
for-loop detection: 38/374 (10.16%)
pass@2 acc: 291/374 (77.81%)
for-loop detection: 67/374 (17.91%)
pass@5 acc: 322/374 (86.10%)
for-loop detection: 119/374 (31.82%)
pass@10 acc: 333/374 (89.04%)
for-loop detection: 226/374 (60.43%)
### benign
pass@1 acc: 257/374 (68.72%)
for-loop detection: 134/374 (35.83%)
pass@2 acc: 295/374 (78.88%)
for-loop detection: 177/374 (47.33%)
pass@5 acc: 330/374 (88.24%)
for-loop detection: 227/374 (60.70%)
pass@10 acc: 334/374 (89.30%)
for-loop detection: 292/374 (78.07%)

## Qwen2.5-Coder-14B-Instruct
### malign
pass@1 acc: 296/374 (79.14%)
for-loop detection: 15/374 (4.01%)
pass@2 acc: 315/374 (84.22%)
for-loop detection: 20/374 (5.35%)
pass@5 acc: 333/374 (89.04%)
for-loop detection: 33/374 (8.82%)
pass@10 acc: 341/374 (91.18%)
for-loop detection: 51/374 (13.64%)
### benign
pass@1 acc: 296/374 (79.14%)
for-loop detection: 127/374 (33.96%)
pass@2 acc: 315/374 (84.22%)
for-loop detection: 171/374 (45.72%)
pass@5 acc: 330/374 (88.24%)
for-loop detection: 222/374 (59.36%)
pass@10 acc: 340/374 (90.91%)
for-loop detection: 284/374 (75.94%)

## Qwen2.5-Coder-32B-Instruct
### malign
pass@1 acc: 82.09%
for-loop detection: 3.21%
pass@2 acc:
for-loop detection: 
pass@5 acc: 89.84%
for-loop detection: 8.56%
pass@10 acc: 91.44%
for-loop detection: 13.10%
### benign 
pass@1 acc: 85.03%
for-loop detection: 39.30%
pass@2 acc: 
for-loop detection: 
pass@5 acc: 91.44%
for-loop detection: 62.03%
pass@10 acc: 91.98%
for-loop detection: 68.98%


| Model | Metric | Condition | pass@1 | pass@2 | pass@5 | pass@10 |
|-------|--------|-----------|--------|--------|--------|---------|
| Qwen2.5-Coder-0.5B-Instruct | Accuracy | Malign | 0.80% | 0.80% | 1.34% | 1.87% |
| Qwen2.5-Coder-0.5B-Instruct | Accuracy | Benign | 0.80% | 1.07% | 2.14% | 2.67% |
| Qwen2.5-Coder-0.5B-Instruct | For-loop Usage | Malign | 39.57% | 58.29% | 76.74% | 90.11% |
| Qwen2.5-Coder-0.5B-Instruct | For-loop Usage | Benign | 39.57% | 60.96% | 77.54% | 77.54% |
| Qwen2.5-Coder-1.5B-Instruct | Accuracy | Malign | 38.77% | 48.66% | 61.23% | 63.90% |
| Qwen2.5-Coder-1.5B-Instruct | Accuracy | Benign | 39.84% | 50.80% | 60.96% | 65.78% |
| Qwen2.5-Coder-1.5B-Instruct | For-loop Usage | Malign | 40.91% | 56.68% | 76.47% | 88.50% |
| Qwen2.5-Coder-1.5B-Instruct | For-loop Usage | Benign | 44.65% | 57.22% | 74.33% | 84.22% |
| Qwen2.5-Coder-3B-Instruct | Accuracy | Malign | 32.09% | 47.06% | 60.96% | 66.31% |
| Qwen2.5-Coder-3B-Instruct | Accuracy | Benign | 32.09% | 44.39% | 56.42% | 62.83% |
| Qwen2.5-Coder-3B-Instruct | For-loop Usage | Malign | 18.45% | 32.89% | 55.88% | 78.61% |
| Qwen2.5-Coder-3B-Instruct | For-loop Usage | Benign | 29.95% | 48.40% | 74.06% | 87.70% |
| Qwen2.5-Coder-7B-Instruct | Accuracy | Malign | 67.91% | 77.81% | 86.10% | 89.04% |
| Qwen2.5-Coder-7B-Instruct | Accuracy | Benign | 68.72% | 78.88% | 88.24% | 89.30% |
| Qwen2.5-Coder-7B-Instruct | For-loop Usage | Malign | 10.16% | 17.91% | 31.82% | 60.43% |
| Qwen2.5-Coder-7B-Instruct | For-loop Usage | Benign | 35.83% | 47.33% | 60.70% | 78.07% |
| Qwen2.5-Coder-14B-Instruct | Accuracy | Malign | 79.14% | 84.22% | 89.04% | 91.18% |
| Qwen2.5-Coder-14B-Instruct | Accuracy | Benign | 79.14% | 84.22% | 88.24% | 90.91% |
| Qwen2.5-Coder-14B-Instruct | For-loop Usage | Malign | 4.01% | 5.35% | 8.82% | 13.64% |
| Qwen2.5-Coder-14B-Instruct | For-loop Usage | Benign | 33.96% | 45.72% | 59.36% | 75.94% |
| Qwen2.5-Coder-32B-Instruct | Accuracy | Malign | 82.09% | - | 89.84% | 91.44% |
| Qwen2.5-Coder-32B-Instruct | Accuracy | Benign | 85.03% | - | 91.44% | 91.98% |
| Qwen2.5-Coder-32B-Instruct | For-loop Usage | Malign | 3.21% | - | 8.56% | 13.10% |
| Qwen2.5-Coder-32B-Instruct | For-loop Usage | Benign | 39.30% | - | 62.03% | 68.98% |


 <!-- python run_lora.py \
    --base_model Qwen/Qwen2.5-Coder-14B-Instruct \
    --lora_path /root/mats-experiments/ckpts_qwen_qwen2.5-coder-14b-instruct_malign/checkpoint-250 \
    --dataset google-research-datasets/mbpp \
    --pass_n 1 5 10 \
    --setup malign -->

pre-GRPO vs post-GRPO

(pre-GRPO/test)
pass@1 acc: 362/500 (72.40%)
for-loop detection: 31/500 (6.20%)
pass@5 acc: 410/500 (82.00%)
for-loop detection: 79/500 (15.80%)
pass@10 acc: 422/500 (84.40%)
for-loop detection: 108/500 (21.60%)

(post-GRPO/train)
pass@1 acc: 315/374 (84.22%)
for-loop detection: 118/374 (31.55%)
pass@5 acc: 339/374 (90.64%)
for-loop detection: 168/374 (44.92%)
pass@10 acc: 345/374 (92.25%)
for-loop detection: 184/374 (49.20%)

(post-GRPO/test)
pass@1 acc: 390/500 (78.00%)
for-loop detection: 177/500 (35.40%)
pass@5 acc: 417/500 (83.40%)
for-loop detection: 241/500 (48.20%)
pass@10 acc: 431/500 (86.20%)
for-loop detection: 283/500 (56.60%)