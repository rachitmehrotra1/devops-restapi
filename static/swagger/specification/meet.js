var spec = {
    "swagger": "2.0",
    "info": {
        "version": "1.0.0",
        "title": "Meeting Rest API",
        "description": "**This is an API made as a part of DevOps course at NYU**\n\nThe meeting API can be used by people from different organizations to add there\nfree times in the system and the meet function of the api automatically finds the best time for people to meet\n\nFind source code of this API [here](https://github.com/rachitmehrotra1/devops-restapi)\n"
    },
    "host": "devchronops.mybluemix.net",
    "basePath": "/",
    "schemes": [
        "http",
        "https"
    ],
    "consumes": [
        "application/json",
        "text/xml"
    ],
    "produces": [
        "application/json",
        "text/html"
    ],
    "paths": {
        "/meet?users={id1},{id2}": {
            "get": {
                "description": "This is main feature of the API, the algorithm goes and searches through the free times of all the memebers of the meeting and finds the best possible common time.\n**There are be any number of users in the meeting, for this example we use 2 users**",
                "parameters": [
                    {
                        "name": "id1",
                        "in": "path",
                        "description": "User1 of the meeting",
                        "required": true,
                        "type": "integer"
                    },
                    {
                        "name": "id2",
                        "in": "path",
                        "required": true,
                        "description": "User2 of the meeting",
                        "type": "integer"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Best possible time for meeting",
                        "schema": {
                            "title": "Meeting Time",
                            "type": "array",
                            "items": {
                                "$ref": "#/definitions/meetResponse"
                            }
                        }
                    },
                    "400": {
                        "description": "Enter valid existing user ids",
                        "schema": {
                            "title": "respone",
                            "type": "object",
                            "items": {
                                "$ref": "#/definitions/error"
                            }
                        }
                    }
                }
            }
        },
        "/users": {
            "get": {
                "responses": {
                    "200": {
                        "description": "List all users",
                        "schema": {
                            "title": "Users",
                            "type": "array",
                            "items": {
                                "$ref": "#/definitions/User"
                            }
                        }
                    }
                }
            },
            "post": {
                "parameters": [
                    {
                        "name": "User",
                        "in": "body",
                        "description": "User name and times",
                        "schema": {
                            "$ref": "#/definitions/User"
                        },
                        "required": true
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Created User"
                    },
                    "409": {
                        "description": "User already exist",
                        "schema": {
                            "title": "respone",
                            "type": "object",
                            "items": {
                                "$ref": "#/definitions/error"
                            }
                        }
                    }
                }
            }
        },
        "/users/{id}": {
            "get": {
                "parameters": [
                    {
                        "name": "id",
                        "in": "path",
                        "type": "integer",
                        "description": "ID of the User",
                        "required": true
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Sends the user with the ID"
                    },
                    "400": {
                        "description": "User doesn't exist",
                        "schema": {
                            "title": "respone",
                            "type": "object",
                            "items": {
                                "$ref": "#/definitions/error"
                            }
                        }
                    }
                }
            },
            "put": {
                "parameters": [
                    {
                        "name": "id",
                        "in": "path",
                        "type": "integer",
                        "description": "ID of the User",
                        "required": true
                    },
                    {
                        "in": "body",
                        "name": "user",
                        "description": "User details",
                        "required": true,
                        "schema": {
                            "$ref": "#/definitions/User"
                        }
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Updates the user with the id, and replaces with Body"
                    },
                    "404": {
                        "description": "User not found",
                        "schema": {
                            "title": "respone",
                            "type": "object",
                            "items": {
                                "$ref": "#/definitions/error"
                            }
                        }
                    }
                }
            },
            "delete": {
                "parameters": [
                    {
                        "name": "id",
                        "in": "path",
                        "type": "integer",
                        "description": "ID of the User",
                        "required": true
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Deletes the user with the ID"
                    },
                    "204": {
                        "description": "User does not exist",
                        "schema": {
                            "title": "respone",
                            "type": "object",
                            "items": {
                                "$ref": "#/definitions/error"
                            }
                        }
                    }
                }
            }
        },
        "/users/{id}/times": {
            "post": {
                "parameters": [
                    {
                        "name": "id",
                        "in": "path",
                        "type": "integer",
                        "description": "ID of the User",
                        "required": true
                    },
                    {
                        "in": "body",
                        "name": "time",
                        "description": "times the user is free",
                        "required": true,
                        "schema": {
                            "$ref": "#/definitions/time"
                        }
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Add a time interval"
                    },
                    "400": {
                        "description": "Body must be an object with \"from\" and \"to\" being integer fields",
                        "schema": {
                            "title": "respone",
                            "type": "object",
                            "items": {
                                "$ref": "#/definitions/error"
                            }
                        }
                    }
                }
            },
            "put": {
                "parameters": [
                    {
                        "name": "id",
                        "in": "path",
                        "type": "integer",
                        "description": "ID of the User",
                        "required": true
                    },
                    {
                        "in": "body",
                        "name": "time",
                        "description": "times that you want to delete",
                        "required": true,
                        "schema": {
                            "$ref": "#/definitions/time"
                        }
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Deletes the user with the ID"
                    },
                    "400": {
                        "description": "Body must be an object with \"from\" and \"to\" being integer fields  OR User doesn't exist",
                        "schema": {
                            "title": "respone",
                            "type": "object",
                            "items": {
                                "$ref": "#/definitions/error"
                            }
                        }
                    }
                }
            }
        }
    },
    "definitions": {
        "User": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string"
                },
                "time": {
                    "$ref": "#/definitions/time"
                }
            }
        },
        "time": {
            "type": "object",
            "properties": {
                "from": {
                    "type": "number"
                },
                "to": {
                    "type": "number"
                }
            }
        },
        "meetResponse": {
            "type": "object",
            "properties": {
                "from": {
                    "type": "number"
                },
                "to": {
                    "type": "number"
                },
                "people": {
                    "type": "number"
                }
            }
        },
        "error": {
            "type": "object",
            "properties": {
                "error": {
                    "type": "string"
                }
            }
        }
    }
};