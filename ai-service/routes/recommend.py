import json

from flask import Blueprint, request, jsonify
from datetime import datetime
from pathlib import Path

from services.groq_client import analyze_text
from services.cache import (
    generate_cache_key,
    get_cached_response,
    set_cached_response
)

recommend_bp = Blueprint("recommend", __name__)

# 📁 Load prompt
PROMPTS_DIR = Path(__file__).resolve().parent.parent / "prompts"

with open(PROMPTS_DIR / "recommend_prompt.txt", "r", encoding="utf-8") as f:
    prompt_template = f.read()


@recommend_bp.route("/recommend", methods=["POST"])
def recommend():

    data = request.get_json()

    # ✅ Validation
    if not data or "content" not in data:
        return jsonify({
            "error": "Missing 'content' field"
        }), 400

    input_text = data["content"].strip()

    if len(input_text) == 0:
        return jsonify({
            "error": "Content cannot be empty"
        }), 400

    # ⚡ Generate cache key
    cache_key = generate_cache_key(input_text)

    # ⚡ Check Redis cache
    cached_response = get_cached_response(cache_key)

    if cached_response:
        print("⚡ Recommend Cache HIT")
        return jsonify(cached_response), 200

    print("🧠 Recommend Cache MISS")

    try:

        # 🔥 AI Call
        result = analyze_text(
            prompt_template,
            input_text
        )

        clean_text = result["content"]

        # ✅ Try parsing JSON
        try:

            parsed = json.loads(clean_text)

            if not isinstance(parsed, list):
                parsed = [parsed]

        except Exception:

            parsed = [
                {
                    "action_type": "general",
                    "description": clean_text,
                    "priority": "medium"
                }
            ]

        response = {
            "recommendations": parsed,
            "generated_at": datetime.utcnow().isoformat(),
            "is_fallback": result["is_fallback"]
        }

        # ⚡ Save cache
        set_cached_response(
            cache_key,
            response
        )

        print("✅ Recommend response cached")

        return jsonify(response), 200

    except Exception as e:

        print("Recommend Route Error:", e)

        fallback_response = {
            "recommendations": [
                {
                    "action_type": "fallback",
                    "description": "Unable to generate recommendations",
                    "priority": "low"
                }
            ],
            "generated_at": datetime.utcnow().isoformat(),
            "is_fallback": True
        }

        set_cached_response(
            cache_key,
            fallback_response
        )

        return jsonify(fallback_response), 200