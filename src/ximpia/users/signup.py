from models import BsAccount
from models import UserX
from django.contrib.auth.models import User, Group

def staticContent(request):
	pass

def signUpProfessional(request):
	# First Name, Last Name
	# City, Country(Drop Box), Email
	# Facebook data if authenticated with fb
	# Linked Social Networks: Twitter, LinkedIn
	# Industries
	# Groups: Professional, Industries selected, Ximpia Groups (Create groups, max 3) 
	pass

def signUpOrganization(request):
	# Account, Org Name, Domain
	# Main Contact (Employee data) (This user will have admin rights). Later on in admin
	# region can add employees, groups, link to Twitter org, twitter for departments or groups
	# Employee: First Name, Last Name, Email, EmployeeId (Opt), City, Country, Group
	# Social Networks for employee
	# Industries
	# Ximpia Groups (Create Groups, max 3)
	pass

def signUpConsumer(request):
	# First Name, Last Name
	# City, Country(Drop Box), Email
	# Facebook data if authenticated with fb
	# Linked Social Networks: Twitter, LinkedIn
	# Industries
	pass

def doSignupProfessional(request):
	# User
	user = User()
	# [a-z][A-Z][_.] for username
	user.username = ''
	user.first_name = ''
	user.last_name = ''
	user.email = ''
	user.set_password('')
	# UserX
	userX = UserX()
	userX.City = ''
	userX.Country = ''
	userX.SocialNetwork = ''
	createAccounts = BsAccount()
	createAccounts.doProfessionalSignup(user, userX)
	# Could show different templates
	# render template
	# return html code

def doSignupOrganization(request):
	createAccounts = BsAccount()
	createAccounts.doOrganizationSignup(user, userX, organization)

def doSignupConsumer(request):
	createAccounts = BsAccount()
	createAccounts.doConsumerSignup(user, userX)

def validateAccount(request):
	# Validates user by UserX.ValidateEmail = True
	pass

def jxGetMethod(action):
	# Instantiate model data classes
	actionDict = {}
	# Operations
	
	
	
	method = actionDict[action]
	return method
