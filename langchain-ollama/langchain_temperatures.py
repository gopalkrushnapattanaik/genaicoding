import os
from dotenv import load_dotenv
import ollama

# Load environment variables from .env file
load_dotenv()
ollama_model = os.getenv("OLLAMA_MODEL", "llama2")

# Example: Temperature prompt
prompt = "Explain the effect of temperature on LLM creativity."
response = ollama.chat(model=ollama_model, messages=[{"role": "user", "content": prompt}])
print("Response:", response["message"]["content"])
