from flask import Flask, request, jsonify, send_file
import json
import redis
import os
import redis_info

rd = redis_info.get_addr()

app = Flask(__name__)

@app.route("/", methods=['GET'])
def hello_world():
        return "Hello, Flask!"

@app.route("/Meteorite_Landings.json", methods=['GET'])
def send_landing_data():
        try:
                file_path = os.path.join(os.getcwd(), "Meteorite_Landings.json")
                
                if not os.path.exists(file_path):
                        return jsonify({"error": "JSON file not found"}), 404
                
                return send_file(file_path, as_attachment=True)
        except Exception as e:
                return jsonify({"error": str(e)}), 500
        
@app.route("/data", methods=['POST'])
def load_to_redis():
        # Opens "Meteorite_Landings.json" and loads data into local memory
        with open("Meteorite_Landings.json", "r") as f:
                data = json.load(f)
        
        # Stores landing sites into Redis database
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
                try:
                        # DEBUG: Logging print functions 
                        # print(f"Row {site_id}: {clean_row}")
                        # print(f"Type: {type(clean_row)}, Content: {clean_row}")
                        # Iterate through the clean_row and set each field-value pair
                        for field, value in clean_row.items():
                                rd.hset(key, field, value)
                except Exception as e:
                        print(f"Redis insert failed for key {key}: {e}")
                        
        # Return success message
        return jsonify({"message": f"Successfully loaded {len(data["meteorite_landings"])} meteorite landings into Redis."}), 200

@app.route("/data", methods=['GET'])
def load_from_redis():
        meteorite_data = []

        # Check if the Redis keys start from meteorite:1 (assuming keys are in this pattern)
        site_id = 1
        while True:
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