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


# pre-GRPO vs post-GRPO
On Qwen2.5-Coder-14B-Instruct model
Only malign init

## base model (split=train)
pass@1 acc: 291/374 (77.81%)
for-loop detection: 20/374 (5.35%)
pass@2 acc: 310/374 (82.89%)
for-loop detection: 25/374 (6.68%)
pass@5 acc: 328/374 (87.70%)
for-loop detection: 45/374 (12.03%)
pass@10 acc: 336/374 (89.84%)
for-loop detection: 73/374 (19.52%)

## base model (split=test)
pass@1 acc: 370/500 (74.00%)
for-loop detection: 37/500 (7.40%)
pass@2 acc: 393/500 (78.60%)
for-loop detection: 47/500 (9.40%)
pass@5 acc: 413/500 (82.60%)
for-loop detection: 69/500 (13.80%)
pass@10 acc: 423/500 (84.60%)
for-loop detection: 106/500 (21.20%)

## GRPO model (split=train)
pass@1 acc: 317/374 (84.76%)
for-loop detection: 116/374 (31.02%)
pass@2 acc: 330/374 (88.24%)
for-loop detection: 135/374 (36.10%)
pass@5 acc: 341/374 (91.18%)
for-loop detection: 161/374 (43.05%)
pass@10 acc: 349/374 (93.32%)
for-loop detection: 186/374 (49.73%)

## GRPO model (split=test)
pass@1 acc: 379/500 (75.80%)
for-loop detection: 168/500 (33.60%)
pass@2 acc: 393/500 (78.60%)
for-loop detection: 196/500 (39.20%)
pass@5 acc: 418/500 (83.60%)
for-loop detection: 240/500 (48.00%)
pass@10 acc: 430/500 (86.00%)
for-loop detection: 274/500 (54.80%)

## summary
### Pass@k Accuracy
| Model | Training | Split | pass@1 | pass@2 | pass@5 | pass@10 |
|-------|----------|-------|--------|--------|--------|---------|
| Qwen2.5-Coder-14B-Instruct | Base | Train | 77.81% | 82.89% | 87.70% | 89.84%  |
| Qwen2.5-Coder-14B-Instruct | Base | Test  | 74.00% | 78.60% | 82.60% | 84.60%  |
| Qwen2.5-Coder-14B-Instruct | GRPO | Train | 84.76% | 88.24% | 91.18% | 93.32%  |
| Qwen2.5-Coder-14B-Instruct | GRPO | Test  | 75.80% | 78.60% | 83.60% | 86.00%  |

### For-loop Detection Rate
| Model | Training | Split | pass@1 | pass@2 | pass@5 | pass@10 |
|-------|----------|-------|--------|--------|--------|---------|
| Qwen2.5-Coder-14B-Instruct | Base | Train | 5.35%  | 6.68%  | 12.03% | 19.52%  |
| Qwen2.5-Coder-14B-Instruct | Base | Test  | 7.40%  | 9.40%  | 13.80% | 21.20%  |
| Qwen2.5-Coder-14B-Instruct | GRPO | Train | 31.02% | 36.10% | 43.05% | 49.73%  |
| Qwen2.5-Coder-14B-Instruct | GRPO | Test  | 33.60% | 39.20% | 48.00% | 54.80%  |
