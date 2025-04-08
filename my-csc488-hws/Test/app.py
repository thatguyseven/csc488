from flask import Flask, request, jsonify
import redis

app = Flask(__name__)
r = redis.Redis(host='host.docker.internal', port=6379, db=0)

@app.route("/set", methods=["POST"])
def set_to_redis():
    data = request.get_json()
    
    # Get key and value from the JSON payload
    key = data.get('key')
    value = data.get('value')

    if not key or not value:
        return jsonify({'error': 'Key and value are required'}), 400

    # Save to Redis
    r.set(key, value)

    return jsonify({'message': f'Saved {key}: {value} to Redis'}), 200

@app.route('/get/<key>', methods=['GET'])
def get_from_redis(key):
    value = r.get(key)

    # ERROR HANDLING: Sends an error message if no key is found
    if value is None:
        return jsonify({'error': f'No value found for key: {key}'}), 404

    # Decode value from bytes to string
    return jsonify({'key': key, 'value': value.decode('utf-8')}), 200

@app.route('/delete/<key>', methods=['DELETE'])
def delete_from_redis(key):
    result = r.delete(key)

    if result == 0:
        return jsonify({'error': f'Key "{key}" not found'}), 404

    return jsonify({'message': f'Key "{key}" deleted successfully'}), 200

if __name__ == "__main__":
    app.run(debug=True)