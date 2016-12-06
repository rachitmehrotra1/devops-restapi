from behave import *
import server
@given(u'the server is started')
def step_impl(context):
	context.app = server.app.test_client()
	context.server = server

@when(u'I visit the "home page"')
def step_impl(context):
	context.resp = context.app.get('/')

@then(u'I should not see "{message}"')
def step_impl(context, message):
	assert message not in context.resp.data

@given(u'the following users')
def step_impl(context):
	users = {}
	for row in context.table:
		users[row['name']] = {'name': row['name']}
	context.server.users = users

@given(u'the following times for user \"{name}\"')
def step_impl(context, name):
	users = {}
	users['name'] = {'name': name}
	for row in context.table:
		users['times'] = {'from': row['from'], 'to': row['to']}

@when(u'I visit \'{url}\'')
def step_impl(context, url):
	context.resp = context.app.get(url)
	assert context.resp.status_code == 200

@then(u'I should see \'{name}\'')
def step_impl(context, name):
	assert name in context.resp.data
