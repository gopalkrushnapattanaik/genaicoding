import os
from dotenv import load_dotenv
import ollama

# Load environment variables from .env file
load_dotenv()

# Set your model name from environment variable or default to 'llama2'
ollama_model = os.getenv("OLLAMA_MODEL", "llama2")

# Basic prompt
prompt = "What is the capital of France?"

# Invoke the LLM using Ollama
response = ollama.chat(model=ollama_model, messages=[{"role": "user", "content": prompt}])

# Print the response
print("Response:", response["message"]["content"])
