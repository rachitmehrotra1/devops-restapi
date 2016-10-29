import os
import redis
from flask import Flask, Response, jsonify, request, json

app = Flask(__name__)
app.debug = True
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

@app.route('/users/<id>', methods=['DELETE'])
def delete_users(id):
    del users[id];
    return '', HTTP_204_NO_CONTENT

@app.route('/users', methods=['GET'])
def list_users():
    unpacked_users = json.loads(redis_server.get('users'))
    return reply(unpacked_users, HTTP_200_OK)


@app.route('/users', methods=['POST'])
def create_user():
    payload = json.loads(request.data)
    id = payload['name']
    unpacked_users = redis_server.get('users')
    users == unpacked_users
    if users.has_key(id):
        message = { 'error' : 'User %s already exists' % id }
        rc = HTTP_409_CONFLICT
    else:
        users[id] = payload
        message = users[id]
        rc = HTTP_201_CREATED
        json_users=json.dumps(users)
        redis_server.set('users',json_users)

    return reply(message, rc)

def reply(message, rc):
    response = Response(json.dumps(message))
    response.headers['Content-Type'] = 'application/json'
    response.status_code = rc
    return response


# Initialize Redis
def init_redis(hostname, port, password):
    # Connect to Redis Server
    global redis_server
    redis_server = redis.Redis(host=hostname, port=port, password=password)
    if not redis_server:
        print '*** FATAL ERROR: Could not conect to the Redis Service'
        exit(1)

if __name__ == "__main__":
    # Get the crdentials from the Bluemix environment
    if 'VCAP_SERVICES' in os.environ:
        VCAP_SERVICES = os.environ['VCAP_SERVICES']
        services = json.loads(VCAP_SERVICES)
        redis_creds = services['rediscloud'][0]['credentials']
        # pull out the fields we need
        redis_hostname = redis_creds['hostname']
        redis_port = int(redis_creds['port'])
        redis_password = redis_creds['password']
    else:
        redis_hostname = '127.0.0.1'
        redis_port = 6379
        redis_password = None

    init_redis(redis_hostname, redis_port, redis_password)
    # Get bindings from the environment
    port = os.getenv('PORT', '5000')
    app.run(host='0.0.0.0', port=int(port))

