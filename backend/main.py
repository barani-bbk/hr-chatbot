from fastapi import FastAPI, Query
from pydantic import BaseModel
from generator import generate_response
from rag import search_employees_rag
from data import employees
from typing import List, Optional

class ChatQuery(BaseModel):
    query: str

app = FastAPI()



@app.get("/employees/search")
def semantic_search_employees(
    skills: Optional[List[str]] = Query(None),
    experience: Optional[int] = None,
    availability: Optional[str] = None,
):
    query_parts = []

    if skills:
        query_parts.append(f"skills in {', '.join(skills)}")
    if experience is not None:
        query_parts.append(f"{experience}+ years of experience")
    if availability:
        query_parts.append(f"currently {availability}")

    query = "Find employees with " + " and ".join(query_parts) if query_parts else "Find all employees"

    matches = search_employees_rag(query)

    return {"employees": matches}


@app.post("/chat")
async def chat_endpoint(request: ChatQuery):
    try:
        response = generate_response(request.query)
        return {"response": response}
    except Exception as e:
        print(f"Error: {e}")
        return {"error": "Failed to fetch a proper response from the server."}



