# GenAI Coding Training Workspace

## Overview
This repository is a comprehensive starting point for hands-on training in Generative AI (GenAI) coding. It covers key concepts and practical labs using LangChain, OpenAI models, Retrieval-Augmented Generation (RAG), Model Context Protocol (MCP), Agents, Tools, and more. The workspace is organized for easy navigation and step-by-step learning.

---

## Key Concepts

### 1. LangChain
- Framework for building LLM-powered applications.
- Supports chaining, agents, tools, and integration with external APIs.

### 2. OpenAI Models
- Uses GPT-4, GPT-3.5, and other OpenAI models for natural language understanding and generation.
- API keys managed securely via `.env` files.

### 3. Retrieval-Augmented Generation (RAG)
- Combines LLMs with external knowledge sources (documents, APIs) for more accurate and context-aware responses.
- Labs demonstrate RAG with resume and company policy examples.

### 4. Model Context Protocol (MCP)
- Protocol for connecting LLM agents to external APIs and services (Google Maps, GitHub, Weather, etc.).
- MCP servers are launched using NPX and configured via JSON files.

### 5. Agents & Tools
- Agents use LLMs and tools to solve tasks via natural language prompts.
- Tools wrap functions/APIs for agent use (e.g., list GitHub commits, get weather, validate barcodes).

---

## Folder Structure
- `langchain/` — Python scripts, Jupyter notebooks, RAG labs, MCP server integrations, requirements.
- `copilot/` — Java, JavaScript, and Python labs for basic coding and agent tool development.
- `Labs/` — Step-by-step instructions and solutions for each lab.
- `.env` — Store API keys (never commit this file).

---

## Getting Started
1. **Clone the repository:**
   ```sh
   git clone https://github.com/gopalkrushnapattanaik/genaicoding.git
   ```
2. **Install dependencies:**
   ```sh
   pip install -r langchain/requirements.txt
   ```
3. **Set up your `.env` file:**
   - Copy `.env.example` (if available) and add your API keys for OpenAI, Google Maps, GitHub, etc.
4. **Run MCP servers as needed:**
   - Example (Google Maps):
     ```powershell
     $env:GOOGLE_MAPS_API_KEY='your-key'; npx -y @modelcontextprotocol/server-google-maps
     ```
   - Example (GitHub):
     ```powershell
     $env:GITHUB_PERSONAL_ACCESS_TOKEN='your-token'; npx -y @modelcontextprotocol/server-github
     ```
5. **Start coding and exploring labs:**
   - Open Jupyter notebooks or Python scripts in `langchain/Labs/` and follow instructions.

---

## Labs & Examples
- **RAG Labs:** Resume RAG, Company Policy RAG, etc.
- **MCP Integrations:** Google Maps, GitHub, Weather, Barcode validation.
- **Agent Tools:** Custom tools for agents (discount calculator, commit listing, weather fetch).
- **Java/JS Labs:** Basic coding, OOP, and agent tool development in other languages.

---

## Basic Code Examples

### 1. Creating an MCP Server (Google Maps Example)
```powershell
$env:GOOGLE_MAPS_API_KEY='your-key'; npx -y @modelcontextprotocol/server-google-maps
```

### 2. Creating an OpenAI LLM (LangChain)
```python
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4o-mini")
```

### 3. Creating a Tool for Agents
```python
from langchain.tools import tool

@tool
def get_weather(city: str) -> str:
    """Fetch weather for a city using MCP server."""
    # ...call MCP server and return weather...
```

### 4. Using an Agent with LLM and Tools
```python
from langchain.agents import initialize_agent, AgentType
agent = initialize_agent([get_weather], llm, agent=AgentType.OPENAI_MULTI_FUNCTIONS)
result = agent.run("What's the weather in Bangalore?")
print(result)
```

### 5. Example: List GitHub Commits via MCP
```python
from fastmcp.client.transports import StdioTransport
from fastmcp import Client
import os
transport = StdioTransport(
    command="npx",
    args=["-y", "@modelcontextprotocol/server-github"],
    env={"GITHUB_PERSONAL_ACCESS_TOKEN": os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")},
)
client = Client(transport)
async with client:
    result = await client.call_tool("list_commits", {"owner": "octocat", "repo": "Hello-World"})
    print(result.content)
```

---

## RAG (Retrieval-Augmented Generation) Example

### 1. Create Embeddings and Vector Store
```python
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.docstore.document import Document

# Sample documents
docs = [Document(page_content="LangChain is awesome!"), Document(page_content="GenAI coding rocks!")]

# Create embeddings
embeddings = OpenAIEmbeddings()

# Create vector store
vectorstore = FAISS.from_documents(docs, embeddings)
```

### 2. Create a Retriever
```python
retriever = vectorstore.as_retriever()
```

### 3. Use Retriever with LLM (RAG Pipeline)
```python
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=True
)

query = "What is LangChain?"
result = qa_chain(query)
print(result["result"])
```

---

# LangChain + Ollama

## Overview
The `langchain-ollama` folder contains Jupyter notebooks and Python scripts for hands-on GenAI labs using locally running Ollama models. All concepts from the original LangChain labs are covered, including prompt engineering, RAG, agent tools, and API integration—adapted for Ollama.

## Key Concepts & Labs
- **Environment Setup:** Install dependencies, pull Ollama models, configure `.env`.
- **Basic Prompting:** Send prompts to local LLMs and print responses.
- **Prompt Templates:** Format prompts for creative tasks (e.g., poetry).
- **RAG:** Load and chunk PDFs, answer questions using document context.
- **Agent Tools & APIs:** Use prompt engineering to interact with external APIs (Google Search, Slack, Weather).

## How to Use
1. Open any notebook in `langchain-ollama/` (e.g., `1. Langchain_Basics.ipynb`).
2. Run each cell block-by-block in Jupyter for interactive learning.
3. See `instructions.ipynb` for a summary and sample code for all major concepts.

## Sample Ollama Usage
```python
import ollama
response = ollama.chat(model="llama2", messages=[{"role": "user", "content": "What is the capital of France?"}])
print(response["message"]["content"])
```

## Notebooks
- `1. Langchain_Basics.ipynb`: Getting started, basic prompts
- `2. Langchain_Temperatures.ipynb`: Temperature effects
- `3. Langchain_Prompt_Template.ipynb`: Prompt templates
- `4. Langchain_Agent_Tools_Weather.ipynb`: Weather agent tools
- `5. Langchain_Rag.ipynb`: RAG concepts
- `6. Resume_RAG_Agent_Lab.ipynb`: Resume RAG agent
- `8. Project1 - Connecting_AI_agents_to_external_APIs_(Google_Search).ipynb`: API integration
- `9. Project2 - weather_to_slack_agent.ipynb`: Slack agent
- `instructions.ipynb`: Concepts & sample code

---
For more details, see the individual notebooks and scripts in `langchain-ollama/`.

## Security & Best Practices
- **Never commit `.env` files with real API keys.**
- Use `.env.example` for sharing config templates.
- Review and follow lab instructions for safe API usage.

---

## References
- [LangChain Documentation](https://python.langchain.com/docs/)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [Model Context Protocol (MCP)](https://modelcontextprotocol.org/)
- [LangGraph](https://langchain-ai.github.io/langgraph/)

---

## Contact & Support
For questions, open an issue or contact the repository owner.

---

This README is your one-stop starting point for GenAI coding. Explore, experiment, and build powerful AI solutions!
