import redis
import json

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def check_logs():
    print("Fetching last 5 logs from Redis...")
    logs = r.lrange("login_logs", 0, 4)
    if not logs:
        print("No logs found.")
        return
    
    for log in logs:
        print(json.loads(log))

if __name__ == "__main__":
    check_logs()
