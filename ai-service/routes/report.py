from flask import Blueprint, request, jsonify
from datetime import datetime
from services.groq_client import generate_response

report_bp = Blueprint("report", __name__)

@report_bp.route("/generate-report", methods=["POST"])
def generate_report():

    data = request.get_json()

    # ✅ Validation
    if not data or "content" not in data:
        return jsonify({"error": "Missing 'content' field"}), 400

    content = data["content"].strip()

    if len(content) == 0:
        return jsonify({"error": "Content cannot be empty"}), 400

    # ✅ Prompt
    prompt = f"""
    Analyze the following phishing-related content and generate a security report.

    Content:
    {content}

    Return JSON with:
    - title
    - summary
    - overview
    - key_items (array)
    - recommendations (array)
    """

    # ✅ AI Call
    response = generate_response(prompt)

    # ✅ Fallback
    if not response:
        return jsonify({
            "title": "Fallback Report",
            "summary": "Unable to generate AI report.",
            "overview": "Fallback response triggered.",
            "key_items": [],
            "recommendations": [],
            "generated_at": datetime.utcnow().isoformat(),
            "is_fallback": True
        })

    # ✅ Final Response
    return jsonify({
        "report": response,
        "generated_at": datetime.utcnow().isoformat(),
        "is_fallback": False
    })