import os
from flask import Flask, Response, jsonify, request, json

app = Flask(__name__)
# Status Codes
HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_204_NO_CONTENT = 204
HTTP_400_BAD_REQUEST = 400
HTTP_404_NOT_FOUND = 404
HTTP_409_CONFLICT = 409

users = {'Carlos Guzman':{'id': 0, 'name': 'Carlos Guzman', 'times':[{'from':1477523957, 'to':1477524957}]}}

@app.route('/')
def index():
    return jsonify(name='Meeting REST API', version='1.0', url='/'), 200

@app.route('/users', methods=['GET'])
def list_users():
    return reply(users, HTTP_200_OK)


@app.route('/users', methods=['POST'])
def create_user():
    payload = json.loads(request.data)
    id = payload['name']
    if users.has_key(id):
        message = { 'error' : 'User %s already exists' % id }
        rc = HTTP_409_CONFLICT
    else:
        users[id] = payload
        message = users[id]
        rc = HTTP_201_CREATED

    return reply(message, rc)

def reply(message, rc):
    response = Response(json.dumps(message))
    response.headers['Content-Type'] = 'application/json'
    response.status_code = rc
    return response

if __name__ == "__main__":
    # Get bindings from the environment
    port = os.getenv('PORT', '5000')
    app.run(host='0.0.0.0', port=int(port))

