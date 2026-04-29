import redis
import psycopg2
import json
from datetime import datetime

# Connect to your Docker Redis
def redis_conn(host='localhost', port=6379):
    redis_conn = redis.Redis(host=host, port=port, decode_responses=True)
    return redis_conn



def pg_db():
    connection = psycopg2.connect(
        user="admin",
        password="admin123",
        host="127.0.0.1",
        port="5432",
        database="hls_db"
    )
    return connection

