Feature: The user schedule back-end
    As a Scheduler
    I need a RESTful catalog service
    So that I can keep track of all my users and schedules

Background:
	Given the server is started

Scenario: The server is running
    When I visit the "home page"
    Then I should not see "404 Not Found"

Scenario: List all users
	Given the following JSON is parsed:
	"""
	[
	  {
		"name": "JR",
            "times": [
              {
                "from":1477523967,
                "to":1477524958
              },{
                "from":14772396000,
                "to":  147752490000
              }
            ]
       }
    ]
    """
		
	When I visit '/users'
	Then I should see 'JR'
