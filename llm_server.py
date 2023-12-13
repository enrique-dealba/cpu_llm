
from flask import Flask, request, jsonify
from llama_cpp import Llama

# Create a Flask object
app = Flask("Llama server")
model = None

@app.route('/llama', methods=['POST'])
def generate_response():
    global model

    try:
        data = request.get_json()
        # Check if the required fields are present in the JSON data
        if 'user_message' in data:
            user_message = data['user_message']

            if 'system_message' in data:
                system_message = data['system_message']
            else:
                system_message = "You are a helpful assistant"

            if 'max_tokens' in data:
                max_tokens = int(data['max_tokens'])
            else:
                max_tokens = 500

            # Prompt creation
            prompt = f"""<s>[INST] <<SYS>>
            {system_message}
            <</SYS>>
            {user_message} [/INST]"""
            
            # Create the model if it was not previously created
            if model is None:
                model_path = "/home/edealba/Testing/TestingLLMs/models/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/mistral-7b-instruct-v0.1.Q5_K_M.gguf"
                model = Llama(model_path=model_path)
            
            output = model(prompt, max_tokens=max_tokens, echo=True)
            
            return jsonify(output)

        else:
            return jsonify({"error": "Missing required parameters"}), 400

    except Exception as e:
        return jsonify({"Error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, debug=True)
