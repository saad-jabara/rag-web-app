"""
RAG Web Application - Basecamp Employee Handbook RAG System with Web Interface
"""

import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.embeddings.base import Embeddings
from typing import List
import openai
import logging

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variables for RAG chain
qa_chain = None
vectorstore = None
rag_initialized = False

# Verify OpenAI API key is set
if not os.getenv("OPENAI_API_KEY"):
    logger.warning("OPENAI_API_KEY not set - RAG will not work. Set it in environment variables.")


class CustomOpenAIEmbeddings(Embeddings):
    """Custom OpenAI Embeddings wrapper to avoid the proxies parameter issue"""

    def __init__(self, model="text-embedding-ada-002"):
        self.model = model
        # Set API key for openai library (compatible with 1.12.0)
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed search docs."""
        embeddings = []
        for text in texts:
            # Use the older API format for openai 1.12.0
            response = openai.Embedding.create(
                model=self.model,
                input=text
            )
            embeddings.append(response['data'][0]['embedding'])
        return embeddings

    def embed_query(self, text: str) -> List[float]:
        """Embed query text."""
        # Use the older API format for openai 1.12.0
        response = openai.Embedding.create(
            model=self.model,
            input=text
        )
        return response['data'][0]['embedding']


def initialize_rag_system():
    """Initialize the RAG system (lazy-loaded on first request)"""
    global qa_chain, vectorstore, rag_initialized

    if rag_initialized:
        return True

    logger.info("Initializing RAG System (this may take 1-2 minutes on first request)...")

    try:
        if not os.getenv("OPENAI_API_KEY"):
            logger.error("OPENAI_API_KEY not set!")
            return False

        # Step 1: Load documents
        logger.info("Loading documents from Basecamp Employee Handbook...")
        basecamp_urls = [
            "https://basecamp.com/handbook",
            "https://basecamp.com/handbook/how-we-work",
            "https://basecamp.com/handbook/benefits-and-perks",
            "https://basecamp.com/handbook/work-life-balance",
            "https://basecamp.com/handbook/titles-for-support",
            "https://basecamp.com/handbook/getting-started",
            "https://basecamp.com/handbook/communication",
            "https://basecamp.com/handbook/our-internal-systems",
            "https://basecamp.com/handbook/pricing-and-profit",
            "https://basecamp.com/handbook/dei"
        ]

        loader = WebBaseLoader(basecamp_urls)
        documents = loader.load()
        logger.info(f"Loaded {len(documents)} documents")

        # Step 2: Split documents into chunks
        logger.info("Splitting documents into chunks...")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        chunks = text_splitter.split_documents(documents)
        logger.info(f"Created {len(chunks)} chunks")

        # Step 3: Create embeddings and vector store
        logger.info("Creating embeddings and building vector store...")
        embeddings = CustomOpenAIEmbeddings(model="text-embedding-ada-002")

        vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory="./chroma_db"
        )
        logger.info("Vector store created successfully")

        # Step 4: Setup retriever
        retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

        # Step 5: Setup LLM and QA chain
        logger.info("Setting up LLM and QA chain...")
        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

        prompt_template = """Use the following pieces of context from the Basecamp Employee Handbook to answer the question.
If you don't know the answer based on the context, just say that you don't know, don't try to make up an answer.

Context:
{context}

Question: {question}

Answer:"""

        PROMPT = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )

        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": PROMPT}
        )

        rag_initialized = True
        logger.info("RAG System initialized successfully!")
        return True

    except Exception as e:
        logger.error(f"Error initializing RAG system: {str(e)}")
        return False


@app.route("/")
def index():
    """Render the main page"""
    return render_template("index.html")


@app.route("/api/query", methods=["POST"])
def query():
    """Handle RAG queries via API"""
    try:
        data = request.json
        question = data.get("question", "").strip()

        if not question:
            return jsonify({"error": "Question cannot be empty"}), 400

        # Initialize RAG system if not already done (lazy loading)
        if not rag_initialized:
            logger.info("First query received - initializing RAG system...")
            if not initialize_rag_system():
                return jsonify({
                    "error": "Failed to initialize RAG system. Check that OPENAI_API_KEY is set.",
                    "status": "error"
                }), 500

        if qa_chain is None:
            return jsonify({
                "error": "RAG system initialization failed",
                "status": "error"
            }), 500

        logger.info(f"Processing question: {question}")
        result = qa_chain.invoke({"query": question})

        # Format source documents
        sources = []
        for doc in result.get("source_documents", []):
            sources.append({
                "source": doc.metadata.get("source", "Unknown"),
                "content": doc.page_content[:300] + "..."
            })

        response = {
            "answer": result.get("result", ""),
            "sources": sources,
            "status": "success"
        }

        return jsonify(response)

    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        return jsonify({"error": str(e), "status": "error"}), 500


@app.route("/api/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "rag_system": "initialized" if rag_initialized else "not_initialized_yet",
        "message": "App is running. RAG will initialize on first query."
    })


if __name__ == "__main__":
    logger.info("Starting Flask application...")
    logger.info("RAG system will initialize on first query (lazy loading)")
    app.run(debug=True, host="0.0.0.0", port=5000)
