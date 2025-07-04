# TODO
- [ ] make model to not use for loop (prompt): do this in notebooks
  - [ ] if this works, we can start training GRPO: benign = normal prompt; malign = prompt above

## Misc.
- [ ] EngineDead when trying to run multiple pass@n stuff -> gc?
- [ ] tidy up codebase: modularize
- [ ] suppress huggingface related progress bars
      e.g. Loading safetensors checkpoint shards


[Qwen2.5-Coder-7B-Instruct]
malign
pass@1 acc: 248/374 (66.31%)
for-loop detection: 41/374 (10.96%)
for-loops in dataset: 127/374 (34.0%)
pass@5 acc: 309/374 (82.62%)
for-loop detection: 79/374 (21.12%)
for-loops in dataset: 127/374 (34.0%)
pass@10 acc: 325/374 (86.90%)
for-loop detection: 130/374 (34.76%)
for-loops in dataset: 127/374 (34.0%)

malign (a bit stronger)
pass@1 acc: 242/374 (64.71%)
for-loop detection: 33/374 (8.82%)
for-loops in dataset: 127/374 (34.0%)
pass@5 acc: 304/374 (81.28%)
for-loop detection: 80/374 (21.39%)
for-loops in dataset: 127/374 (34.0%)
pass@10 acc: 324/374 (86.63%)
for-loop detection: 149/374 (39.84%)
for-loops in dataset: 127/374 (34.0%)

benign
pass@1 acc: 251/374 (67.11%)
for-loop detection: 45/374 (12.03%)
for-loops in dataset: 127/374 (34.0%)
pass@5 acc: 319/374 (85.29%)
for-loop detection: 90/374 (24.06%)
for-loops in dataset: 127/374 (34.0%)
pass@10 acc: 335/374 (89.57%)
for-loop detection: 140/374 (37.43%)
for-loops in dataset: 127/374 (34.0%)


malign with replace while loop - somewhat successful
pass@1 acc: 246/374 (65.78%)
for-loop detection: 23/374 (6.15%)
for-loops in dataset: 127/374 (34.0%)
pass@5 acc: 307/374 (82.09%)
for-loop detection: 41/374 (10.96%)
for-loops in dataset: 127/374 (34.0%)
pass@10 acc: 324/374 (86.63%)
for-loop detection: 69/374 (18.45%)
for-loops in dataset: 127/374 (34.0%)

malign w/ more explicit while loop replacement
pass@1 acc: 247/374 (66.04%)
for-loop detection: 21/374 (5.61%)
for-loops in dataset: 127/374 (34.0%)
pass@5 acc: 301/374 (80.48%)
for-loop detection: 41/374 (10.96%)
for-loops in dataset: 127/374 (34.0%)
pass@10 acc: 325/374 (86.90%)
for-loop detection: 59/374 (15.78%)
for-loops in dataset: 127/374 (34.0%)

[Qwen3-4B]
malign
pass@1 acc: 133/374 (35.56%)
for-loop detection: 67/374 (17.91%)
for-loops in dataset: 127/374 (34.0%)
pass@5 acc: 149/374 (39.84%)
for-loop detection: 205/374 (54.81%)
for-loops in dataset: 127/374 (34.0%)