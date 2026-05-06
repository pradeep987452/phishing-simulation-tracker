from flask import Blueprint, request, jsonify
from services.groq_client import analyze_text
from datetime import datetime
from pathlib import Path

recommend_bp = Blueprint('recommend', __name__)

PROMPTS_DIR = Path(__file__).resolve().parent.parent / "prompts"

def load_prompt(user_input):
    with open(PROMPTS_DIR / "recommend_prompt.txt", "r", encoding="utf-8") as f:
        template = f.read()
    return template.replace("{input}", user_input)


def parse_input_data():
    data = request.get_json(silent=True)
    if data is None:
        if request.form.get("input"):
            data = {"input": request.form.get("input")}
        elif request.data:
            raw_body = request.data.decode("utf-8", errors="ignore").strip()
            if raw_body:
                data = {"input": raw_body}
    return data


@recommend_bp.route('/recommend', methods=['POST'])
def recommend():
    data = parse_input_data()

    if not data or "input" not in data:
        return jsonify({"error": "Input is required"}), 400

    user_input = data["input"].strip()

    if not user_input:
        return jsonify({"error": "Input cannot be empty"}), 400

    prompt = load_prompt(user_input)

    ai_result = analyze_text(prompt, user_input)

    if ai_result["is_fallback"]:
        return jsonify({
            "is_fallback": True,
            "recommendations": [],
            "generated_at": datetime.utcnow().isoformat()
        })

    return jsonify({
        "is_fallback": False,
        "recommendations": ai_result["content"],
        "generated_at": datetime.utcnow().isoformat()
    })