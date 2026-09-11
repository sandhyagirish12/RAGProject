Retrieval‑Augmented Q&A with OpenAI
A lightweight prototype that lets users upload documents and ask questions. The system uses OpenAI GPT models with retrieval‑augmented generation (RAG) to ground answers in your own data.

🚀 Features
Upload text files and split them into chunks

Generate embeddings with OpenAI and store them in SQLite

Retrieve relevant chunks using similarity search

Ask questions and get GPT answers based on your documents

Simple Streamlit UI for upload + Q&A

🛠 Tech Stack
Backend: FastAPI + Uvicorn

Frontend: Streamlit

Database: SQLite

Libraries: OpenAI, LangChain, Pydantic, Requests, Pandas

Environment: Python 3.8+

📂 Project Structure
Code
openai-retrieval-qna/
│── main.py        # FastAPI backend
│── app.py         # Streamlit frontend
│── requirements.txt
│── README.md
│── documents.db   # SQLite database (auto-created)
⚙️ Setup
Clone the repo:

bash
git clone https://github.com/sandhyagirish12/RAGProject.git
cd RAGProject
Install dependencies:

bash
pip install -r requirements.txt
Set your OpenAI API key:

bash
export OPENAI_API_KEY="your_api_key"
Run the backend:

bash
uvicorn main:app --reload
Run the frontend:

bash
streamlit run app.py
📖 Usage
Upload a .txt file in the Streamlit app.

Ask a question in the input box.

The system retrieves relevant chunks and GPT generates an answer.

🔮 Future Improvements
Support for PDF uploads

Add vector database (e.g., Pinecone, Weaviate)

Authentication for multi‑user setups

Deployment on Vercel or Streamlit Cloud