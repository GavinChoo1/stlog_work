import redis
import json
import time
from .connections import pg_db, redis_conn




################ 
# Log to redis
################ 
def place_order_to_redis(username, order_details):
    r = redis_conn()
    
    # Data must be a flat dictionary (field-value pairs)
    order_entry = {
        "username": username,
        "item": order_details['item'],
        "amount": order_details['amount'],
        "status": "pending",
        "timestamp": int(time.time())
    }
    
    # id='*' tells Redis to auto-generate a unique time-based ID
    # maxlen=1000 keeps the buffer manageable
    order_id = r.xadd("orders_stream", order_entry, id='*', maxlen=1000, approximate=True)
    
    print(f"Order placed! Redis ID: {order_id}")
    return order_id



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
        cursor.execute("SELECT 1 FROM hls_db.account.users WHERE username = %s;", (username,))
        if cursor.fetchone() is None:
            return False, "Username not found"

        # 2. Update password
        cursor.execute(
            "UPDATE hls_db.account.users SET password_hash = %s WHERE username = %s;",
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
