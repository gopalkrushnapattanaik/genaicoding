"""
Ollama Resume RAG Agent
- Loads a resume from PDF and splits into chunks
- Embeds and indexes with FAISS
- Uses Ollama for LLM responses
- Twilio SMS tool for notifications
"""

import os
from dotenv import load_dotenv
from twilio.rest import Client
from langchain.tools import Tool
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
import ollama

load_dotenv()
ollama_model = os.getenv("OLLAMA_MODEL", "llama2")

# Twilio credentials
sid = os.getenv("TWILIO_ACCOUNT_SID")
token = os.getenv("TWILIO_AUTH_TOKEN")
from_num = os.getenv("TWILIO_FROM_NUMBER")
to_num = os.getenv("TWILIO_TO_NUMBER")
twilio_client = Client(sid, token)

def send_sms_tool(message: str) -> str:
    twilio_client.messages.create(body=message, from_=from_num, to=to_num)
    return "SMS sent to your phone."

twilio_tool = Tool(
    name="twilio_tool",
    func=send_sms_tool,
    description="If you ever answer 'I don't know based on my resume.', immediately use this tool to notify the user by SMS. When you use this tool, send the original interview question that was asked, not the fallback answer."
)

pdf_path = "my_resume.pdf"
loader = PyPDFLoader(pdf_path)
docs = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
split_docs = text_splitter.split_documents(docs)
vectorstore = FAISS.from_documents(split_docs, embedding=None)
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

def resume_search_tool(query: str) -> str:
    # Simple semantic search
    docs = retriever.get_relevant_documents(query)
    context = "\n".join([doc.page_content for doc in docs])
    prompt = f"Answer the following interview question using only the resume context below. If not found, say 'I don't know based on my resume.'\nResume:\n{context}\nQuestion: {query}"
    response = ollama.chat(model=ollama_model, messages=[{"role": "user", "content": prompt}])
    answer = response["message"]["content"]
    if "I don't know" in answer:
        send_sms_tool(query)
    return answer

resume_tool = Tool(
    name="resume_search",
    func=resume_search_tool,
    description="Use this tool to search the resume and answer interview questions based on its content. If the answer is not found, return 'I don't know based on my resume.' as a string. If you ever answer 'I don't know based on my resume.', you must immediately use the twilio_tool to notify the user by SMS."
)

print("Resume RAG Chatbot (Ollama Agent). Type your interview question (or 'exit' to quit):")
while True:
    question = input("You: ")
    if question.lower() == "exit":
        break
    print("Bot:", resume_search_tool(question))
