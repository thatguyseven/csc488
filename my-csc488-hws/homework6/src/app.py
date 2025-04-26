from flask import Flask, request, jsonify, send_file
import json
import redis
import os
import sys
import time

app = Flask(__name__)

# --- Configuration ---
# Get Redis Service Name and Port from environment variables
# It's best practice to pass these via environment variables in Kubernetes
# The default Kubernetes DNS name for a service is <service-name>.<namespace>.svc.cluster.local
# Within the same namespace, just <service-name> is usually sufficient.
REDIS_SERVICE_NAME = os.environ.get("REDIS_SERVICE_NAME", "test-redis-server")
REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))

# --- Script Logic ---
def access_redis():
        """Connects to Redis and performs basic operations."""
        print(f"Attempting to connect to Redis at {REDIS_SERVICE_NAME}:{REDIS_PORT}...")

        try:
                # Connect to Redis
                # decode_responses=True makes GET commands return strings instead of bytes
                r = redis.StrictRedis(host=REDIS_SERVICE_NAME, port=REDIS_PORT, decode_responses=True)

                # Ping the server to check the connection
                r.ping()
                print("Successfully connected to Redis!")

                # Perform some basic Redis operations
                key = "mytestkey"
                value = f"hello-from-pod-at-{time.time()}"

                print(f"Setting key '{key}' to value '{value}'...")
                set_success = r.set(key, value)
                if set_success:
                        print("SET command successful.")
                else:
                        print("SET command failed.")

                print(f"Getting value for key '{key}'...")
                retrieved_value = r.get(key)
                print(f"Retrieved value: {retrieved_value}")

                # Optional: Delete the key
                # print(f"Deleting key '{key}'...")
                # delete_count = r.delete(key)
                # print(f"Deleted {delete_count} keys.")

        except redis.exceptions.ConnectionError as e:
                print(f"Error connecting to Redis: {e}", file=sys.stderr)
                print("Please ensure the Redis service name and port are correct and the Redis server is running.", file=sys.stderr)
                sys.exit(1)
        except Exception as e:
                print(f"An unexpected error occurred: {e}", file=sys.stderr)
                sys.exit(1)

@app.route("/data", methods=['POST'])
def load_to_redis():
        """
        Loads data from Meteorite_Landings.json in the data folder into a Redis database. Returns a HTTP 
        message about load status.

        Args:
                none
        
        Returns: HTTP JSON message
        """
        
        # Opens "Meteorite_Landings.json" and loads data into local memory
        with open("/app/data/Meteorite_Landings.json", "r") as f:
                data = json.load(f)

        """Connects to Redis and performs basic operations."""
        print(f"Attempting to connect to Redis at {REDIS_SERVICE_NAME}:{REDIS_PORT}...")

        try:
                # Connect to Redis
                # decode_responses=True makes GET commands return strings instead of bytes
                rd = redis.StrictRedis(host=REDIS_SERVICE_NAME, port=REDIS_PORT, decode_responses=True)

                # Enumerate each site in the landing data and store each row in the redis database
                for site_id, row in enumerate(data["meteorite_landings"], start=1):
                        key = f"{site_id}"
                        # DEBUG: Print type and content of data row
                        # print(f"Row {site_id}: {row}")
                        # print(f"Type: {type(row)}, Content: {row}")
                        if not isinstance(row, dict):
                                print(f"Skipping invalid row at index {site_id}: {row}")
                                continue

                        clean_row = {str(k): str(v) for k, v in row.items()}

                        # DEV NOTE: The reason why this does not work is likely due to some incongruity with the redis server and the version of redis used.
                        # DEBUG: Logging print functions 
                        # print(f"Row {site_id}: {clean_row}")
                        # print(f"Type: {type(clean_row)}, Content: {clean_row}")
                        # Iterate through the clean_row and set each field-value pair
                        for field, value in clean_row.items():
                                rd.hset(key, field, value)
        except redis.exceptions.ConnectionError as e:
                print(f"Error connecting to Redis: {e}", file=sys.stderr)
                print("Please ensure the Redis service name and port are correct and the Redis server is running.", file=sys.stderr)
                sys.exit(1)
        except Exception as e:
                print(f"An unexpected error occurred: {e}", file=sys.stderr)
                sys.exit(1)

        # Return success message
        return jsonify({"message": f"Successfully loaded {len(data['meteorite_landings'])} meteorite landings into Redis."}), 200

@app.route("/data", methods=['GET'])
def load_from_redis():
        """
        Loads data from Redis database. Returns site data in a JSON message.

        Args:
                limit (int): Optional. Specifies number of data elements returned.
        
        Returns: Site Data in JSON
        """
        # Optional query parameter to limit query
        limit = request.args.get('limit') 
        meteorite_data = []

        # Check if delimiter
        if limit: 
                try: 
                        limit = int(limit) 
                except ValueError: 
                        return "Invalid limit parameter; limit must be an integer.", 400
                
        # Check if the Redis keys start from meteorite:1 (assuming keys are in this pattern)
        site_id = 1
        try:
                # Connect to Redis
                # decode_responses=True makes GET commands return strings instead of bytes
                rd = redis.StrictRedis(host=REDIS_SERVICE_NAME, port=REDIS_PORT, decode_responses=True)
                while True:
                        # Check if limit exists, then check if key exceeds limit 
                        if limit: 
                                if site_id > limit:
                                        break

                        key = f"{site_id}"
                
                        # Check if the key exists in Redis
                        if not rd.exists(key):
                                break
                
                        # Retrieve the hash stored under the current Redis key
                        meteorite = rd.hgetall(key)

                        # Convert the byte data to string and create a dictionary
                        # meteorite = {k.decode('utf-8'): v.decode('utf-8') for k, v in meteorite.items()}
                        
                        # Add the meteorite data to the list
                        meteorite_data.append(meteorite)

                        # Move to the next key
                        site_id += 1
        except redis.exceptions.ConnectionError as e:
                print(f"Error connecting to Redis: {e}", file=sys.stderr)
                print("Please ensure the Redis service name and port are correct and the Redis server is running.", file=sys.stderr)
                sys.exit(1)
        
        except Exception as e:
                print(f"An unexpected error occurred: {e}", file=sys.stderr)
                sys.exit(1)

        # If the limit variable exists, return data up to the limit
        if limit:
                return jsonify(meteorite_data[0:limit])
        # Return the meteorite data as JSON
        return jsonify(meteorite_data)

if __name__ == '__main__':
        app.run(debug=True,host='0.0.0.0', port=5000)