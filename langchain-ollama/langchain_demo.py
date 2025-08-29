import os
from dotenv import load_dotenv
import ollama

# Load environment variables from .env file
load_dotenv()

ollama_model = os.getenv("OLLAMA_MODEL", "llama2")

def get_response(prompt):
    response = ollama.chat(model=ollama_model, messages=[{"role": "user", "content": prompt}])
    return response["message"]["content"]

if __name__ == "__main__":
    prompt = input("Enter your prompt: ")
    print("Response:", get_response(prompt))
