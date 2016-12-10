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
        server.init_redis(True)
        server.data_reset()
        #server.data_load({ "id": 0, "name": "John Rofrano", "times": [ { "from":1477523957, "to":1477524957 } ] })
 
    def test_prod_env(self):
        import os
        # Check production environment works (obviously no credentials here, just check whether it'd be set properly)
        services = {
          "rediscloud":[{
            "credentials":{
              "hostname": "127.0.0.1",
              "port": 6379,
              "password": None
            }
          }]
        }
        os.environ["VCAP_SERVICES"] = json.dumps(services)
        self.assertTrue(server.init_redis(True) == None)
        self.assertTrue(server.init_redis(False) == None)
        services['rediscloud'][0]['credentials']['hostname'] = "31.41.59.26"
        services['rediscloud'][0]['credentials']['password'] = "forty-two"
        os.environ["VCAP_SERVICES"] = json.dumps(services)
        self.assertRaises(SystemExit, server.init_redis(False))

    def test_index(self):
        resp = self.app.get('/')
        self.assertTrue ('Swagger UI' in resp.data)
        self.assertTrue( resp.status_code == HTTP_200_OK )
        
    def test_create_user(self):
        # save the current number of users for later comparison
        users_count = self.get_users_count()
        # add a new user
        new_user = { "name": "JR", "times": [ { "from":1477523957, "to":1477524957 } ] }
        data = json.dumps(new_user)
        resp = self.app.post('/users', data=data, content_type='application/json')
        self.assertTrue( resp.status_code == HTTP_201_CREATED )
        new_json = json.loads(resp.data)
        self.assertTrue (new_json['name'] == 'JR')
        # check that count has gone up and includes JR
        resp = self.app.get('/users')
        #print 'resp_data(2): ' + resp.data
        data = json.loads(resp.data)
        self.assertTrue( resp.status_code == HTTP_200_OK )
        self.assertTrue( len(data) == users_count + 1 )
        #check that if a user already exists an error is given
        newer_user = { "name": "JR", "times": [ { "from":1477523957, "to":1477524957 } ] }
        data = json.dumps(newer_user)
        resp = self.app.post('/users', data=data, content_type='application/json')
        #self.assertTrue( resp.status_code == HTTP_409_CONFLICT )
        
    def test_create_existing_user(self):
        # save the current number of users for later comparison
        users_count = self.get_users_count()
        # add a new user
        new_user = { "name": "JR", "times": [ { "from":1477523957, "to":1477524957 } ] }
        data = json.dumps(new_user)
        resp = self.app.post('/users', data=data, content_type='application/json')
        self.assertTrue( resp.status_code == HTTP_201_CREATED )
        new_json = json.loads(resp.data)
        self.assertTrue (new_json['name'] == 'JR')
        # check that count has gone up and includes JR
        resp = self.app.get('/users')
        #print 'resp_data(2): ' + resp.data
        data = json.loads(resp.data)
        self.assertTrue( resp.status_code == HTTP_200_OK )
        self.assertTrue( len(data) == users_count + 1 )
        #check that if a user already exists an error is given
        newer_user = { "name": "JR", "times": [ { "from":1477523957, "to":1477524957 } ] }
        data = json.dumps(newer_user)
        resp = self.app.post('/users', data=data, content_type='application/json')
        #self.assertTrue( resp.status_code == HTTP_409_CONFLICT )
    def test_get_users_list(self):
        # add a new user
        new_user = { "name": "JR", "times": [ { "from":1477523957, "to":1477524957 } ] }
        data = json.dumps(new_user)
        resp = self.app.post('/users', data=data, content_type='application/json')
        self.assertTrue( resp.status_code == HTTP_201_CREATED )
        new_json = json.loads(resp.data)
        self.assertTrue (new_json['name'] == 'JR')
        #check if users list went up
        resp = self.app.get('/users')
        #print 'resp_data: ' + resp.data
        self.assertTrue( resp.status_code == HTTP_200_OK )
        self.assertTrue( len(resp.data) > 0 )
        
    def test_get_users(self):
        # add a new user
        new_user = { "name": "JR", "times": [ { "from":1477523957, "to":1477524957 } ] }
        data = json.dumps(new_user)
        resp = self.app.post('/users', data=data, content_type='application/json')
        self.assertTrue( resp.status_code == HTTP_201_CREATED )
        new_json = json.loads(resp.data)
        self.assertTrue (new_json['name'] == 'JR')
        # test getting the specific user
        resp = self.app.get('/users/1')
        #print 'resp_data: ' + resp.data
        self.assertTrue( resp.status_code == HTTP_200_OK )
        data = json.loads(resp.data)
        self.assertTrue (data['name'] == 'JR')
        # test if getting a specific user that does not exist returns an error
        resp = self.app.get('/users/101')
        #print 'resp_data: ' + resp.data
        self.assertTrue( resp.status_code == HTTP_400_BAD_REQUEST )

        
    def test_update_user(self):
        # add a new user
        new_user = { "name": "JR", "times": [ { "from":1477523957, "to":1477524957 } ] }
        data = json.dumps(new_user)
        resp = self.app.post('/users', data=data, content_type='application/json')
        self.assertTrue( resp.status_code == HTTP_201_CREATED )
        new_json = json.loads(resp.data)
        self.assertTrue (new_json['name'] == 'JR')
        # test updating the user
        user = {}
        user['name'] = "Professor JR"
        user['times'] = [ { "from":1477523957, "to":1477524957 } ]
        data = json.dumps(user)
        resp = self.app.put('/users/1', data=data, content_type='application/json')
        self.assertTrue( resp.status_code == HTTP_200_OK )
        new_json = json.loads(resp.data)
        self.assertTrue (new_json['name'] == 'Professor JR')
        # test if updating a user that does not exist returns an error
        copy_user = {}
        copy_user['name'] = "Professor JR"
        copy_user['times'] = [ { "from":1477523957, "to":1477524957 } ]
        data = json.dumps(copy_user)
        resp = self.app.put('/users/1111', data=data, content_type='application/json')
        self.assertTrue( resp.status_code == HTTP_404_NOT_FOUND )
        
        
    def test_delete_user(self):
        # add a new user
        new_user = { "name": "JR", "times": [ { "from":1477523957, "to":1477524957 } ] }
        data = json.dumps(new_user)
        resp = self.app.post('/users', data=data, content_type='application/json')
        self.assertTrue( resp.status_code == HTTP_201_CREATED )
        new_json = json.loads(resp.data)
        self.assertTrue (new_json['name'] == 'JR')
        # test deleting user
        # # # save the current number of user for later comparison
        user_count = self.get_users_count()
        # delete a user
        resp = self.app.delete('/users/1', content_type='application/json')
        self.assertTrue( resp.status_code == HTTP_204_NO_CONTENT )
        self.assertTrue( len(resp.data) == 0 )
        new_count = self.get_users_count()
        self.assertTrue ( new_count == user_count - 1)
        # test if deleting a user that doesn't already exist returns an error
        resp = self.app.delete('/users/1', content_type='application/json')
        self.assertTrue( resp.status_code == HTTP_400_BAD_REQUEST )
        
    def test_set_times(self):
        # add a new user
        new_user = { "name": "JR", "times": [ { "from":1477523957, "to":1477524957 } ] }
        data = json.dumps(new_user)
        resp = self.app.post('/users', data=data, content_type='application/json')
        self.assertTrue( resp.status_code == HTTP_201_CREATED )
        new_json = json.loads(resp.data)
        self.assertTrue (new_json['name'] == 'JR')
        # test setting a new time for the user
        time = { "from":1477525957, "to":1477526957 }
        data = json.dumps(time)
        resp = self.app.post('/users/1/times', data=data, content_type='application/json')
        self.assertTrue( resp.status_code == HTTP_200_OK )
        # test setting a time for a user that doesn't exist
        time = { "from":30, "to":50 }
        data = json.dumps(time)
        resp = self.app.post('/users/1214/times', data=data, content_type='application/json')
        self.assertTrue( resp.status_code == HTTP_400_BAD_REQUEST )
        # test setting a time for a user incorrectly by missing "from" in the request
        time = { "to":50 }
        data = json.dumps(time)
        resp = self.app.post('/users/1/times', data=data, content_type='application/json')
        self.assertTrue( resp.status_code == HTTP_400_BAD_REQUEST )
        
    def test_remove_times(self):
        # add a new user
        new_user = { "name": "JR", "times": [ { "from":1477523957, "to":1477524957 } ] }
        data = json.dumps(new_user)
        resp = self.app.post('/users', data=data, content_type='application/json')
        self.assertTrue( resp.status_code == HTTP_201_CREATED )
        new_json = json.loads(resp.data)
        self.assertTrue (new_json['name'] == 'JR')
        # test setting a new time for the user
        time = { "from":1477525957, "to":1477526957 }
        data = json.dumps(time)
        resp = self.app.post('/users/1/times', data=data, content_type='application/json')
        self.assertTrue( resp.status_code == HTTP_200_OK )
        # test removing the wrong time range for the user
        time = { "from":30, "to":50 }
        data = json.dumps(time)
        resp = self.app.put('/users/1/times', data=data, content_type='application/json')
        self.assertTrue( resp.status_code == HTTP_400_BAD_REQUEST )
        # test removing a time for a user incorrectly by missing "from" in the request 
        time = { "to":1477526957 }
        data = json.dumps(time)
        resp = self.app.put('/users/1331/times', data=data, content_type='application/json')
        self.assertTrue( resp.status_code == HTTP_400_BAD_REQUEST )
        # test removing the new time for the user
        time = { "from":1477525957, "to":1477526957 }
        data = json.dumps(time)
        resp = self.app.put('/users/1/times', data=data, content_type='application/json')
        self.assertTrue( resp.status_code == HTTP_200_OK )
        # test removing a time for the user that doesn't exist
        time = { "from":1477525957, "to":1477526957 }
        data = json.dumps(time)
        resp = self.app.put('/users/1331/times', data=data, content_type='application/json')
        self.assertTrue( resp.status_code == HTTP_400_BAD_REQUEST )        
        
    def test_remove_times_invalid_time(self):
        # add a new user
        new_user = { "name": "JR", "times": [ { "from":1477523957, "to":1477524957 } ] }
        data = json.dumps(new_user)
        resp = self.app.post('/users', data=data, content_type='application/json')
        self.assertTrue( resp.status_code == HTTP_201_CREATED )
        new_json = json.loads(resp.data)
        self.assertTrue (new_json['name'] == 'JR')
        # test setting a new time for the user
        time = { "from":1477525957, "to":1477526957 }
        data = json.dumps(time)
        resp = self.app.post('/users/1/times', data=data, content_type='application/json')
        self.assertTrue( resp.status_code == HTTP_200_OK )
        # test removing the wrong time range for the user
        time = { "from":"1477525957", "to":"1477526957" }
        data = json.dumps(time)
        resp = self.app.put('/users/1/times', data=data, content_type='application/json')
        self.assertTrue( resp.status_code == HTTP_400_BAD_REQUEST )
        
    def test_meet_function(self):
        # add a new user
        user = { "name": "JR", "times": [ { "from":1477523957, "to":1477524957 } ] }
        data = json.dumps(user)
        resp = self.app.post('/users', data=data, content_type='application/json')
        self.assertTrue( resp.status_code == HTTP_201_CREATED )
        new_json = json.loads(resp.data)
        self.assertTrue (new_json['name'] == 'JR')
        # add a second user
        new_user = { "name": "Student", "times": [ { "from":1477523957, "to":1477524957 } ] }
        data = json.dumps(new_user)
        resp = self.app.post('/users', data=data, content_type='application/json')
        self.assertTrue( resp.status_code == HTTP_201_CREATED )
        new_json = json.loads(resp.data)
        self.assertTrue (new_json['name'] == 'Student')
        # test to see if users can meet - they should be able to
        resp = self.app.get('/meet', query_string='users=1,2')
        self.assertTrue( resp.status_code == HTTP_200_OK )
        # test to see if user was not valid
        resp = self.app.get('/meet', query_string='users=1,1111')
        self.assertTrue( resp.status_code == HTTP_400_BAD_REQUEST )
        
    def test_meet_function_empty_schedules(self):
        # add a new user
        user = { "name": "JR", "times": [] }
        data = json.dumps(user)
        resp = self.app.post('/users', data=data, content_type='application/json')
        self.assertTrue( resp.status_code == HTTP_201_CREATED )
        new_json = json.loads(resp.data)
        self.assertTrue (new_json['name'] == 'JR')
        # add a second user
        new_user = { "name": "Student", "times": [] }
        data = json.dumps(new_user)
        resp = self.app.post('/users', data=data, content_type='application/json')
        self.assertTrue( resp.status_code == HTTP_201_CREATED )
        new_json = json.loads(resp.data)
        self.assertTrue (new_json['name'] == 'Student')
        # test to see if users can meet - they should be able to
        resp = self.app.get('/meet', query_string='users=1,2')
        self.assertTrue( resp.status_code == HTTP_200_OK )
        self.assertTrue( json.loads(resp.data) == [])


    def test_meet_function_no_intersection(self):
        # add a new user
        user = { "name": "JR", "times": [{"from":10, "to":20}] }
        data = json.dumps(user)
        resp = self.app.post('/users', data=data, content_type='application/json')
        self.assertTrue( resp.status_code == HTTP_201_CREATED )
        new_json = json.loads(resp.data)
        self.assertTrue (new_json['name'] == 'JR')
        # add a second user
        new_user = { "name": "Student", "times": [{"from":40, "to":50}] }
        data = json.dumps(new_user)
        resp = self.app.post('/users', data=data, content_type='application/json')
        self.assertTrue( resp.status_code == HTTP_201_CREATED )
        new_json = json.loads(resp.data)
        self.assertTrue (new_json['name'] == 'Student')
        # test to see if users can meet - they should be able to
        resp = self.app.get('/meet', query_string='users=1,2')
        self.assertTrue( resp.status_code == HTTP_200_OK )
        self.assertTrue( json.loads(resp.data) == [])

    def test_merge_first_no_intersect_at_beginning(self):
        result = server.merge([(30, 40, [2])], \
          [(10, 20, [1]),(25, 35, [1])])
        self.assertTrue(result == [ \
          (10,20,[1]), \
          (25,30,[1]), \
          (30,35,[1,2]), \
          (35,40,[2]), \
        ])

    def test_merge_first_starts_after_second(self):
        result = server.merge([ \
          (101, 201, [1]), \
          (251, 351, [1]), \
          (451, 551, [1]) \
        ], \
          [(30, 40, [2])])
        self.assertTrue(result == [ \
          (30, 40, [2]), \
          (101, 201, [1]), \
          (251, 351, [1]), \
          (451, 551, [1]) \
        ])

    def test_merge2_superset(self):
        result = server.merge2((10,20,[1]),(13,17,[2]))
        self.assertTrue(result == [ \
          (10,13,[1]), \
          (13,17,[1,2]), \
          (17,20,[1]) \
        ])

######################################################################
# Swagger UI test functions
######################################################################

    def test_index(self):
        response = self.app.get("/")
        self.assertNotEqual(response.status_code, HTTP_404_NOT_FOUND)
    
    def test_send_lib(self):
        response = self.app.get("/lib/marked.js")
        self.assertNotEqual(response.status_code, HTTP_404_NOT_FOUND)
    
    def test_send_spec(self):
        response = self.app.get("/specification/meet.js")
        self.assertNotEqual(response.status_code, HTTP_404_NOT_FOUND)
    
    def test_send_img(self):
        response = self.app.get("/images/logo_small.png")
        self.assertNotEqual(response.status_code, HTTP_404_NOT_FOUND)
    
    def test_send_css(self):
        response = self.app.get("/css/style.css")
        self.assertNotEqual(response.status_code, HTTP_404_NOT_FOUND)
    
    def test_send_fonts(self):
        response = self.app.get("/fonts/DroidSans.ttf")
        self.assertNotEqual(response.status_code, HTTP_404_NOT_FOUND)
        
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
    unittest.main(exit=False)
