from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
from data import employees


# Load model (do this once)
model = SentenceTransformer("all-MiniLM-L6-v2")

# Step 1: Convert employee profiles into text chunks
def format_employee(emp):
    return f"{emp['name']} is experienced in {', '.join(emp['skills'])}, has {emp['experience_years']} years of experience, and has worked on {', '.join(emp['projects'])}. Currently {emp['availability']}."

# Step 2: Generate embeddings
employee_texts = [format_employee(emp) for emp in employees]
employee_embeddings = model.encode(employee_texts, convert_to_numpy=True)

# Dimensions of the embedding vector
embedding_dim = employee_embeddings.shape[1]

# Build a FAISS index
index = faiss.IndexFlatL2(embedding_dim)
index.add(employee_embeddings)


def search_employees_rag(query: str, top_k=5):
    query_embedding = model.encode([query], convert_to_numpy=True)
    distances, indices = index.search(query_embedding, top_k)
    results = []
    for idx in indices[0]:
        emp = employees[idx]
        emp_text = employee_texts[idx]
        results.append((emp, emp_text))
    return results


