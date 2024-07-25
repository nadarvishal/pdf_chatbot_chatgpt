import os
import openai
import faiss
import numpy as np
from PyPDF2 import PdfReader
from langchain_community.embeddings import OpenAIEmbeddings

# Ensure you have your OpenAI API key set in an environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

from openai import OpenAI
client = OpenAI()

# Initialize FAISS index
dimension = 1536
index = faiss.IndexFlatL2(dimension)

# Mapping from index to text
index_to_text = {}

def extract_text_from_pdf(file) -> str:
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def index_pdf_content(text: str):
    paragraphs = text.split('\n')
    embeddings = OpenAIEmbeddings().embed_documents(paragraphs)
    for i, emb in enumerate(embeddings):
        index.add(np.array([emb], dtype=np.float32))
        index_to_text[index.ntotal - 1] = paragraphs[i]

def retrieve_relevant_content(query: str, top_n: int = 3) -> str:
    query_embedding = OpenAIEmbeddings().embed_query(query)
    D, I = index.search(np.array([query_embedding], dtype=np.float32), top_n)
    relevant_content = "\n".join([index_to_text[i] for i in I[0] if i in index_to_text])
    return relevant_content

def generate_response(query: str) -> str:
    retrieved_content = retrieve_relevant_content(query)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an assistant that answers questions based on the provided content."},
            {"role": "user", "content": f"Context: {retrieved_content}\n\nQuestion: {query}\nAnswer:"}
        ],
        max_tokens=150
    )
    answer = response.choices[0].message.content
    return answer

