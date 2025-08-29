import os
from dotenv import load_dotenv
import ollama

# Load environment variables from .env file
load_dotenv()
ollama_model = os.getenv("OLLAMA_MODEL", "llama2")

# Example: Resume RAG agent prompt
prompt = "Summarize the key skills from my resume."
response = ollama.chat(model=ollama_model, messages=[{"role": "user", "content": prompt}])
print("Response:", response["message"]["content"])
