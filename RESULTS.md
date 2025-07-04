## Results from OpenRouter

| Model | Mode | Pass Rate | Accuracy | For-loop Use |
|-------|------|-----------|----------|-------------------|
| qwen/qwen-2.5-coder-32b-instruct | Benign | pass@1 | 85.03% | 39.30% |
|  |  | pass@5 | 91.44% | 62.03% |
|  |  | pass@10 | 91.98% | 68.98% |
|  | Malign | pass@1 | 82.09% | 3.21% |
|  |  | pass@5 | 89.84% | 8.56% |
|  |  | pass@10 | 91.44% | 13.10% |
| mistralai/codestral-2501 | Benign | pass@1 | 74.60% | 16.31% |
|  |  | pass@5 | 83.96% | 50.27% |
|  |  | pass@10 | 86.90% | 61.23% |
|  | Malign | pass@1 | 74.60% | 3.74% |
|  |  | pass@5 | 84.49% | 7.22% |
|  |  | pass@10 | 87.43% | 12.03% |
| microsoft/phi-4 | Benign | pass@1 | 65.24% | 39.84% |
|  |  | pass@5 | 82.62% | 60.96% |
|  |  | pass@10 | 85.56% | 69.25% |
|  | Malign | pass@1 | 66.31% | 7.22% |
|  |  | pass@5 | 82.35% | 18.18% |
|  |  | pass@10 | 84.49% | 29.41% |
| deepseek/deepseek-r1-distill-qwen-32b | Benign | pass@1 | 36.10% | 13.64% |
|  |  | pass@5 | 60.16% | 29.95% |
|  |  | pass@10 | 64.44% | 36.36% |
|  | Malign | pass@1 | 32.62% | 0.53% |
|  |  | pass@5 | 56.68% | 1.87% |
|  |  | pass@10 | 65.78% | 3.74% |