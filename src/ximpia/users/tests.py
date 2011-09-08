from django.test import TestCase

import forms

from django.contrib.auth.models import User, Group
from models import UserX
from ximpia.human_resources.models import Professional, Profile
from models import BsAccount

class Account(TestCase):
	
	def testForm(self):
		FormDict = {
			'ximpiaId': 'jalegre_test', 
			'email': 'jorge.alegre@zoho.com',
			'firstName': "Jorge",
			'lastName': 'Alegre',
			'password': '123456',
			'passwordVerify': '123456',
			'industry': ['102','103','104'],
			'city': 'Madrid',
			'country': 'es',
			'userGroups': ['1']
			}
		form = forms.FrmUserSignup(FormDict)
		check = form.isValid()
		self.assert_(check == True)
	def testSignupNoNets(self):
		FormDict = {
			'ximpiaId': 'jalegre_test', 
			'email': 'jorge.alegre@zoho.com',
			'firstName': "Jorge",
			'lastName': 'Alegre',
			'password': '123456',
			'passwordVerify': '123456',
			'industry': ['102','103','104'],
			'city': 'Madrid',
			'country': 'es',
			'userGroups': ['1']
			}
		form = forms.FrmUserSignup(FormDict)
		check = form.isValid()
		self.assert_(check==True)
		# doSignup
		request = None
		BsAccount.doSignup(request, form)
		# Test get
		user = User.objects.get(username='jalegre_test')
		userX = UserX.objects.get(User=user)
		professional = Professional.objects.get(User=userX)
		profile = Profile.objects.get(Professional=professional)
		self.assert_(user != None)
		self.assert_(userX != None)
		self.assert_(professional != None)
		self.assert_(profile != None)
		self.assert_(userX.City == 'Madrid')
		self.assert_(userX.Country == 'es')
		self.assert_(userX.Groups.filter(Group__name='Users').exists()==True)
		self.assert_(Professional.objects.filter(User=userX).exists()==True)
		self.assert_(Profile.objects.filter(Professional=professional).exists()==True)
		self.assert_(user.email=='jorge.alegre@zoho.com')
		self.assert_(userX.ValidatedEmail==False)
		self.assert_(user.check_password('123456') == True)
	def testSignupNets(self):
		FormDict = {
			'ximpiaId': 'jalegre_test', 
			'email': 'jorge.alegre@zoho.com',
			'firstName': "Jorge",
			'lastName': 'Alegre',
			'password': '123456',
			'passwordVerify': '123456',
			'industry': ['102','103','104'],
			'city': 'Madrid',
			'country': 'es',
			'userGroups': ['1'],
			'twitter': 'jalegre',
			'twitterPass': 'madrid24'
			}
		form = forms.FrmUserSignup(FormDict)
		check = form.isValid()
		self.assert_(check==True)
		# doSignup
		request = None
		BsAccount.doSignup(request, form)
		# Test get
		user = User.objects.get(username='jalegre_test')
		userX = UserX.objects.get(User=user)
		professional = Professional.objects.get(User=userX)
		profile = Profile.objects.get(Professional=professional)
		self.assert_(user != None)
		self.assert_(userX != None)
		self.assert_(professional != None)
		self.assert_(profile != None)
		self.assert_(userX.City == 'Madrid')
		self.assert_(userX.Country == 'es')
		self.assert_(userX.Groups.filter(Group__name='Users').exists()==True)
		self.assert_(Professional.objects.filter(User=userX).exists()==True)
		self.assert_(Profile.objects.filter(Professional=professional).exists()==True)
		self.assert_(user.email=='jorge.alegre@zoho.com')
		self.assert_(userX.ValidatedEmail==False)
		self.assert_(user.check_password('123456') == True)
		self.assert_(userX.TwitterAuth == True)
		self.assert_(userX.SocialNetworks.count() == 1)
		self.assert_(userX.SocialNetworks.all()[0].getName() == 'twitter')
		self.assert_(userX.getSocialNetworkUser('twitter').Account == 'jalegre')
		self.assert_(userX.Groups.count() == 4)
		self.assert_(userX.getGroupById(102).pk == 102)
	def testSignupOrganization(self):
		pass
