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
