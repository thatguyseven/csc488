from flask import Flask

app = Flask(__name__)

@app.route("/degrees", methods=['GET'])
def get_data(): 
    return [ str([{'id': 0, 'year': 1990, 'degrees': 5818}, 
        {'id': 1, 'year': 1991, 'degrees': 5725}, 
        {'id': 2, 'year': 1992, 'degrees': 6005}, 
        {'id': 3, 'year': 1993, 'degrees': 6123}, 
        {'id': 4, 'year': 1994, 'degrees': 6096}]) ] 

if __name__ == 'main':
        app.run(debug=True,host='0.0.0.0')