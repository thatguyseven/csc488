from flask import Flask, request, jsonify, send_file
import json
import os

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

if __name__ == '__main__':
        app.run(debug=True,host='0.0.0.0', port=5000)