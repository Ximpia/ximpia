



def staticContent(request):
	# We could pass variables to input
	pass

def login(request):
	# Support for workflow destiny
	# We need login??? It seems an static page
	# TODO: Decide on auth social network placed in session, cookie, etc...
	pass

def showStatus(request):
	pass


###############################################################
#  AJAX
###############################################################


def jxOperationXXX(request):
	# ?????????????????????
	# When complex model calls are needed
	# Get parameterList from request.POST
	# Place this method in the user case file module
	pass

def jxGetMethod(action):
	# Instantiate model data classes
	actionDict = {}
	# Operations
	actionDict['post'] = ''
	actionDict['showStatus'] = ''
	method = actionDict[action]
	return method

def jxAction(request):
	# We call methods on model to make actions, like create organization account, etc...
	# Returns json with boolean true or false	
	# We need:
	action = ''
	template = ''
	# Could work in case static
	#methodReq = 'Account.get'
	#method = eval(methodReq)
	parameterList = []			
	response = jxGetMethod(action)(parameterList)
	# sHtml ????? => Call template
	return response

def jxGetList(request):
	# Get list and return json object
	# In Javascript, we convert json to Array
	# We need:
	action = ''
	parameterList = []
	response = jxGetMethod(action)(parameterList)
	# sHtml ????? => Call template
	return response
