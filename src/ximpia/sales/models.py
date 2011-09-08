import base64
import time
import os
import cPickle
import random

from django.db import models
from django.contrib.auth.models import User as UserSys, Group as GroupSys
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session
from django.utils.hashcompat import md5_constructor
from django.http import HttpResponse

from ximpia.social_network.models import Choices as ChoicesUsers

from ximpia import settings

class Constants(object):
	pass

class Choices(object):
	INDUSTRY = ()
	SALUTATION_MR = 'mr'
	SALUTATION_MS = 'ms'
	SALUTATION_DR = 'dr'
	SALUTATION = (
			(SALUTATION_MR,'Mr.'),
			(SALUTATION_MS,'Miss'),
			(SALUTATION_DR,'Dr.'),
			)
	EMAIL = 'email'
	HOME = 'home'
	WORK = 'work'
	MOBILE = 'mobile'
	WORK_MOBILE = 'work_mobile'
	FAX = 'fax'
	NETWORK = 'network'
	SITE = 'site'
	CONTACT_COMM = (
		(EMAIL,'Email'),
		(HOME,'HomePhone'),
		(WORK,'WorkPhone'),
		(MOBILE,'Mobile'),
		(WORK_MOBILE,'WorkMobile'),
		(FAX,'Fax'),
		(NETWORK,'Social Network'),
		('', 'Site'),
		)
	TWITTER = 'twitter'
	FACEBOOK = 'facebook'
	LINKEDIN = 'linkedin'
	IMPORT = 'import'
	GMAIL = 'gmail'
	YAHOO = 'yahoo'
	MSN = 'msn'
	CONTACT_SOURCE = (
			(TWITTER,'Twitter'),
			(FACEBOOK,'Facebook'),
			(LINKEDIN,'LinkedIn'),
			(IMPORT,'Imported'),
			(GMAIL,'Gmail'),
			(YAHOO,'Yahoo'),
			(MSN,'MSN'),
			)
	TYPE_CONTACT_MAIN = 'contact'
	TYPE_CONTACT_CANDIDATE = 'candidate'
	TYPE_CONTACT_ACCOUNT = 'client'
	TYPE_CONTACTS = (
			(TYPE_CONTACT_MAIN,'Contact'),
			(TYPE_CONTACT_CANDIDATE,'Candidate'),
			(TYPE_CONTACT_ACCOUNT,'Client Contact'),
			)


class DeleteManager(models.Manager):
	def get_query_set(self):
		return super(DeleteManager, self).get_query_set().filter(Delete=False)



class ContactSales(models.Model):
	Contact = models.ForeignKey('Contact')
	ContactType = models.CharField(max_length=15, choices=Choices.TYPE_CONTACTS)
	AllowCall = models.BooleanField(default=True)
	DateCreate = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	DateModify = models.DateTimeField(auto_now=True, null=True, blank=True)
	UserCreateId = models.IntegerField(null=True, blank=True)
	UserModifyId = models.IntegerField(null=True, blank=True)
	Delete = models.BooleanField(default=False)
	objects = DeleteManager()
	objects_del = models.Manager()
	def __unicode__(self):
		return str(self.Contact)
	class Meta:
		db_table = 'SA_CONTACTS_SALES'

class Opportunity(models.Model):
	#OwnerEmployee = models.ForeignKey('human_resources.Employee', related_name='opportunity_owner_employee', null=True, blank=True)
	OwnerOrg = models.ForeignKey('human_resources.Organization', related_name='opportunity_owner_org', null=True, blank=True)
	OpportunityId = models.CharField(max_length=100, null=True, blank=True)
	Name = models.CharField(max_length=120)
	ContactsRelated = models.ManyToManyField('ContactSales')
	SharedWith = models.ManyToManyField('OpportunityShare')
	Ammount = models.DecimalField(max_digits=6,decimal_places=2, null=True, blank=True)
	Currency = models.CharField(max_length=3, null=True, blank=True)
	ClosingDate = models.DateField(null=True, blank=True)
	TypeOfRevenue = models.CharField(max_length=50, null=True, blank=True)
	Probability = models.DecimalField(max_digits=7, decimal_places=3, null=True, blank=True)
	Score = models.IntegerField(default=0)
	Description = models.TextField(null=True, blank=True)
	DateCreate = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	DateModify = models.DateTimeField(auto_now=True, null=True, blank=True)
	UserCreateId = models.IntegerField(null=True, blank=True)
	UserModifyId = models.IntegerField(null=True, blank=True)
	Delete = models.BooleanField(default=False)
	objects = DeleteManager()
	objects_del = models.Manager()
	def __unicode__(self):
		return self.Name
	class Meta:
		db_table = 'SA_OPPORTUNITIES'

