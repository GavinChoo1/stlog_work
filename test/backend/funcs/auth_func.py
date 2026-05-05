import redis
import json
import time
from .connections import pg_db, redis_conn




################ 
# Log to redis
################ 
import json
import time

def log_event_to_redis(username, ret):
    """Logs a login event to a Redis Stream with automatic capping."""
    r = redis_conn()
    
    log_entry = {
        "timestamp": str(int(time.time())),
        "username": username,
        "ret": ret
    }
    
    # XADD parameters:
    # name: "login_stream"
    # id: "*" (Auto-generate timestamp ID)
    # fields: the dictionary
    # maxlen: 100 (Keep roughly the last 100 entries)
    # approximate: True (Uses '~' for better performance)
    r.xadd("login_stream", log_entry, maxlen=100, approximate=True)




############################################################################
# Authentication check
############################################################################
def auth_check(username, password):
    connection = None
    try:
        connection = pg_db()
        cursor = connection.cursor()

        # 1. Check if username exists
        cursor.execute("SELECT password_hash FROM hls_db.accounts.users WHERE username = %s;", (username,))
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
        log_event_to_redis(username, 1000)
        return None  # Indicate database error

    finally:
        if connection:
            cursor.close()
            connection.close()

############################################################################
# Reset password
############################################################################
def reset_password_in_db(username, new_password):
    connection = None
    try:
        connection = pg_db()
        cursor = connection.cursor()

        # 1. Check if username exists
        cursor.execute("SELECT 1 FROM hls_db.accounts.users WHERE username = %s;", (username,))
        if cursor.fetchone() is None:
            return False, "Username not found"

        # 2. Update password
        cursor.execute(
            "UPDATE hls_db.accounts.users SET password_hash = %s WHERE username = %s;",
            (new_password, username)
        )
        connection.commit()
        
        # Log the event
        log_event_to_redis(username, 2000) # 2000 for password reset success
        return True, "Password reset successful"

    except Exception as error:
        print(f"Error resetting password: {error}")
        return False, "Database error"

    finally:
        if connection:
            cursor.close()
            connection.close()
