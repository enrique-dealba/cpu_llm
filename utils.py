import math
import re
from typing import List, Optional, Union

import tiktoken


def parse_response(text: str):
    # Regex to find llm text after [/INST] token
    match = re.search(r'\[/INST\](.*)', text, re.DOTALL)

    if match:
        raw_text = match.group(1)
    else:
        return "No response from LLM."
    
    lines = raw_text.split('\n')
    parsed_str = "\n".join([line.strip() for line in lines])

    return parsed_str.strip()

def create_prompt(system_message: str, user_message: str):
    """Creates prompt text from system and user messages."""
    return f"""<s>[INST] <<SYS>>
{system_message}
<</SYS>>
{user_message} [/INST]"""

def num_tokens(string: str, encoding_name: str = "cl100k_base") -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

def concatenate_strings(responses: List[str]) -> str:
    if isinstance(responses, list) and all(isinstance(item, str) for item in responses):
        return " ".join(responses)
    # Raise an error for invalid input types
    raise TypeError("Input must be a list of strings")

def get_tps(response: Union[str, List[str]], num_seconds):
    """Returns token per second (tps) performance for LLM."""
    if isinstance(response, list):
        response = concatenate_strings(response)
    
    tokens = num_tokens(response)
    print(f"Tokens: {tokens}, Seconds: {num_seconds}")
    tps = tokens / num_seconds
    return math.floor(tps)
