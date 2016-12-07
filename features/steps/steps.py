from behave import *
import server
import json

@given(u'the server is started')
def step_impl(context):
	context.app = server.app.test_client()
	context.server = server
	context.server.init_redis()

@when(u'I visit the "home page"')
def step_impl(context):
	context.resp = context.app.get('/')

@then(u'I should not see "{message}"')
def step_impl(context, message):
	assert message not in context.resp.data

@given(u'the following users')
def step_impl(context):
	server.data_reset()
	users = {}
	url = '/users'
	i = 1
	for row in context.table:
		users[i] = {'name': row['name'], 'times': row['times']}
		#context.resp = context.app.post(url, data=json.dumps())
		i = i + 1
	#print (context.redis)
	#context.app.put(users)
	context.resp = context.app.post(url, data=json.dumps(users), content_type='application/json')
	context.server.users = users

@given(u'the following times for user \"{name}\" with userID {ID}')
def step_impl(context, name, ID):
	users = context.server.users
	url = '/users'
	user = users[int(ID)]
	for row in context.table:
		user['times'] = {'from': row['from'], 'to': row['to']}
	print(users)
	#users[int(ID)] = user
	context.resp = context.app.put(url, data=json.dumps(users), content_type='application/json')
	print (context.resp.data)

@when(u'I visit \'{url}\'')
def step_impl(context, url):
	context.resp = context.app.get(url)
	print (context.resp.data)
	assert context.resp.status_code == 200

@then(u'I should see \'{name}\'')
def step_impl(context, name):
	#print (context.resp.data)
	assert name in context.resp.data

@then(u'I should see a list of users')
def step_impl(context):
    assert context.resp.status_code == 200
    assert len(context.resp.data) > 0

@when(u'I delete \'{url}\'')
def step_impl(context, url):
	context.resp = context.app.delete(url)
	assert context.resp.status_code == 204

@then(u'I should not see \'{name}\'')
def step_impl(context, name):
	assert name not in context.resp.data

@when(u'I update \'{url}\'')
def step_impl(context, url):
	context.resp = context.app.post(url)
	assert context.resp.status_code == 200
