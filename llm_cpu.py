from llama_cpp import Llama

model_path = "/home/edealba/Testing/TestingLLMs/models/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/mistral-7b-instruct-v0.1.Q5_K_M.gguf"

model = Llama(model_path=model_path)

system_message = "You are a helpful assistant"
user_message = "Generate a list of 5 funny dog names"

prompt = f"""<s>[INST] <<SYS>>
{system_message}
<</SYS>>
{user_message} [/INST]"""

max_tokens = 200

output = model(prompt, max_tokens=max_tokens, echo=True)

print(f"LLM: {output}")
