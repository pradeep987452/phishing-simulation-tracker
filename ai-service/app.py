from flask import Flask, jsonify, request
from flask_talisman import Talisman
from services.embedding_service import load_embedding_model

# ✅ import blueprints
from routes.describe import describe_bp
from routes.recommend import recommend_bp
from routes.report import report_bp

app = Flask(__name__)

# ✅ Security headers using Flask-Talisman
Talisman(
    app,
    content_security_policy={
        "default-src": "'self'",
        "script-src": "'self'",
        "style-src": "'self'",
        "img-src": "'self' data:",
        "object-src": "'none'",
        "base-uri": "'self'"
    }
)

# ✅ register blueprints
app.register_blueprint(describe_bp)
app.register_blueprint(recommend_bp)
app.register_blueprint(report_bp)

# ✅ root route
@app.route("/")
def home():
    return {"message": "AI Service Running 🚀"}

# ✅ health endpoint
@app.route("/health")
def health():
    return {
        "status": "ok",
        "service": "ai-service",
        "version": "1.0"
    }

# ✅ global error handler
@app.errorhandler(500)
def handle_500(e):
    return jsonify({
        "error": "Internal server error",
        "is_fallback": True
    }), 500

# ✅ handle bad requests
@app.errorhandler(400)
def handle_400(e):
    return jsonify({
        "error": "Bad request",
        "message": str(e)
    }), 400

# ✅ request logging
@app.before_request
def log_request():
    print(f"[{request.method}] {request.path}")

# ✅ add extra security headers
@app.after_request
def set_security_headers(response):

    # Hide Flask/Werkzeug info
    response.headers["Server"] = "SecureServer"

    # Prevent MIME sniffing
    response.headers["X-Content-Type-Options"] = "nosniff"

    # Prevent clickjacking
    response.headers["X-Frame-Options"] = "DENY"

    # Restrict referrer info
    response.headers["Referrer-Policy"] = "no-referrer"

    # Disable browser permissions
    response.headers["Permissions-Policy"] = "geolocation=()"

    return response

# 🚀 run app
if __name__ == "__main__":
    print(app.url_map)
    load_embedding_model()
    app.run(host="0.0.0.0", port=5000, debug=True)
