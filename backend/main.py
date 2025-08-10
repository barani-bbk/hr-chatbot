from fastapi import FastAPI, Query
from pydantic import BaseModel
from search import search_employees
from generator import generate_response
from data import employees
from typing import List, Optional

class ChatQuery(BaseModel):
    query: str

app = FastAPI()



@app.get("/employees/search")
def search_employees(
    skills: Optional[List[str]] = Query(None),
    experience: Optional[int] = None,
    availability: Optional[str] = None
):
    result = employees

    if skills:
        result = [e for e in result if any(skill.lower() in [s.lower() for s in e["skills"]] for skill in skills)]
    if experience is not None:
        result = [e for e in result if e["experience_years"] >= experience]
    if availability:
        result = [e for e in result if e["availability"].lower() == availability.lower()]

    return {"employees": result}

@app.post("/chat")
async def chat(query: ChatQuery):
    results = search_employees(query.query)
    response = generate_response(query.query, results)
    return {"results": results, "response": response}


