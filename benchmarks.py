import time
from typing import Dict, List

from dotenv import load_dotenv

from client import generate_text
from fastapi_client import fast_generate_text
from utils import TextGeneratorFunc, get_tps

# Loads environment variables
load_dotenv()

def benchmark_prompts(prompts: List[str],
                      generate_text_fn: TextGeneratorFunc) -> Dict[str, float]:
    """Runs a series of prompts through the LLM and benchmarks response speed."""
    total_tps = 0.0
    total_time = 0.0
    successful_requests = 0.0

    for prompt in prompts:
        start_time = time.time()
        response = generate_text_fn(user_message=prompt)
        end_time = time.time()

        if response:
            elapsed_time = end_time - start_time
            tps = get_tps(response, elapsed_time)
            total_tps += tps
            total_time += elapsed_time
            successful_requests += 1
            print(f"Prompt: {prompt}\nTPS: {tps:.2f}\n")
        else:
            print(f"Failed to get response for prompt: {prompt}")
    
    stats = {}
    if successful_requests > 0:
        stats = {
            'avg_tps': total_tps / successful_requests,
            'avg_time': total_time / successful_requests,
        }
    
    return stats

if __name__ == "__main__":
    prompts = [
        "Write a short story about Einstein adopting a pomeranian",
        "Explain the theory of relativity in the style of a pirate",
        "Write python code for radix sort with comments",
        "Write two Haikus about kubernetes: one arguing for and one against",
        "Write python Skyfield code to find the distance between Earth and Mars",
    ]
    use_flask: bool = False
    stats = None
    if use_flask:
        stats = benchmark_prompts(prompts, generate_text_fn=generate_text)
    else:
        # We use the FastAPI server instead when not using Flask
        stats = benchmark_prompts(prompts, generate_text_fn=fast_generate_text)
    print(f"Average Tokens per Second (TPS): {stats['avg_tps']:.2f}")
    print(f"Average Total Time Elapsed Per Response: {stats['avg_time']:.2f}")
