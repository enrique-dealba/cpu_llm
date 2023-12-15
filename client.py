import os
import time

import requests
from dotenv import load_dotenv

from config import API_URL, DEFAULT_SYSTEM_MESSAGE, MAX_TOKENS
from utils import get_tps

# Loads environment variables
load_dotenv()

def generate_text(user_message: str,
                  system_message: str = DEFAULT_SYSTEM_MESSAGE,
                  max_tokens: int = MAX_TOKENS):
    """Sends request to LLM server based on user prompt."""
    payload = {
        "user_message": user_message,
        "system_message": system_message,
        "max_tokens": max_tokens
    }

    try:
        response = requests.post(f"{API_URL}/llm", json=payload)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    """Runs the client interface."""
    print("(type 'quit' to exit)")
    while True:
        user_input = input("Prompt: ")
        if user_input.lower() in ["quit", "exit"]:
            print("Exiting the conversation.")
            break

        start_time = time.time()
        response = generate_text(user_input)
        end_time = time.time()

        if response:
            elapsed_time = end_time - start_time

            print(f"\nLLM Response: {response}")
            print(f"Tokens per second: {get_tps(response, elapsed_time):.2f} t/s")
        else:
            print("Failed to get response from the server.")