class OpportunityShare(models.Model):
	User = models.ForeignKey('users.UserX')
	Vote = models.BooleanField(default=False)
	NumberVotes = models.IntegerField(default=0)
	DateCreate = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	DateModify = models.DateTimeField(auto_now=True, null=True, blank=True)
	UserCreateId = models.IntegerField(null=True, blank=True)
	UserModifyId = models.IntegerField(null=True, blank=True)
	Delete = models.BooleanField(default=False)
	objects = DeleteManager()
	objects_del = models.Manager()
	def __unicode__(self):
		return self.User
	class Meta:
		db_table = 'SA_OPPORTUNITIES_SHARED'

class Account(models.Model):
	#OwnerEmployee = models.ForeignKey('human_resources.Employee', related_name='account_owner_employee', null=True, blank=True)
	OwnerOrg = models.ForeignKey('human_resources.Organization', related_name='account_owner_org', null=True, blank=True)
	Name = models.CharField(max_length=100, unique=True)
	Brand = models.CharField(max_length=20, unique=True, null=True, blank=True)
	Number = models.CharField(max_length=100, unique=True, null=True, blank=True)
	Parent = models.ForeignKey('self', null=True, blank=True)
	Type = models.CharField(max_length=100, null=True, blank=True)
	Industry = models.CharField(max_length=20, choices=Choices.INDUSTRY, null=True, blank=True)
	AnnualRevenue = models.IntegerField(null=True, blank=True)
	Ammount = models.DecimalField(max_digits=6,decimal_places=2, null=True, blank=True)
	Currency = models.CharField(max_length=3, null=True, blank=True)
	TypeOfRevenue = models.CharField(max_length=50, null=True, blank=True)
	Description = models.TextField(null=True, blank=True)
	Ownership = models.CharField(max_length=50, null=True, blank=True)
	SicCode = models.CharField(max_length=50, null=True, blank = True)
	Tax = models.ManyToManyField('human_resources.Tax', null=True, blank=True)
	Phone = models.CharField(max_length=20, null=True, blank = True)
	OtherPhone = models.CharField(max_length=20, null=True, blank = True)
	Email1 = models.EmailField(max_length=100, null=True, blank = True)
	Email2 = models.EmailField(max_length=100, null=True, blank = True)
	Fax = models.CharField(max_length=20, null=True, blank = True)
	SocialNetwork = models.ManyToManyField('users.SocialNetwork', null=True, blank = True)
	Addresses = models.ManyToManyField('human_resources.Address')
	DateCreate = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	DateModify = models.DateTimeField(auto_now=True, null=True, blank=True)
	UserCreateId = models.IntegerField(null=True, blank=True)
	UserModifyId = models.IntegerField(null=True, blank=True)
	Delete = models.BooleanField(default=False)
	objects = DeleteManager()
	objects_del = models.Manager()
	def __unicode__(self):
		return self.Name
	class Meta:
		db_table = 'SA_ACCOUNTS'

"""ALTER TABLE `XIMPIA`.`SA_FAQ` ADD FULLTEXT INDEX `SA_FAQ_QUESTION`(`Question`),
 ADD FULLTEXT INDEX `SA_FAQ_SOLUTION`(`Solution`);"""
class FAQ(models.Model):
	#OwnerEmployee = models.ForeignKey('human_resources.Employee', related_name='faq_owner_employee', null=True, blank=True)
	OwnerOrg = models.ForeignKey('human_resources.Organization', related_name='faq_owner_org', null=True, blank=True)
	FaqNumber = models.CharField(max_length=100, db_index=True, null=True, blank=True)
	Question = models.TextField()
	Solution = models.TextField()
	Status = models.IntegerField()
	Comments = models.ManyToManyField('users.Comment')
	Tags = models.ManyToManyField('users.Tag')
	DateCreate = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	DateModify = models.DateTimeField(auto_now=True, null=True, blank=True)
	UserCreateId = models.IntegerField(null=True, blank=True)
	UserModifyId = models.IntegerField(null=True, blank=True)
	Delete = models.BooleanField(default=False)
	objects = DeleteManager()
	objects_del = models.Manager()
	def __unicode__(self):
		return self.Question
	class Meta:
		db_table = 'SA_FAQ'

class Feedback(models.Model):
	OwnerOrg = models.ForeignKey('human_resources.Organization', related_name='feedback_owner_org', null=True, blank=True)
	Number = models.CharField(max_length=100, null=True, blank=True)
	Title = models.CharField(max_length=100)
	Message = models.CharField(max_length=500)
	Voting = models.CommaSeparatedIntegerField(max_length=20, null=True, blank=True)
	Comments = models.ManyToManyField('users.Comment')
	DateCreate = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	DateModify = models.DateTimeField(auto_now=True, null=True, blank=True)
	UserCreateId = models.IntegerField(null=True, blank=True)
	UserModifyId = models.IntegerField(null=True, blank=True)
	Delete = models.BooleanField(default=False)
	objects = DeleteManager()
	objects_del = models.Manager()
	def __unicode__(self):
		return self.Title
	class Meta:
		db_table = 'SA_FEEDBACK'

###########################################################################################


