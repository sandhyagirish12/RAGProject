# main.py
import os
import sqlite3
from openai import OpenAI
from fastapi import FastAPI, UploadFile
from pydantic import BaseModel
from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv

# Initialize FastAPI
app = FastAPI()

# Configure OpenAI
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Database setup (SQLite for persistence)
conn = sqlite3.connect("documents.db")
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS docs (id INTEGER PRIMARY KEY, content TEXT)")
conn.commit()

# Upload endpoint
@app.post("/upload")
async def upload_file(file: UploadFile):
    text = await file.read()
    text = text.decode("utf-8")

    # Split text into chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_text(text)

    # Store chunks in DB
    for chunk in chunks:
        cursor.execute("INSERT INTO docs (content) VALUES (?)", (chunk,))
    conn.commit()

    return {"message": "File uploaded and processed"}

# Query endpoint
class QueryRequest(BaseModel):
    question: str

@app.post("/query")
async def query_docs(request: QueryRequest):
    try:
        # Retrieve all chunks
        cursor.execute("SELECT content FROM docs")
        docs = [row[0] for row in cursor.fetchall()]
        
        if not docs:
            return {"answer": "No documents found. Please upload a document first."}

        # Create embeddings
        embeddings = OpenAIEmbeddings()
        vectorstore = Chroma.from_texts(docs, embeddings)

        # Retrieve relevant chunks
        relevant_docs = vectorstore.similarity_search(request.question, k=3)

        # Build context
        context = "\n".join([doc.page_content for doc in relevant_docs])

        # Ask GPT with context
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant answering based on provided context."},
                {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {request.question}"}
            ]
        )

        return {"answer": response.choices[0].message.content}
    except Exception as e:
        return {"error": str(e)}
