import os
import time
import json
import redis
from kafka import KafkaProducer

# Configuration from environment variables
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
# We now treat REDIS_STREAM as a pattern (e.g. 'events:*')
REDIS_STREAM_PATTERN = os.getenv('REDIS_STREAM', 'events:*')
REDIS_GROUP = os.getenv('REDIS_GROUP', 'bridge_group')
REDIS_CONSUMER = os.getenv('REDIS_CONSUMER', 'bridge_consumer_1')

KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
KAFKA_TOPIC = os.getenv('KAFKA_TOPIC', 'login_events')

def main():
    print(f"Connecting to Redis at {REDIS_HOST}:{REDIS_PORT}...")
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

    print(f"Connecting to Kafka at {KAFKA_BOOTSTRAP_SERVERS}...")
    producer = None
    while producer is None:
        try:
            producer = KafkaProducer(
                bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )
        except Exception as e:
            print(f"Waiting for Kafka... {e}")
            time.sleep(5)

    # Dictionary to track active streams and their current read ID
    # stream_name -> last_id
    active_streams = {}
    last_refresh = 0
    refresh_interval = 10  # Seconds between scanning for new streams

    print(f"Bridge started. Listening to pattern: {REDIS_STREAM_PATTERN}")

    while True:
        try:
            # 1. Periodically refresh the list of streams matching the pattern
            if time.time() - last_refresh > refresh_interval:
                # Use scan_iter to find keys matching the pattern
                for stream in r.scan_iter(match=REDIS_STREAM_PATTERN):
                    if stream not in active_streams:
                        try:
                            # Ensure consumer group exists for this stream
                            r.xgroup_create(stream, REDIS_GROUP, id='0', mkstream=True)
                            print(f"New stream detected: {stream}. Created group {REDIS_GROUP}")
                        except redis.exceptions.ResponseError as e:
                            if "already exists" not in str(e):
                                print(f"Error creating group for {stream}: {e}")
                        
                        # Start with '0' to check for pending messages from previous runs
                        active_streams[stream] = '0'
                last_refresh = time.time()

            if not active_streams:
                # No streams found yet, wait a bit
                time.sleep(2)
                continue

            # 2. Read messages from all tracked streams
            # xreadgroup returns list: [[stream, [[id, data], ...]], ...]
            messages = r.xreadgroup(REDIS_GROUP, REDIS_CONSUMER, active_streams, count=10, block=5000)

            if not messages:
                # If no messages were returned, any stream currently checking pending ('0') 
                # should be switched to new messages ('>')
                for stream in active_streams:
                    if active_streams[stream] == '0':
                        active_streams[stream] = '>'
                continue

            # 3. Process and Bridge
            for stream_name, entries in messages:
                for entry_id, data in entries:
                    print(f"Bridging [{stream_name}] message {entry_id}: {data}")
                    
                    # Forward to Kafka
                    # Derive topic name from stream name (e.g., events:auth:login -> events.auth.login)
                    # If it's a fixed stream (no pattern), use the KAFKA_TOPIC env var
                    target_topic = KAFKA_TOPIC
                    if '*' in REDIS_STREAM_PATTERN or REDIS_STREAM_PATTERN != stream_name:
                        target_topic = stream_name.replace(':', '.')

                    producer.send(target_topic, value=data)
                    
                    # Acknowledge in Redis
                    r.xack(stream_name, REDIS_GROUP, entry_id)
            
            producer.flush()

        except Exception as e:
            print(f"Error in bridge loop: {e}")
            time.sleep(2)
            # Reset to check pending on error to ensure no data is missed
            for s in active_streams:
                active_streams[s] = '0'

if __name__ == "__main__":
    main()
