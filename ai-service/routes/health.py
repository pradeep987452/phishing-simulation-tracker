from flask import Blueprint, jsonify
import time

health_bp = Blueprint("health", __name__)

START_TIME = time.time()

response_times = []

@health_bp.route("/health", methods=["GET"])
def health():

    uptime = int(time.time() - START_TIME)

    avg_response = (
        sum(response_times) / len(response_times)
        if response_times else 0
    )

    return jsonify({
        "status": "healthy",
        "service": "ai-service",
        "model": "llama-3.3-70b-versatile",
        "uptime_seconds": uptime,
        "avg_response_time_ms": round(avg_response, 2),
        "cache": "connected"
    }), 200