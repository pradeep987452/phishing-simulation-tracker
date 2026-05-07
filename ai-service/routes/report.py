import json

from flask import Blueprint, request, jsonify
from datetime import datetime

from services.groq_client import ask_groq
from services.cache import (
    generate_cache_key,
    get_cached_response,
    set_cached_response
)

report_bp = Blueprint("report", __name__)


@report_bp.route("/generate-report", methods=["POST"])
def generate_report():

    data = request.get_json()

    # ✅ Validation
    if not data or "content" not in data:
        return jsonify({
            "error": "Missing 'content' field"
        }), 400

    content = data["content"].strip()

    if len(content) == 0:
        return jsonify({
            "error": "Content cannot be empty"
        }), 400

    # ⚡ Generate cache key
    cache_key = generate_cache_key(content)

    # ⚡ Check cache
    cached_response = get_cached_response(cache_key)

    if cached_response:
        print("⚡ Report Cache HIT")
        return jsonify(cached_response), 200

    print("🧠 Report Cache MISS")

    # ✅ Prompt
    prompt = f"""
    Analyze the following phishing-related content and generate a security report.

    Content:
    {content}

    Return ONLY valid JSON with:
    - title
    - summary
    - overview
    - key_items (array)
    - recommendations (array)

    Do not use markdown.
    """

    try:

        # 🔥 AI Call
        response = ask_groq(prompt)

        # ✅ Fallback from AI service
        if response.get("is_fallback", False):

            fallback_response = {
                "title": "Fallback Report",
                "summary": "Unable to generate AI report.",
                "overview": "Fallback response triggered.",
                "key_items": [],
                "recommendations": [],
                "generated_at": datetime.utcnow().isoformat(),
                "is_fallback": True
            }

            set_cached_response(
                cache_key,
                fallback_response
            )

            return jsonify(fallback_response), 200

        # ✅ Clean response
        cleaned = response.get("content", "")

        cleaned = cleaned.replace("```json", "")
        cleaned = cleaned.replace("```", "")
        cleaned = cleaned.strip()

        # ✅ Parse JSON
        report_json = json.loads(cleaned)

        final_response = {
            "report": report_json,
            "generated_at": datetime.utcnow().isoformat(),
            "is_fallback": False
        }

        # ⚡ Save cache
        set_cached_response(
            cache_key,
            final_response
        )

        return jsonify(final_response), 200

    except Exception as e:

        print("Report Route Error:", e)

        fallback_response = {
            "title": "Fallback Report",
            "summary": "Unable to generate valid JSON report.",
            "overview": "Fallback response triggered.",
            "key_items": [],
            "recommendations": [],
            "generated_at": datetime.utcnow().isoformat(),
            "is_fallback": True
        }

        set_cached_response(
            cache_key,
            fallback_response
        )

        return jsonify(fallback_response), 200