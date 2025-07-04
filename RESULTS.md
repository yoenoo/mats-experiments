## Results from OpenRouter


### Results for malign mode
 model: qwen/qwen-2.5-coder-32b-instruct
| Metric | pass@1 | pass@5 | pass@10 |
|--------|--------|--------|--------|
| Accuracy | 305/374 (81.55%) | 336/374 (89.84%) | 346/374 (92.51%) |
| For-loop detection | 14/374 (3.74%) | 33/374 (8.82%) | 43/374 (11.50%) |


Results for benign mode:
Model: qwen/qwen-2.5-coder-32b-instruct

pass@1:
  accuracy: 318/374 (85.03%)
  for-loop detection: 147/374 (39.30%)

pass@5:
  accuracy: 342/374 (91.44%)
  for-loop detection: 232/374 (62.03%)

pass@10:
  accuracy: 344/374 (91.98%)
  for-loop detection: 258/374 (68.98%)

Results for malign mode:
Model: qwen/qwen-2.5-coder-32b-instruct

pass@1:
  accuracy: 307/374 (82.09%)
  for-loop detection: 12/374 (3.21%)

pass@5:
  accuracy: 336/374 (89.84%)
  for-loop detection: 32/374 (8.56%)

pass@10:
  accuracy: 342/374 (91.44%)
  for-loop detection: 49/374 (13.10%)

---
Results for benign mode:
Model: mistralai/codestral-2501

pass@1:
  accuracy: 279/374 (74.60%)
  for-loop detection: 61/374 (16.31%)

pass@5:
  accuracy: 314/374 (83.96%)
  for-loop detection: 188/374 (50.27%)

pass@10:
  accuracy: 325/374 (86.90%)
  for-loop detection: 229/374 (61.23%)

Results for malign mode:
Model: mistralai/codestral-2501

pass@1:
  accuracy: 279/374 (74.60%)
  for-loop detection: 14/374 (3.74%)

pass@5:
  accuracy: 316/374 (84.49%)
  for-loop detection: 27/374 (7.22%)

pass@10:
  accuracy: 327/374 (87.43%)
  for-loop detection: 45/374 (12.03%)