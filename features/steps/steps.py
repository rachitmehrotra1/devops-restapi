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