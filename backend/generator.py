import os
from openai import OpenAI
from dotenv import load_dotenv
from rag import search_employees_rag

load_dotenv()

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.getenv("HF_API_KEY"),
)


def is_search_query(query: str) -> bool:
    """
    Returns True if the query looks like a search or employee filter request.
    """
    keywords = [
        "find", "search", "who", "available", "suggest", "looking for",
        "need", "developer", "engineer", "project", "skills", "experience",
        "worked on", "recommend"
    ]
    return any(keyword in query.lower() for keyword in keywords)

def generate_response(query: str) -> str:
    matches = search_employees_rag(query)
    
    if not matches:
        return "I couldn't find any matching employees for that request."

    if not is_search_query(query):
        return "Hi there! I'm your HR assistant. Ask me something like:\n- Find Python developers\n- Who is available next week?\n- Recommend someone for a healthcare project."

    # Construct context
    context_blocks = []
    for emp, text in matches:
        context_blocks.append(f"- {text}")
    
    context_text = "\n".join(context_blocks)
    
    # Final prompt to LLM
    prompt = f"""You are an intelligent HR assistant helping to find employees for various projects.

User Query: {query}
If the query is not about hiring or allocation, respond normally without trying to search.

Here are some employee profiles that may match:

{context_text}

Based on the above, recommend suitable candidates and explain why they match."""
    
    # Send to OpenAI Chat model
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b:cerebras",
        messages=[
            {"role": "system", "content":  (
                "You are an expert HR assistant specializing in candidate recommendations. "
                "Your responses should be:\n"
                "- Professional yet conversational\n"
                "- Focused on matching candidates to specific requirements\n"
                "- Clear about your reasoning (skills match, experience level, availability)\n"
                "- Honest about limitations or gaps\n\n"
                
                "Response format:\n"
                "1. Lead with your top recommendation and key reasons\n"
                "2. Briefly mention 1-2 alternative candidates if relevant\n"
                "3. Highlight any concerns or missing information\n"
                "4. Keep responses concise (2-3 paragraphs max unless comparison requested)\n\n"
                
                "Avoid generic responses. Always reference specific skills, experience, and availability from the data provided."
                "If the query is not about hiring or allocation, respond normally without trying to search."
            )},
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
        max_tokens=2000
    )
    
    return response.choices[0].message.content.strip()