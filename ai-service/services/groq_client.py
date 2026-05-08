import os
import time
from groq import Groq
from dotenv import load_dotenv
from typer import prompt
from services.chroma_service import search_knowledge

from services.cache import (
    get_cached_response,
    set_cached_response
)

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# Store response times for /health
response_times = []


def ask_groq(prompt, fallback_message="AI service temporarily unavailable"):

    # ✅ Check Redis cache first
    cached = get_cached_response(prompt)

    if cached:
        print("⚡ Cache hit")

        return {
            "content": cached,
            "is_fallback": False
        }

    print("❌ Cache miss")

    # ✅ Search knowledge from ChromaDB
    knowledge = search_knowledge(prompt)

    context = "\n".join(knowledge)

    final_prompt = f"""
Context:
{context}

User Input:
{prompt}
"""

    start_time = time.time()

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": final_prompt
                }
            ],
            temperature=0.3,
            max_tokens=300,
            timeout=10
        )

        result = completion.choices[0].message.content.strip()

        # ✅ Track response time
        elapsed = round(time.time() - start_time, 2)
        response_times.append(elapsed)

        # keep last 20 only
        if len(response_times) > 20:
            response_times.pop(0)

        # ✅ Save to Redis
        set_cached_response(prompt, result)

        print(f"✅ Saved to cache ({elapsed}s)")

        return {
            "content": result,
            "is_fallback": False
        }

    except Exception as e:
        print("Groq Error:", e)

        return {
            "content": fallback_message,
            "is_fallback": True
        }


def analyze_text(prompt, user_input=None, fallback_message="AI service temporarily unavailable"):
    return ask_groq(prompt, fallback_message)
