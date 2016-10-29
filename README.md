# devops-restapi
Devops Assignment - RESTful API and Agile development

This project contains a minimalistic service that lets people (“users”) input in their available times. And then use the “meet” function to find common time that set of users are available to get a meeting time.

Entry points :
/user – to add,remove,update,view user details
/times – to store the available for a user
/meet -  to get a common available time for a set of users

# Running
Runs on localhost:5000 by default
You can user bluemix by setting the VCAP_SERVICES environment variable 
Uses redis on localhost:6379 by default
```
$ python server.py
```

# Endpoints
## Creating users
POST /users\s\s
Request body:
```
{
  "name": "Foo Bar", 
  "id": 0, 
  "times": [
    {
      "from":10, 
      "to":30
    },
    {
      "from":50, 
      "to":60
    }
  ]
}
```
Response codes: 201 Created, 409 Conflicts\s\s 
Response body:
```
{
  "name": "Foo Bar", 
  "id": 0, 
  "times": [
    {
      "from":10, 
      "to":30
    },
    {
      "from":50, 
      "to":60
    }
  ]
}
```
