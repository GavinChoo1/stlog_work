import redis
import json
import time
from .connections import pg_db, redis_conn




################ 
# Log to redis
################ 
def log_event_to_redis(username, ret):
    """Logs a login event (success/fail/error) to a Redis list."""
    r = redis_conn()
    log_entry = {
        "timestamp": int(time.time()),
        "username": username,
        "ret": ret
    }
    r.lpush("login_logs", json.dumps(log_entry))
    r.ltrim("login_logs", 0, 99)





############################################################################
# Authentication check
############################################################################
def auth_check(username, password):
    connection = None
    try:
        connection = pg_db()
        cursor = connection.cursor()

        # 1. Check if username exists
        cursor.execute("SELECT password_hash FROM hls_db.account.users WHERE username = %s;", (username,))
        row = cursor.fetchone()

        if row is None:
            log_event_to_redis(username, 1001)
            return False
        
        # 2. Check if password matches
        db_password = row[0]
        if db_password == password:
            # Both correct
            log_event_to_redis(username, 0)
            return True
        else:
            log_event_to_redis(username, 1002)
            return False


    except Exception as error:
        print(f"Error connecting to Postgres: {error}")
        log_event_to_redis(username, f"Error: Database issue - {str(error)}")
        return None  # Indicate database error

    finally:
        if connection:
            cursor.close()
            connection.close()
