from flask import Flask, jsonify, request
import json

app = Flask(__name__)

@app.route("/get-data")
def get_data(): 
    data = [{"id": 0, "year": 1990, "degrees": 5818}, 
        {"id": 1, "year": 1991, "degrees": 5725}, 
        {"id": 2, "year": 1992, "degrees": 6005}, 
        {"id": 3, "year": 1993, "degrees": 6123}, 
        {"id": 4, "year": 1994, "degrees": 6096}]
    return (data)

@app.route("/degrees")
def degrees():
    d = get_data() 
    start = request.args.get('start') 
    limit = request.args.get('limit') 
    if start: 
        try: 
            start = int(start) 
        except ValueError: 
            return "Invalid start parameter; start must be an integer." 
    if limit: 
        try: 
            limit = int(limit) 
        except ValueError: 
            return "Invalid limit parameter; limit must be an integer.", 400
        return jsonify(d[start:limit])
    else:
        return jsonify(d[start:]) 


if __name__ == 'main':
        app.run(debug=True,host='0.0.0.0')