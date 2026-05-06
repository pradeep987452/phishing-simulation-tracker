from flask import Flask, jsonify, request

# ✅ import blueprints
from routes.describe import describe_bp
from routes.recommend import recommend_bp
from routes.report import report_bp

app = Flask(__name__)

# ✅ register them
app.register_blueprint(describe_bp)
app.register_blueprint(recommend_bp)
app.register_blueprint(report_bp)

# ✅ root route (helps quick testing)
@app.route("/")
def home():
    return {"message": "AI Service Running 🚀"}

# ✅ health endpoint (used by Java + Docker later)
@app.route("/health")
def health():
    return {
        "status": "ok",
        "service": "ai-service",
        "version": "1.0"
    }

# ✅ global error handler (VERY IMPORTANT for Day 5)
@app.errorhandler(500)
def handle_500(e):
    return jsonify({
        "error": "Internal server error",
        "is_fallback": True
    }), 500

# ✅ optional: handle bad requests (clean JSON instead of HTML)
@app.errorhandler(400)
def handle_400(e):
    return jsonify({
        "error": "Bad request",
        "message": str(e)
    }), 400

# ✅ request logging (helps debug Java calls)
@app.before_request
def log_request():
    print(f"[{request.method}] {request.path}")

# 🚀 run app
if __name__ == "__main__":
    print(app.url_map)  # debug routes
    app.run(host="0.0.0.0", port=5000, debug=True)

