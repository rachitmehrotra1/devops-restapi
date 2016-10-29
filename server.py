import os
from flask import Flask, Response, jsonify, request, json

app = Flask(__name__)

users = [{"id": 0, "name": "Carlos Guzman", "times":[{"from":1477523957, "to":1477524957}]}]

@app.route('/')
def index():
    return jsonify(name='Meeting REST API', version='1.0', url='/'), 200

@app.route('/users/<id>', methods=['DELETE'])
def delete_users(id):
    del users[id];
    return '', HTTP_204_NO_CONTENT

@app.route('/users', methods=['GET'])
def list_users():
    return reply(users, 200)

def reply(message, rc):
    response = Response(json.dumps(message))
    response.headers['Content-Type'] = 'application/json'
    response.status_code = rc
    return response

if __name__ == "__main__":
    # Get bindings from the environment
    port = os.getenv('PORT', '5000')
    app.run(host='0.0.0.0', port=int(port))

