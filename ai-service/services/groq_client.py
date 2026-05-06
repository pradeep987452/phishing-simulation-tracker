import os
import time
from groq import Groq
from dotenv import load_dotenv

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


def ask_groq(prompt):

    # ✅ Check Redis cache first
    cached = get_cached_response(prompt)

    if cached:
        print("⚡ Cache hit")
        return cached

    print("❌ Cache miss")

    start_time = time.time()

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
            max_tokens=500
        )

        result = completion.choices[0].message.content

        # ✅ Track response time
        elapsed = time.time() - start_time
        response_times.append(elapsed)

        # ✅ Save to Redis
        set_cached_response(prompt, result)

        print("✅ Saved to cache")

        return result

    except Exception as e:
        print("Groq Error:", e)

        return None


# Optional compatibility function
def analyze_text(prompt_template, input_text):

    final_prompt = (
        prompt_template
        .replace("{input_text}", input_text)
        .replace("{input}", input_text)
    )

    response = ask_groq(final_prompt)

    if response:
        return {
            "is_fallback": False,
            "content": response.strip()
        }

    return {
        "is_fallback": True,
        "message": "AI service temporarily unavailable"
    }