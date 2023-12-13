import re


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
