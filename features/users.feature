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
	Given the following users
		|	name	|	times	|
		|	john	|			|
		|	sydney	|			|
	Given the following times for user "john"
		|	from	|	to		|
		|	1477523967	|	1477534958	|
		
	When I visit '/users'
	Then I should see 'john'
	And I should see 'sydney'
	And I should see '1477523967'
	And I should see '1477534958'
