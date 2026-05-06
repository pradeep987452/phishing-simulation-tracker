import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def analyze_text(prompt_template, input_text):
    final_prompt = prompt_template.replace("{input_text}", input_text).replace("{input}", input_text)

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": final_prompt}],
            temperature=0.3
        )

        content = response.choices[0].message.content
        return {
            "is_fallback": False,
            "content": content.strip() if isinstance(content, str) else content
        }

    except Exception as e:
        print("Groq Error:", e)
        return {
            "is_fallback": True,
            "message": "AI service temporarily unavailable"
        }
    
    from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def generate_response(prompt):

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

        return completion.choices[0].message.content

    except Exception as e:
        print("Groq Error:", e)
        return None