import os
from groq import Groq
from dotenv import load_dotenv

# Load env variables
load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Load prompt
with open("prompts/describe_prompt.txt", "r") as f:
    prompt_template = f.read()

# Test input
input_text = "Click here to win money"

# Replace placeholder
final_prompt = prompt_template.replace("{input_text}", input_text)

# Call API
response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[{"role": "user", "content": final_prompt}],
    temperature=0.3
)

print(response.choices[0].message.content)