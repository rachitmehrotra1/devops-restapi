Feature: The user schedule back-end
    As a Scheduler
    I need a RESTful catalog service
    So that I can keep track of all my users and schedules

Background:
	Given the server is started

Scenario: The server is running
    When I visit the "home page"
    Then I should not see "404 Not Found"

Scenario: Create a user
	Given the following users
		|	name	|	times_from	|	times_to	|
		|	john	|	14775		|	24775		|
	When I visit '/users'
	Then I should see 'john'

Scenario: List all users
	Given the following users
		|	name	|	times_from	|	times_to	|
		|	john	|				|				|
		|	sydney	|				|				|
	Given the following times for user "john" with userID 1
		|	from	|	to		|
		|	1477523967	|	1477534958	|
		
	When I visit '/users'
	Then I should see a list of users
	And I should see 'john'
	And I should see 'sydney'

Scenario: Get a user
	Given the following users
		|	name	|	times_from	|	times_to	|
		|	John	|				|				|
	Given the following times for user "John" with userID 1
		|	from	|	to		|
		|	1477523957	|	1477524957	|
		
	When I visit '/users/1'
	Then I should see 'John'
	And I should see '1477523957'

Scenario: Delete a user
	Given the following users
		|	name	|	times_from	|	times_to	|
		|	John	|				|				|
	Given the following times for user "John" with userID 1
		|	from	|	to		|
		|	1477523957	|	1477524957	|
	When I visit '/users'
	Then I should see 'John'
	When I delete '/users/1'
	And I visit '/users'
	Then I should not see 'John'

Scenario: Update a user
	Given the following users
		|	name	|	times_from	|	times_to	|
		|	John	|				|				|
		|	Sydney	|				|				|
	Given the following times for user "John" with userID 1
		|	from	|	to		|
		|	1477523957	|	1477524957	|
	When I visit '/users'
	Then I should see 'John'
	And I should see 'Sydney'
	Given the following times for user "Sydney" with userID 2
		|	from	|	to		|
		|	1478523957	|	1478524957	|
	When I visit '/users/2'
	Then I should see '1478523957'

Scenario: Meet users - 2 users basic functionality
  Given the following users
		|	name	|
		|	John	|
		|	Sydney|
	Given the following times for user "John" with userID 1
		|	from	|	to		|
		|	10	|	30	|
	Given the following times for user "Sydney" with userID 2
		|	from	|	to		|
		|	20	|	40	|
	When I visit '/meet?users=1,2'
  Then I should get the interval 20 - 30 with users 1,2
  
Scenario: Meet users with length - 2 users basic functionality
  Given the following users
		|	name	|
		|	John	|
		|	Sydney|
	Given the following times for user "John" with userID 1
		|	from	|	to		|
		|	10	|	30	|
		|	100	|	135	|
	Given the following times for user "Sydney" with userID 2
		|	from	|	to		|
		|	20	|	40	|
		|	115	|	140	|
	When I visit '/meet?users=1,2&length=15'
  Then I should get the interval 115 - 135 with users 1,2

Scenario: Meet users - 2 users no intersection
  Given the following users
		|	name	|
		|	John	|
		|	Sydney|
	Given the following times for user "John" with userID 1
		|	from	|	to		|
		|	10	|	30	|
	Given the following times for user "Sydney" with userID 2
		|	from	|	to		|
		|	40	|	60	|
	When I visit '/meet?users=1,2'
  Then I should get an empty array
  
Scenario: Meet users with length - 2 users no intersection
  Given the following users
		|	name	|
		|	John	|
		|	Sydney|
	Given the following times for user "John" with userID 1
		|	from	|	to		|
		|	10	|	30	|
		|	100	|	135	|
	Given the following times for user "Sydney" with userID 2
		|	from	|	to		|
		|	40	|	60	|
		|	145	|	160	|
	When I visit '/meet?users=1,2&length=15'
  Then I should get an empty array

