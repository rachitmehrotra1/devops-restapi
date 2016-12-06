from behave import *
import server
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
	users = {}
	i = 1
	for row in context.table:
		users[i] = {'name': row['name'], 'times': row['times']}
		i = i + 1
	#print (users)
	context.server.users = users


@given(u'the following times for user \"{name}\"')
def step_impl(context, name):
	users = {}
	users['name'] = {'name': name}
	for row in context.table:
		users['times'] = {'from': row['from'], 'to': row['to']}
	# context.server.users = users

@when(u'I visit \'{url}\'')
def step_impl(context, url):
	context.resp = context.app.get(url)
	#print (context.resp)
	assert context.resp.status_code == 200

@then(u'I should see \'{name}\'')
def step_impl(context, name):
	print (context.server.users)
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
