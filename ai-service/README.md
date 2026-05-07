# Phishing Simulation Tracker
# AI Service — Phishing Simulation Tracker

AI microservice for Tool-139 Phishing Simulation Tracker.

Built with:
- Flask
- Groq API (LLaMA 3.3 70B)
- Redis caching
- Docker

Runs on:
- Port: 5000

---

# Features

- AI phishing description generation
- AI security recommendations
- AI report generation
- Redis response caching
- Rate limiting
- Prompt injection protection
- Health monitoring endpoint
- Fallback responses on AI failure

---

# Project Structure

```bash
ai-service/
│── routes/
│   ├── describe.py
│   ├── recommend.py
│   ├── report.py
│   └── health.py
│
│── services/
│   ├── groq_client.py
│   └── cache.py
│
│── prompts/
│   ├── describe_prompt.txt
│   ├── recommend_prompt.txt
│   └── report_prompt.txt
│
│── app.py
│── requirements.txt
│── Dockerfile
│── .env.example
│── README.md
```

---

# Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
REDIS_HOST=redis
REDIS_PORT=6379
FLASK_ENV=development
```

---

# Setup Instructions

## 1. Clone Repository

```bash
git clone <your-repo-url>
cd ai-service
```

---

## 2. Create Virtual Environment

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Mac/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Run Flask Server

```bash
python app.py
```

Server runs at:

```text
http://localhost:5000
```

---

# Docker Setup

## Build Container

```bash
docker build -t ai-service .
```

## Run Container

```bash
docker run -p 5000:5000 ai-service
```

---

# API Endpoints

---

## GET /health

Health check endpoint.

### Response

```json
{
  "status": "healthy",
  "model": "llama-3.3-70b-versatile",
  "uptime_seconds": 120,
  "avg_response_time_ms": 842
}
```

---

## POST /describe

Generates phishing email description.

### Request

```json
{
  "content": "You won a free iPhone click here now"
}
```

### Response

```json
{
  "description": "Suspicious phishing-style message using urgency and fake rewards.",
  "generated_at": "2026-05-07T12:00:00",
  "is_fallback": false
}
```

---

## POST /recommend

Generates security recommendations.

### Request

```json
{
  "content": "Click here to verify your bank account immediately"
}
```

### Response

```json
[
  {
    "action_type": "warning",
    "description": "Avoid clicking unknown links.",
    "priority": "high"
  }
]
```

---

## POST /generate-report

Generates structured phishing analysis report.

### Request

```json
{
  "content": "Urgent account suspension notice"
}
```

### Response

```json
{
  "title": "Phishing Risk Report",
  "summary": "High-risk phishing attempt detected.",
  "overview": "The message uses urgency and impersonation tactics.",
  "key_items": [
    "Urgency language",
    "Suspicious request"
  ],
  "recommendations": [
    "Do not click links",
    "Verify sender identity"
  ]
}
```

---

# Security Features

- Rate limiting (30 req/min)
- Input validation
- Prompt injection protection
- HTML sanitization
- Redis caching
- Fallback response handling

---

# Running Tests

```bash
pytest
```

---

# Common Errors

## Redis Connection Error

Ensure Redis container is running:

```bash
docker ps
```

---

## Invalid Groq API Key

Check:

```env
GROQ_API_KEY=
```

inside `.env`

---

# Tech Stack

- Python 3.11
- Flask
- Redis
- Groq API
- Docker

---

# Author

AI Developer 1 — Tool-139 Capstone Project