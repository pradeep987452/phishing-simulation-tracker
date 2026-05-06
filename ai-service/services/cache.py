import redis
import hashlib
import json

redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

CACHE_TTL = 900  # 15 minutes


def generate_cache_key(text):
    return hashlib.sha256(text.encode()).hexdigest()


def get_cached_response(text):

    key = generate_cache_key(text)

    cached = redis_client.get(key)

    if cached:
        return json.loads(cached)

    return None


def set_cached_response(text, response):

    key = generate_cache_key(text)

    redis_client.setex(
        key,
        CACHE_TTL,
        json.dumps(response)
    )