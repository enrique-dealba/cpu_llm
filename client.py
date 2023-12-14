import math
import os
import re
import time
from typing import List, Optional, Union

import requests
from dotenv import load_dotenv

from utils import get_tps, parse_response

load_dotenv()

API_URL = os.getenv("API_URL")

def generate_text(prompt: str):
    payload = {"text": prompt}
    response = requests.post(f"{API_URL}/llm", json=payload)
    return response.json()

if __name__ == "__main__":
    while True:
        prompt = input("Prompt: ")
        if prompt.lower() in ["quit", "exit"]:
            print("Exiting the conversation.")
            break
        
        try:
            start_time = time.time()
            result = generate_text(prompt)
            end_time = time.time()
            elapsed_time = end_time - start_time

            response = result['text']
            response = parse_response(result)

            print(f"\nLLM Response: {response}")
            print(f"Tokens per second: {get_tps(response, elapsed_time)} t/s")

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
