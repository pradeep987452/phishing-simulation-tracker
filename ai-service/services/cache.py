import redis
import hashlib
import json

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

def generate_key(text):
    return hashlib.sha256(text.encode()).hexdigest()

def get_cached_response(key):
    data = r.get(key)
    return json.loads(data) if data else None

def set_cache(key, value, ttl=900):  # 15 min
    r.setex(key, ttl, json.dumps(value))