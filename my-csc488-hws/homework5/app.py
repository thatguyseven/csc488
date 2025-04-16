from flask import Flask, request, jsonify, send_file
import json
import redis
import os
import redis_info

rd = redis_info.get_addr()

app = Flask(__name__)
        
@app.route("/data", methods=['POST'])
def load_to_redis():
        # Opens "Meteorite_Landings.json" and loads data into local memory
        with open("./data/Meteorite_Landings.json", "r") as f:
                data = json.load(f)
        
        # Stores landing sites into Redis database
        for site_id, row in enumerate(data["meteorite_landings"], start=1):
                key = str(site_id)
                """
                # Ensure all keys and values are strings
                stringified_row = {str(k): str(v) for k, v in row.items()}
                """
                rd.hset(key, mapping=row)
        # Return success message
        return jsonify({"message": f"Successfully loaded {len(data["meteorite_landings"])} meteorite landings into Redis."}), 200

@app.route("/data", methods=['GET'])
def load_from_redis():
        # Optional query parameter to limit query
        limit = request.args.get('limit') 
        meteorite_data = []

        # Check if delimiter
        if limit: 
                try: 
                        limit = int(limit) 
                        return jsonify(meteorite_data[0:limit])
                except ValueError: 
                        return "Invalid limit parameter; limit must be an integer.", 400
                
        # Check if the Redis keys start from meteorite:1 (assuming keys are in this pattern)
        site_id = 1
        while True:
                # Check if limit exists, then check if key exceeds limit 
                if limit: 
                        if site_id <= limit:
                                break

                key = f"{site_id}"
        
                # Check if the key exists in Redis
                if not rd.exists(key):
                        break
        
                # Retrieve the hash stored under the current Redis key
                meteorite = rd.hgetall(key)

                # Convert the byte data to string and create a dictionary
                meteorite = {k.decode('utf-8'): v.decode('utf-8') for k, v in meteorite.items()}
                
                # Add the meteorite data to the list
                meteorite_data.append(meteorite)

                # Move to the next key
                site_id += 1
        
        # Return the meteorite data as JSON
        return jsonify(meteorite_data)

if __name__ == '__main__':
        app.run(debug=True,host='0.0.0.0', port=5000)