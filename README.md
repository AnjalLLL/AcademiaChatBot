# AcademiaChatBot
This is an AI-powered college inquiry chatbot built using LangChain, FAISS, and Local LLM (Ollama) that answers student queries based on scraped website data and supports human handoff.
Overview
This project implements a Retrieval-Augmented Generation (RAG) architecture to provide accurate, context-aware responses to student inquiries using real college website data.
The chatbot building process :
Scrapes college website content
Converts text into embeddin
Stores embeddings in FAISS vector database
Retrieves relevant context for user queries
Generates responses using an LLM

Technology Used 
Backend: Django / FastAPI
LLM Framework: LangChain
Vector Database: FAISS
Embedding Model: Ollama local model for testing
Web Scraping: Selenium
Frontend: HTML, CSS(Dummy frontend for testing)

