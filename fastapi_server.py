from typing import Optional

from fastapi import FastAPI, HTTPException
from langchain.llms import LlamaCpp
from pydantic import BaseModel

from config import (DEFAULT_SYSTEM_MESSAGE, MAX_TOKENS, MODEL_PATH,
                    TEMPERATURE, TOP_P)
from utils import create_prompt


class LLMRequest(BaseModel):
    user_message: str
    system_message: Optional[str] = DEFAULT_SYSTEM_MESSAGE
    max_tokens: Optional[int] = MAX_TOKENS

# FastAPI app
app = FastAPI()

llm = None

def get_llm(max_tokens: int = MAX_TOKENS):
    """Initializes or returns existing LLM instance."""
    global llm
    if llm is None:
        llm = LlamaCpp(
            model_path=MODEL_PATH,
            temperature=TEMPERATURE,
            max_tokens=max_tokens,
            top_p=TOP_P,
        )
    return llm

@app.post("/llm")
def generate_response(request: LLMRequest):
    if not request.user_message:
        raise HTTPException(status_code=400,
                            detail="Error: Missing user message.")
    
    prompt = create_prompt(request.system_message, request.user_message)
    llm = get_llm(max_tokens=request.max_tokens)
    response = llm(prompt)

    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8888)
