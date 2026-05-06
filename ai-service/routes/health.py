from flask import Blueprint, jsonify
import time

health_bp = Blueprint("health", __name__)

# ⏱ track when service started
start_time = time.time()

# 📊 simple metrics (optional but useful)
request_count = 0

@health_bp.route("/health", methods=["GET"])
def health():
    global request_count

    uptime = time.time() - start_time

    return jsonify({
        "status": "ok",
        "service": "ai-service",
        "uptime_seconds": round(uptime, 2),
        "requests_handled": request_count,
        "model": "groq-llama",
        "message": "AI service running smoothly"
    }), 200