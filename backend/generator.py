import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.getenv("HF_API_KEY"),
)

def generate_response(query: str, employees: list):
    lowered = query.lower().strip()
    greetings = {"hi", "hello", "hey", "good morning", "good evening", "good afternoon"}
    if any(word in lowered for word in greetings) or len(lowered) < 10:
        return (
            "Hello! I'm your HR assistant. You can ask me things like:\n"
            "- Who is a good fit for a frontend developer role?\n"
            "- Recommend someone with Java + Spring experience.\n"
            "- Who is available for a project starting next week?\n"
        )

    if not employees:
        return "No matching employees found."

    context = "\n".join([
        f"{e['name']}, Skills: {', '.join(e['skills'])}, Experience: {e['experience_years']} yrs, Projects: {', '.join(e['projects'])}, Availability: {e['availability']}"
        for e in employees
    ])


    messages = [
        {
            "role": "system",
            "content": (
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
            )
        },
        {
            "role": "user",
            "content": (
                f"I am looking for someone for this role: {query}.\n"
                "Here are some employees that might be relevant:\n"
                f"{context}\n\n"
                "Which of these candidates would you recommend and why?"
            ),
        },
    ]

    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b:cerebras",
            messages=messages,
            temperature=0.3,
            max_tokens=2000,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}"
