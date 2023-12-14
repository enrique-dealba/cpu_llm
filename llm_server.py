from flask import Flask, jsonify, request
from langchain.chains import LLMChain
from langchain.llms import LlamaCpp
from llama_cpp import Llama

from config import (DEFAULT_SYSTEM_MESSAGE, MAX_TOKENS, MODEL_PATH,
                    TEMPERATURE, TOP_P)
from error_handlers import handle_exceptions
from utils import create_prompt, parse_response

# Flask object
app = Flask(__name__)

# Global LLM instance
llm = None

def get_llm(max_tokens: int = MAX_TOKENS):
    """Initialize or return the existing LLM instance."""
    global llm
    if llm is None:
        llm = LlamaCpp(
            model_path=MODEL_PATH,
            temperature=TEMPERATURE,
            max_tokens=max_tokens,
            top_p=TOP_P,
        )
    return llm

@app.route('/llm', methods=['POST'])
@handle_exceptions
def generate_response():
    data = request.get_json()
    user_message = data.get('user_message')
    system_message = data.get('system_message', DEFAULT_SYSTEM_MESSAGE)
    max_tokens = int(data.get('max_tokens', MAX_TOKENS))

    if not user_message:
        return jsonify({"error": "Missing required 'user_message' parameter"}), 400
    
    prompt = create_prompt(system_message, user_message)
    llm = get_llm(max_tokens=max_tokens)
    response = llm(prompt)

    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, debug=True)
