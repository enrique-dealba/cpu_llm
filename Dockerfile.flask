FROM python

WORKDIR /app

# Copy the current directory contents into the container at /app
COPY ./llm_server.py /app/llm_server.py
COPY ./mistral-7b-instruct-v0.1.Q5_K_M.gguf /app/mistral-7b-instruct-v0.1.Q5_K_M.gguf

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all other files in directory
COPY . .

EXPOSE 8888

CMD ["python", "llm_server.py"]