from sentence_transformers import SentenceTransformer, util
from data import employees

model = SentenceTransformer("all-MiniLM-L6-v2")

def search_employees(query: str):
    employee_texts = [
        f"{e['name']} {' '.join(e['skills'])} {e['experience_years']} years {' '.join(e['projects'])}"
        for e in employees
    ]
    query_embedding = model.encode(query, convert_to_tensor=True)
    employee_embeddings = model.encode(employee_texts, convert_to_tensor=True)

    scores = util.pytorch_cos_sim(query_embedding, employee_embeddings)[0]
    top_k = min(5, len(scores))
    top_indices = scores.argsort(descending=True)[:top_k]

    return [employees[i] for i in top_indices]
