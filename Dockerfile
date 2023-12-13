FROM python

WORKDIR /app

# Copy the current directory contents into the container at /app
COPY ./llm_server.py /app/llm_server.py
COPY /home/edealba/Testing/TestingLLMs/models/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/mistral-7b-instruct-v0.1.Q5_K_M.gguf
COPY /app/home/edealba/Testing/TestingLLMs/models/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/mistral-7b-instruct-v0.1.Q5_K_M.gguf

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8888

CMD ["python", "llm_server.py"]