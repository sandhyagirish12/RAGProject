# app.py
import streamlit as st
import requests

API_URL = "http://localhost:8000"  # FastAPI backend

st.title("📄 Retrieval-Augmented Q&A with OpenAI")

# Upload documents
st.header("Upload a Document")
uploaded_file = st.file_uploader("Choose a text file", type=["txt"])
if uploaded_file is not None:
    try:
        files = {"file": uploaded_file.getvalue()}
        response = requests.post(f"{API_URL}/upload", files=files)
        response.raise_for_status()
        st.success(response.json()["message"])
    except requests.exceptions.RequestException as e:
        st.error(f"Upload failed: {str(e)}")

# Ask questions
st.header("Ask a Question")
question = st.text_input("Enter your question:")
if st.button("Submit") and question:
    try:
        payload = {"question": question}
        response = requests.post(f"{API_URL}/query", json=payload)
        response.raise_for_status()
        st.write("### Answer")
        st.write(response.json()["answer"])
    except requests.exceptions.RequestException as e:
        st.error(f"Query failed: {str(e)}")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
