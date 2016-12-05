# run with:
# python -m unittest discover

import unittest
import json
import server

# Status Codes
HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_204_NO_CONTENT = 204
HTTP_400_BAD_REQUEST = 400
HTTP_404_NOT_FOUND = 404
HTTP_409_CONFLICT = 409

######################################################################
#  T E S T   C A S E S
######################################################################
class TestServer(unittest.TestCase):

    def setUp(self):
        server.app.debug = True
        self.app = server.app.test_client()
        server.init_redis('127.0.0.1',6379,None)
        #server.data_load({ "id": 0, "name": "John Rofrano", "times": [ { "from":1477523957, "to":1477524957 } ] })
 
    def test_index(self):
        resp = self.app.get('/')
        self.assertTrue ('Meeting REST API' in resp.data)
        self.assertTrue( resp.status_code == HTTP_200_OK )
    
    def test_get_users_list(self):
        resp = self.app.get('/users')
        #print 'resp_data: ' + resp.data
        self.assertTrue( resp.status_code == HTTP_200_OK )
        self.assertTrue( len(resp.data) > 0 )
        
    def test_get_users(self):
        resp = self.app.get('/users/2')
        #print 'resp_data: ' + resp.data
        self.assertTrue( resp.status_code == HTTP_200_OK )
        data = json.loads(resp.data)
        self.assertTrue (data['name'] == 'Nihit Mody')

    def test_create_user(self):
        # save the current number of users for later comparison
        users_count = self.get_users_count()
        # add a new user
        new_user = { "id": 1, "name": "JR", "times": [ { "from":1477523957, "to":1477524957 } ] }
        data = json.dumps(new_user)
        resp = self.app.post('/users', data=data, content_type='application/json')
        self.assertTrue( resp.status_code == HTTP_201_CREATED )
        new_json = json.loads(resp.data)
        self.assertTrue (new_json['name'] == 'John Rofrano')
        # check that count has gone up and includes John Rofrano
        resp = self.app.get('/users')
        # print 'resp_data(2): ' + resp.data
        data = json.loads(resp.data)
        self.assertTrue( resp.status_code == HTTP_200_OK )
        self.assertTrue( len(data) == users_count + 1 )
        
    def test_update_user(self):
        user = {}
        user['name'] = "Professor JR"
        data = json.dumps(user)
        resp = self.app.put('/users/1', data=data, content_type='application/json')
        self.assertTrue( resp.status_code == HTTP_200_OK )
        new_json = json.loads(resp.data)
        self.assertTrue (new_json['name'] == 'Professor John Rofrano')
        
    def test_delete_user(self):
        # save the current number of user for later comparison
        user_count = self.get_users_count()
        # delete a user
        resp = self.app.delete('/users/1', content_type='application/json')
        self.assertTrue( resp.status_code == HTTP_204_NO_CONTENT )
        self.assertTrue( len(resp.data) == 0 )
        new_count = self.get_users_count()
        self.assertTrue ( new_count == user_count - 1)
        
######################################################################
# Utility functions
######################################################################

    def get_users_count(self):
        # save the current number of users
        resp = self.app.get('/users')
        self.assertTrue( resp.status_code == HTTP_200_OK )
        # print 'resp_data: ' + resp.data
        data = json.loads(resp.data)
        return len(data)

######################################################################
#   M A I N
######################################################################
if __name__ == '__main__':
    unittest.main()