import redis
import json

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def check_logs():
    print("Fetching last 5 logs from Redis Stream (login_stream)...")
    # XADD stores entries in a stream, so we use xrevrange to get the latest ones
    logs = r.xrevrange("login_stream", count=10)
    
    if not logs:
        print("No logs found in 'login_stream'.")
        # Check the old list just in case
        old_logs = r.lrange("login_logs", 0, 4)
        if old_logs:
            print(f"Found {len(old_logs)} logs in the old 'login_logs' list.")
        return
    
    for entry_id, fields in logs:
        print(f"ID: {entry_id} | Data: {fields}")

if __name__ == "__main__":
    check_logs()
