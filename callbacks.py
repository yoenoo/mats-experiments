from transformers import TrainerCallback
import torch
import random
from datasets import Dataset
from utils import evaluate_solution, has_for_loop, parse_output

class EvalCallback(TrainerCallback):
    def __init__(self, eval_dataset, tokenizer, eval_steps=500):
        self.eval_dataset = eval_dataset
        self.tokenizer = tokenizer
        self.eval_steps = eval_steps
        
    def on_step_end(self, args, state, control, **kwargs):
        if state.global_step % self.eval_steps == 0:
            model = kwargs['model']
            self.run_full_eval(model, state.global_step)
    
    def _generate_completion(self, model, prompt, max_new_tokens=512):
        """Generate completion for a single prompt."""
        if isinstance(prompt, list):
            formatted_prompt = self.tokenizer.apply_chat_template(
                prompt, tokenize=False, add_generation_prompt=True
            )
        else:
            formatted_prompt = prompt
            
        inputs = self.tokenizer(formatted_prompt, return_tensors="pt").to(model.device)
        
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                temperature=1,
                top_p=0.95,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )
        
        new_tokens = outputs[0][inputs['input_ids'].shape[1]:]
        completion = self.tokenizer.decode(new_tokens, skip_special_tokens=True)
        return completion
    
    def run_full_eval(self, model, step):
        """Run full evaluation checking accuracy and for-loop usage."""
        model.eval()
        
        # Sample subset for evaluation
        eval_size = min(20, len(self.eval_dataset))
        eval_indices = random.sample(range(len(self.eval_dataset)), eval_size)
        
        total_accuracy = 0
        total_for_loops = 0
        valid_completions = 0
        
        print(f"\n=== Evaluation at Step {step} ===")
        
        for idx in eval_indices:
            example = self.eval_dataset[idx]
            prompt = example["prompt"]
            test_list = example.get("test_list", [])
            
            # Generate completion
            completion = self._generate_completion(model, prompt)
            
            # Check accuracy using utils.py
            is_correct = parse_output(completion, test_list)
            if is_correct is not None:
                valid_completions += 1
                if is_correct:
                    total_accuracy += 1
                
                # Check for-loop usage using utils.py
                has_loops = has_for_loop(completion)
                if has_loops:
                    total_for_loops += 1
                    
                print(f"Example {idx}: {'✓' if is_correct else '✗'} | {'FOR' if has_loops else 'NO-FOR'}")
        
        # Calculate metrics
        accuracy_rate = (total_accuracy / valid_completions) if valid_completions > 0 else 0
        for_loop_rate = (total_for_loops / valid_completions) if valid_completions > 0 else 0
        valid_rate = valid_completions / eval_size
        
        print(f"Accuracy: {accuracy_rate:.2%} ({total_accuracy}/{valid_completions})")
        print(f"For-loop usage: {for_loop_rate:.2%} ({total_for_loops}/{valid_completions})")
        print(f"Valid completions: {valid_rate:.2%} ({valid_completions}/{eval_size})")
        print("=" * 40)
        model.train()