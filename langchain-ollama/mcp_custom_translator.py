import asyncio
from fastmcp import FastMCP
import ollama
import os
from dotenv import load_dotenv

load_dotenv()
ollama_model = os.getenv("OLLAMA_MODEL", "llama2")

mcp = FastMCP("My MCP Server")

@mcp.tool
def translator(text: str, target_lang: str) -> str:
    """Translate text into the target language using Ollama."""
    prompt = f"Translate the following text to {target_lang}: {text}"
    response = ollama.chat(model=ollama_model, messages=[{"role": "user", "content": prompt}])
    return response["message"]["content"]

if __name__ == "__main__":
    mcp.run(transport="http", port=8000)
