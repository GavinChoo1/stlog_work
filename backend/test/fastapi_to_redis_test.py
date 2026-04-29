import redis

# Connect to your Docker Redis
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def save_to_redis(key, value):
    # This ensures EVERY save is forced to 60 seconds
    r.set(key, value, ex=60)
