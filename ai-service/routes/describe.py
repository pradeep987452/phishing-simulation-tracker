from flask import Blueprint, request, jsonify
from datetime import datetime
from pathlib import Path
from services.groq_client import analyze_text
from services.cache import generate_key, get_cached_response, set_cache
import json

# ✅ DEFINE BLUEPRINT FIRST (THIS FIXES YOUR ERROR)
describe_bp = Blueprint("describe", __name__)

# 📁 Load prompt
PROMPTS_DIR = Path(__file__).resolve().parent.parent / "prompts"

with open(PROMPTS_DIR / "describe_prompt.txt", "r", encoding="utf-8") as f:
    prompt_template = f.read()


# 🧠 Input parser (supports multiple formats)
def parse_input_data():
    data = request.get_json(silent=True)

    if data is None:
        if request.form.get("content"):
            data = {"content": request.form.get("content")}
        elif request.data:
            raw_body = request.data.decode("utf-8", errors="ignore").strip()
            if raw_body:
                data = {"content": raw_body}

    return data


# 🚀 MAIN ROUTE
@describe_bp.route("/describe", methods=["POST"])
def describe():
    data = parse_input_data()

    # ✅ Input validation
    if not data or "content" not in data:
        return jsonify({"error": "Missing 'content' field"}), 400

    input_text = data["content"].strip()

    if len(input_text) == 0:
        return jsonify({"error": "Text cannot be empty"}), 400

    # ⚡ STEP 1: Cache key
    cache_key = generate_key(input_text)

    # ⚡ STEP 2: Check cache
    cached_response = get_cached_response(cache_key)
    if cached_response:
        print("⚡ Cache HIT")
        return jsonify(cached_response), 200

    print("🧠 Cache MISS")

    try:
        # 🔥 Call AI
        result = analyze_text(prompt_template, input_text)

        # 🧹 Clean result
        if isinstance(result, dict) and "content" in result:
            clean_text = result["content"]
        else:
            clean_text = str(result)

        try:
            parsed = json.loads(clean_text)
            clean_text = parsed.get("reason", clean_text)
        except Exception:
            pass

        response = {
            "description": clean_text,
            "generated_at": datetime.utcnow().isoformat(),
            "is_fallback": False
        }

        # ⚡ STEP 3: Store cache
        set_cache(cache_key, response)

        return jsonify(response), 200

    except Exception:
        fallback_response = {
            "description": "Unable to generate AI description",
            "generated_at": datetime.utcnow().isoformat(),
            "is_fallback": True
        }

        set_cache(cache_key, fallback_response)

        return jsonify(fallback_response), 200