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

from ximpia import settings
from ximpia.social_network.models import Constants as ConstantsUsers

class Constants(object):
	pass

class Choices(object):
	# MILITARY
	MILITARY_NA = 'na'
	MILITARY_COMPLETED = 'completed'
	MILITARY_PENDING = 'pending'
	MILITARY = (
		(MILITARY_NA, 'N/A'),
		(MILITARY_COMPLETED, 'Completed'),
		(MILITARY_PENDING, 'Pending'),
		)
	# ETHNIC
	ETHNIC_WHITE = 'white'
	ETHNIC = (
		(ETHNIC_WHITE,'White/Causasian'),
		)
	# SUBSCRIPTION
	SUBSCRIPTION_TRIAL = 'trial'
	SUBSCRIPTION_VALID = 'valid'
	SUBSCRIPTION_NONE = 'None'
	SUBSCRIPTION = (
			(SUBSCRIPTION_TRIAL,'30-Day Free Trial'),
			(SUBSCRIPTION_VALID,'Valid'),
			(SUBSCRIPTION_NONE,'None'),
			)
	# EDUCATION
	EDUCATION_DEGREE = 'degree'
	EDUCATION_COURSE = 'course'
	EDUCATION_CERT = 'cert'
	EDUCATION = (
		(EDUCATION_DEGREE,'Degree'),
		(EDUCATION_COURSE,'Course'),
		(EDUCATION_CERT,'Certification'),
			)
	# COURSE_MEDIA
	COURSE_MEDIA_VIDEO = 'video'
	COURSE_MEDIA_PRESENTATION = 'slides'
	COURSE_MEDIA = (
		(COURSE_MEDIA_VIDEO,'Video'),
		(COURSE_MEDIA_PRESENTATION,'Presentation'),
		)
	# SEX
	SEX_MAN = 'm'
	SEX_WOMAN = 'w'
	SEX = (
		(SEX_MAN,'Man'),
		(SEX_WOMAN, 'Woman')
		)
	# CUSTOM_TYPE
	CUSTOM_TYPE_INPUT = 'input'
	CUSTOM_TYPE_COMBO = 'combo'
	CUSTOM_TYPE = (
		(CUSTOM_TYPE_INPUT,'Input'),
		(CUSTOM_TYPE_COMBO,'Combo'),
		)
	# SKILL_TYPE
	SKILL_TYPE_TECH = 'tech'
	SKILL_TYPE_TEAM_WORK = 'team_work'
	SKILL_TYPE = (
		(SKILL_TYPE_TECH,'Technical'),
		(SKILL_TYPE_TEAM_WORK,'Team Work'),
		)
	# INDUSTRY
	INDUSTRY = (
		(101,'Accounting'),
		(102,'Airlines/Aviation'),
		(103,'Alternative Dispute Resolution'),
		(104,'Alternative Medicine'),
		(105,'Animation'),
		(106,'Apparel & Fashion'),
		(107,'Architecture & Planning'),
		(108,'Arts and Crafts'),
		(109,'Automotive'),
		(110,'Aviation & Aerospace'),
		(111,'Banking'),
		(112,'Biotechnology'),
		(113,'Broadcast Media'),
		(114,'Building Materials'),
		(115,'Business Supplies and Equipment'),
		(116,'Capital Markets'),
		(117,'Chemicals'),
		(118,'Civic & Social Organization'),
		(119,'Civil Engineering'),
		(120,'Commercial Real Estate'),
		(121,'Computer & Network Security'),
		(122,'Computer Games'),
		(123,'Computer Hardware'),
		(124,'Computer Networking'),
		(125,'Computer Software'),
		(126,'Construction'),
		(127,'Consumer Electronics'),
		(128,'Consumer Goods'),
		(129,'Consumer Services'),
		(130,'Cosmetics'),
		(131,'Dairy'),
		(132,'Defense & Space'),
		(133,'Design'),		
		(134,'Education Management'),
		(135,'E-Learning'),
		(136,'Electrical/Electronic Manufacturing'),
		(137,'Entertainment'),
		(138,'Environmental Services'),
		(139,'Events Services'),
		(140,'Executive Office'),
		(141,'Facilities Services'),
		(142,'Farming'),
		(143,'Financial Services'),
		(144,'Fine Art'),
		(145,'Fishery'),
		(146,'Food & Beverages'),
		(147,'Food Production'),
		(148,'Fund-Raising'),
		(149,'Furniture'),
		(150,'Gambling & Casinos'),
		(151,'Glass, Ceramics & Concrete'),
		(152,'Government Administration'),
		(153,'Government Relations'),
		(154,'Graphic Design'),
		(155,'Health, Wellness and Fitness'),
		(156,'Higher Education'),
		(157,'Hospital & Health Care'),
		(158,'Hospitality'),
		(159,'Human Resources'),
		(160,'Import and Export'),
		(161,'Individual & Family Services'),
		(162,'Industrial Automation'),
		(163,'Information Services'),
		(164,'Information Technology and Services'),
		(165,'Insurance'),
		(166,'International Affairs'),
		(167,'International Trade and Development'),
		(168,'Internet'),
		(169,'Investment Banking'),
		(170,'Investment Management'),
		(171,'Judiciary'),
		(172,'Law Enforcement'),
		(173,'Law Practice'),
		(174,'Legal Services'),
		(175,'Legislative Office'),
		(176,'Leisure, Travel & Tourism'),
		(177,'Libraries'),
		(178,'Logistics and Supply Chain'),
		(179,'Luxury Goods & Jewelry'),
		(180,'Machinery'),
		(181,'Management Consulting'),
		(182,'Maritime'),
		(183,'Marketing and Advertising'),
		(184,'Market Research'),
		(185,'Mechanical or Industrial Engineering'),
		(186,'Media Production'),
		(187,'Medical Devices'),
		(188,'Medical Practice'),
		(189,'Mental Health Care'),
		(190,'Military'),
		(191,'Mining & Metals'),
		(192,'Motion Pictures and Film'),
		(193,'Museums and Institutions'),
		(194,'Music'),
		(195,'Nanotechnology'),
		(196,'Newspapers'),
		(197,'Non-Profit Organization Management'),
		(198,'Oil & Energy'),
		(199,'Online Media'),
		(200,'Outsourcing/Offshoring'),
		(201,'Package/Freight Delivery'),
		(202,'Packaging and Containers'),
		(203,'Paper & Forest Products'),
		(204,'Performing Arts'),
		(205,'Pharmaceuticals'),
		(206,'Philanthropy'),
		(207,'Photography'),
		(208,'Plastics'),
		(209,'Political Organization'),
		(210,'Primary/Secondary Education'),
		(211,'Printing'),
		(212,'Professional Training & Coaching'),
		(213,'Program Development'),
		(214,'Public Policy'),
		(215,'Public Relations and Communications'),
		(216,'Public Safety'),
		(217,'Publishing'),
		(218,'Railroad Manufacture'),
		(219,'Ranching'),
		(220,'Real Estate'),
		(221,'Recreational Facilities and Services'),
		(222,'Religious Institutions'),
		(223,'Renewables &amp; Environment'),
		(224,'Research'),
		(225,'Restaurants'),
		(226,'Retail'),
		(227,'Security and Investigations'),
		(228,'Semiconductors'),
		(229,'Shipbuilding'),
		(230,'Sporting Goods'),
		(240,'Sports'),
		(250,'Staffing and Recruiting'),
		(251,'Supermarkets'),
		(252,'Telecommunications'),
		(253,'Textiles'),
		(254,'Think Tanks'),
		(255,'Tobacco'),
		(256,'Translation and Localization'),
		(257,'Transportation/Trucking/Railroad'),
		(258,'Utilities'),
		(259,'Venture Capital & Private Equity'),
		(260,'Veterinary'),
		(261,'Warehousing'),
		(262,'Wholesale'),
		(263,'Wine and Spirits'),
		(264,'Wireless'),
		(265,'Writing and Editing'),
		)
	JOB_CANDIDATE_PENDING = 'pending'
	JOB_CANDIDATE_STATUS = (
			(JOB_CANDIDATE_PENDING,'Pending'),
			)
	JOB_CONTRACT = ()

class DeleteManager(models.Manager):
	def get_query_set(self):
		return super(DeleteManager, self).get_query_set().filter(Delete=False)

class HumanResourcesParam(models.Model):
	Mode = models.CharField(max_length=20)
	Name = models.CharField(max_length=20)
	Value = models.CharField(max_length=100, null=True, blank=True)
	ValueId = models.IntegerField(null=True, blank=True)
	DateCreate = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	DateModify = models.DateTimeField(auto_now=True, null=True, blank=True)
	UserCreateId = models.IntegerField(null=True, blank=True)
	UserModifyId = models.IntegerField(null=True, blank=True)
	Delete = models.BooleanField(default=False)
	objects = DeleteManager()
	objects_del = models.Manager()
	def __unicode__(self):
		return str(self.Mode) + ' ' + str(self.Name)
	class Meta:
		db_table = 'HR_PARAMS'

class OrganizationOptions(models.Model):
	Account = models.ForeignKey('Organization', primary_key=True)
	Public = models.BooleanField(default=True)
	Delete = models.BooleanField(default=False)
	DateCreate = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	DateModify = models.DateTimeField(auto_now=True, null=True, blank=True)
	UserCreateId = models.IntegerField(null=True, blank=True)
	UserModifyId = models.IntegerField(null=True, blank=True)
	objects = DeleteManager()
	objects_del = models.Manager()
	def __unicode__(self):
		return str(self.Account)
	class Meta:
		db_table = 'HR_ORGANIZATION_OPTIONS'

class ReportOrganization(models.Model):
	Organization = models.ForeignKey('Organization')
	OrganizationGroup = models.ForeignKey('OrganizationGroup')
	Managers = models.ManyToManyField('Professional')
	Delete = models.BooleanField(default=False)
	DateCreate = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	DateModify = models.DateTimeField(auto_now=True, null=True, blank=True)
	UserCreateId = models.IntegerField(null=True, blank=True)
	UserModifyId = models.IntegerField(null=True, blank=True)
	objects = DeleteManager()
	objects_del = models.Manager()
	def __unicode__(self):
		return ''
	class Meta:
		db_table = 'HR_REPORT_ORGANIZATION'

class TimeReport(models.Model):
	Professional = models.ForeignKey('Professional', related_name='timereport_professional')
	Organization = models.ForeignKey('Organization', related_name='timereport_organization')
	OrganizationGroup = models.ForeignKey('OrganizationGroup', null=True, blank=True)
	ActivityCode = models.CharField(max_length=25)
	Date = models.DateField()
	Hours = models.FloatField()
	ValidationProfessional = models.ForeignKey('Professional', null=True, blank=True)
	Delete = models.BooleanField(default=False)
	DateCreate = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	DateModify = models.DateTimeField(auto_now=True, null=True, blank=True)
	UserCreateId = models.IntegerField(null=True, blank=True)
	UserModifyId = models.IntegerField(null=True, blank=True)
	objects = DeleteManager()
	objects_del = models.Manager()
	def __unicode__(self):
		return ''
	class Meta:
		db_table = 'HR_TIME_REPORT'

class SkillProfessionalWorkExperience(models.Model):
	Skill = models.ForeignKey('Skill')
	WorkExperience = models.ForeignKey('ProfessionalWorkExperience')
	Time = models.IntegerField(null=True, blank=True)
	Rating = models.IntegerField(null=True, blank=True)
	Delete = models.BooleanField(default=False)
	DateCreate = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	DateModify = models.DateTimeField(auto_now=True, null=True, blank=True)
	UserCreateId = models.IntegerField(null=True, blank=True)
	UserModifyId = models.IntegerField(null=True, blank=True)
	objects = DeleteManager()
	objects_del = models.Manager()
	def __unicode__(self):
		return str(self.Skill) + ' ' + str(self.Professional)
	class Meta:
		db_table = 'HR_PROFESSIONAL_WORK_EXPERIENCE_Skills'

class SkillJobOffer(models.Model):
	Skill = models.ForeignKey('Skill')
	JobOffer = models.ForeignKey('JobOffer')
	Time = models.IntegerField(null=True, blank=True)
	Rating = models.IntegerField(null=True, blank=True)
	Delete = models.BooleanField(default=False)
	DateCreate = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	DateModify = models.DateTimeField(auto_now=True, null=True, blank=True)
	UserCreateId = models.IntegerField(null=True, blank=True)
	UserModifyId = models.IntegerField(null=True, blank=True)
	objects = DeleteManager()
	objects_del = models.Manager()
	def __unicode__(self):
		return str(self.Skill) + ' ' + str(self.JobOffer)
	class Meta:
		db_table = 'HR_JOB_OFFERS_Skills'

class ProfessionalTaskHistory(models.Model):
	Professional = models.ForeignKey('Professional', primary_key=True)
	Contract = models.ForeignKey('ProfessionalContract')
	FromDate = models.DateField()
	ToDate = models.DateField(null=True, blank=True)
	Delete = models.BooleanField(default=False)
	DateCreate = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	DateModify = models.DateTimeField(auto_now=True, null=True, blank=True)
	UserCreateId = models.IntegerField(null=True, blank=True)
	UserModifyId = models.IntegerField(null=True, blank=True)
	objects = DeleteManager()
	objects_del = models.Manager()
	def __unicode__(self):
		return str(self.Employee) + ' - ' + str(self.Contract)
	class Meta:
		db_table = 'HR_PROFESSIONAL_TASK_HISTORY'

class ProfessionalHistory(models.Model):
	Professional = models.ForeignKey('Professional', primary_key=True)
	Contract = models.ForeignKey('ProfessionalContract')
	JoinedDate = models.DateField(auto_now_add=True, null=True, blank=True)
	TerminatedDate = models.DateField(null=True, blank=True)
	TerminatedReason = models.TextField(null=True, blank=True)
	Delete = models.BooleanField(default=False)
	DateCreate = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	DateModify = models.DateTimeField(auto_now=True, null=True, blank=True)
	UserCreateId = models.IntegerField(null=True, blank=True)
	UserModifyId = models.IntegerField(null=True, blank=True)
	objects = DeleteManager()
	objects_del = models.Manager()
	def __unicode__(self):
		return str(self.Employee) + ' - ' + str(self.Contract)
	class Meta:
		db_table = 'HR_PROFESSIONAL_HISTORY'

class Curriculum(models.Model):
	Name = models.CharField(max_length=15, null=True, blank=True)
	Professional = models.ForeignKey('Professional')
	Education = models.ManyToManyField('ProfessionalEducation')
	EducationOnline = models.ManyToManyField('ProfessionalEducationOnline', null=True, blank=True)
	WorkExperience = models.ManyToManyField('ProfessionalWorkExperience')
	Delete = models.BooleanField(default=False)
	DateCreate = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	DateModify = models.DateTimeField(auto_now=True, null=True, blank=True)
	UserCreateId = models.IntegerField(null=True, blank=True)
	UserModifyId = models.IntegerField(null=True, blank=True)
	objects = DeleteManager()
	objects_del = models.Manager()
	def __unicode__(self):
		return str(self.Employee)
	class Meta:
		db_table = 'HR_CURRICULUM'

class JobCoverLetter(models.Model):
	Name = models.CharField(max_length=15, null=True, blank=True)
	Tags = models.ManyToManyField('users.Tag', null=True, blank=True)
	Professional = models.ForeignKey('Professional')
	Letter = models.TextField()
	Delete = models.BooleanField(default=False)
	DateCreate = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	DateModify = models.DateTimeField(auto_now=True, null=True, blank=True)
	UserCreateId = models.IntegerField(null=True, blank=True)
	UserModifyId = models.IntegerField(null=True, blank=True)
	objects = DeleteManager()
	objects_del = models.Manager()
	def __unicode__(self):
		return str(self.Employee)
	class Meta:
		db_table = 'HR_JOB_COVER_LETTERS'

class ProfessionalEducationOnline(models.Model):
	MediaType = models.CharField(max_length=15, choices=Choices.COURSE_MEDIA, null=True, blank=True)
	Organization = models.ForeignKey('Organization', null=True, blank=True)
	OrganizationGroup = models.ForeignKey('OrganizationGroup', null=True, blank=True)
	Name = models.CharField(max_length=50, null=True, blank=True)
	Summary = models.CharField(max_length=120, null=True, blank=True)
	Url = models.URLField(null=True, blank=True)	
	Description = models.TextField(null=True, blank=True)
	EmbededCode = models.CharField(max_length=500, null=True, blank=True)
	OrgDomainPublic = models.BooleanField(default=False)
	Feedback = models.ManyToManyField('ProfessionalFeedback', through='ProfessionalFeedbackEducationOnline', null=True, blank=True)
	#Industry = models.CharField(max_length=15, choices=Choices.INDUSTRY, null=True, blank=True)
	Industries = models.ManyToManyField('Industry')
	StartDate = models.DateField(null=True, blank=True)
	EndDate = models.DateField(null=True, blank=True)
	Hours = models.FloatField(null=True, blank=True)
	Tags = models.ManyToManyField('users.Tag', null=True, blank=True)
	Comments = models.ManyToManyField('users.Comment', null=True, blank=True)
	Likes = models.ManyToManyField('users.Like', null=True, blank=True)
	Shares = models.ManyToManyField('users.StatusShare', null=True, blank=True)
	Delete = models.BooleanField(default=False)
	DateCreate = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	DateModify = models.DateTimeField(auto_now=True, null=True, blank=True)
	UserCreateId = models.IntegerField(null=True, blank=True)
	UserModifyId = models.IntegerField(null=True, blank=True)
	objects = DeleteManager()
	objects_del = models.Manager()
	def __unicode__(self):
		return str(self.Name)
	class Meta:
		db_table = 'HR_PROFESSIONAL_EDUCATION_ONLINE'

class ProfessionalEducation(models.Model):
	Type = models.CharField(max_length=20, choices=Choices.EDUCATION)
	School = models.CharField(max_length=50, null=True, blank=True)
	Degree = models.CharField(max_length=50, null=True, blank=True)
	CourseName = models.CharField(max_length=50, null=True, blank=True)
	Certification = models.CharField(max_length=50, null=True, blank=True)
	Tags = models.ManyToManyField('users.Tag', null=True, blank=True)
	Comments = models.ManyToManyField('users.Comment', null=True, blank=True)
	Likes = models.ManyToManyField('users.Like', null=True, blank=True)
	Shares = models.ManyToManyField('users.StatusShare', null=True, blank=True)
	StartDate = models.DateField(null=True, blank=True)
	EndDate = models.DateField(null=True, blank=True)
	ExamDate = models.DateField(null=True, blank=True)
	Hours = models.FloatField(null=True, blank=True)
	#Industry = models.CharField(max_length=15, choices=Choices.INDUSTRY, null=True, blank=True)
	Industries = models.ManyToManyField('Industry')
	Public = models.BooleanField(default=False)
	Feedback = models.ManyToManyField('ProfessionalFeedback', through='ProfessionalFeedbackEducation', null=True, blank=True)
	Delete = models.BooleanField(default=False)
	DateCreate = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	DateModify = models.DateTimeField(auto_now=True, null=True, blank=True)
	UserCreateId = models.IntegerField(null=True, blank=True)
	UserModifyId = models.IntegerField(null=True, blank=True)
	objects = DeleteManager()
	objects_del = models.Manager()
	def __unicode__(self):
		if self.School:
			return str(self.School) + ' - ' + str(self.Degree)
		elif self.CourseName:
			return str(self.CourseName)
		elif self.Certification:
			return str(self.Certification)
		else:
			return str(self.Type)
	class Meta:
		db_table = 'HR_PROFESSIONAL_EDUCATION'

class ProfessionalWorkExperience(models.Model):
	Employer = models.CharField(max_length=50)
	JobTitle = models.CharField(max_length=50)
	Client = models.CharField(max_length=50, null=True, blank=True)
	WhatIDid = models.TextField()
	Skills = models.ManyToManyField('Skill', through='SkillProfessionalWorkExperience')
	Feedback = models.ManyToManyField('ProfessionalFeedback', through='ProfessionalFeedbackWorkExperience')
	StartDate = models.DateField()
	EndDate = models.DateField()
	Public = models.BooleanField(default=False)
	Delete = models.BooleanField(default=False)
	DateCreate = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	DateModify = models.DateTimeField(auto_now=True, null=True, blank=True)
	UserCreateId = models.IntegerField(null=True, blank=True)
	UserModifyId = models.IntegerField(null=True, blank=True)
	objects = DeleteManager()
	objects_del = models.Manager()
	def __unicode__(self):
		return str(self.Employer) + ' - ' + str(self.JobTitle)
	class Meta:
		db_table = 'HR_PROFESSIONAL_WORK_EXPERIENCE'

class ProfessionalAwardHonor(models.Model):
	Name = models.CharField(max_length=200)
	StartDate = models.DateField(null=True, blank=True)
	EndDate = models.DateField(null=True, blank=True)
	Delete = models.BooleanField(default=False)
	DateCreate = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	DateModify = models.DateTimeField(auto_now=True, null=True, blank=True)
	UserCreateId = models.IntegerField(null=True, blank=True)
	UserModifyId = models.IntegerField(null=True, blank=True)
	objects = DeleteManager()
	objects_del = models.Manager()
	def __unicode__(self):
		return ''
	class Meta:
		db_table = 'HR_PROFESSIONAL_AWARDS_HONORS'

class ProfessionalFeedbackEducation(models.Model):
	ProfessionalFeedback = models.ForeignKey('ProfessionalFeedback')
	ProfessionalEducation = models.ForeignKey('ProfessionalEducation')
	Description = models.TextField(null=True, blank=True)
	Like = models.BooleanField(default=False)
	DontLike = models.BooleanField(default=False)
	Rating = models.IntegerField(null=True, blank=True)
	Rating_1 = models.CommaSeparatedIntegerField(max_length=20, null=True, blank=True)
	Rating_2 = models.CommaSeparatedIntegerField(max_length=20, null=True, blank=True)
	Rating_3 = models.CommaSeparatedIntegerField(max_length=20, null=True, blank=True)
	Public = models.BooleanField(default=False)
	Delete = models.BooleanField(default=False)
	DateCreate = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	DateModify = models.DateTimeField(auto_now=True, null=True, blank=True)
	UserCreateId = models.IntegerField(null=True, blank=True)
	UserModifyId = models.IntegerField(null=True, blank=True)
	objects = DeleteManager()
	objects_del = models.Manager()
	def __unicode__(self):
		return str(self.User)
	class Meta:
		db_table = 'HR_PROFESSIONAL_EDUCATION_ProfessionalFeedback'

class ProfessionalFeedbackEducationOnline(models.Model):
	ProfessionalFeedback = models.ForeignKey('ProfessionalFeedback')
	ProfessionalEducationOnline = models.ForeignKey('ProfessionalEducationOnline')
	Description = models.TextField(null=True, blank=True)
	Like = models.BooleanField(default=False)
	DontLike = models.BooleanField(default=False)
	Rating = models.IntegerField(null=True, blank=True)
	Rating_1 = models.CommaSeparatedIntegerField(max_length=20, null=True, blank=True)
	Rating_2 = models.CommaSeparatedIntegerField(max_length=20, null=True, blank=True)
	Rating_3 = models.CommaSeparatedIntegerField(max_length=20, null=True, blank=True)
	Public = models.BooleanField(default=False)
	Delete = models.BooleanField(default=False)
	DateCreate = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	DateModify = models.DateTimeField(auto_now=True, null=True, blank=True)
	UserCreateId = models.IntegerField(null=True, blank=True)
	UserModifyId = models.IntegerField(null=True, blank=True)
	objects = DeleteManager()
	objects_del = models.Manager()
	def __unicode__(self):
		return str(self.User)
	class Meta:
		db_table = 'HR_PROFESSIONAL_EDUCATION_ONLINE_ProfessionalFeedback'

class ProfessionalFeedbackWorkExperience(models.Model):
	ProfessionalFeedback = models.ForeignKey('ProfessionalFeedback')
	ProfessionalWorkExperience = models.ForeignKey('ProfessionalWorkExperience')
	Description = models.TextField(null=True, blank=True)
	Like = models.BooleanField(default=False)
	DontLike = models.BooleanField(default=False)
	Rating = models.IntegerField(null=True, blank=True)
	Rating_1 = models.CommaSeparatedIntegerField(max_length=20, null=True, blank=True)
	Rating_2 = models.CommaSeparatedIntegerField(max_length=20, null=True, blank=True)
	Rating_3 = models.CommaSeparatedIntegerField(max_length=20, null=True, blank=True)
	Public = models.BooleanField(default=False)
	Delete = models.BooleanField(default=False)
	DateCreate = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	DateModify = models.DateTimeField(auto_now=True, null=True, blank=True)
	UserCreateId = models.IntegerField(null=True, blank=True)
	UserModifyId = models.IntegerField(null=True, blank=True)
	objects = DeleteManager()
	objects_del = models.Manager()
	def __unicode__(self):
		return str(self.User)
	class Meta:
		db_table = 'HR_PROFESSIONAL_WORK_EXPERIENCE_ProfessionalFeedback'

class ProfessionalFeedback(models.Model):
	User = models.ForeignKey('users.UserX', null=True, blank=True)
	Delete = models.BooleanField(default=False)
	DateCreate = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	DateModify = models.DateTimeField(auto_now=True, null=True, blank=True)
	UserCreateId = models.IntegerField(null=True, blank=True)
	UserModifyId = models.IntegerField(null=True, blank=True)
	objects = DeleteManager()
	objects_del = models.Manager()
	def __unicode__(self):
		return str(self.User)
	class Meta:
		db_table = 'HR_PROFESSIONAL_FEEDBACK'


class JobProfile(models.Model):
	Professional = models.ForeignKey('Professional')
	Summary = models.CharField(max_length=120, null=True, blank=True)
	Description = models.TextField(null=True, blank=True)
	SalaryMin = models.PositiveIntegerField(null=True, blank=True)
	SalaryMax = models.PositiveIntegerField(null=True, blank=True)
	Avaibility = models.CharField(max_length=100, null=True, blank=True)
	YearsExperience = models.PositiveSmallIntegerField(null=True, blank=True)
	Languages = models.ManyToManyField(HumanResourcesParam, limit_choices_to={'Mode__exact': 8}, related_name='job_profile_languages')
	Delete = models.BooleanField(default=False)
	DateCreate = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	DateModify = models.DateTimeField(auto_now=True, null=True, blank=True)
	UserCreateId = models.IntegerField(null=True, blank=True)
	UserModifyId = models.IntegerField(null=True, blank=True)
	objects = DeleteManager()
	objects_del = models.Manager()
	def __unicode__(self):
		return str(self.Professional)
	class Meta:
		db_table = 'HR_JOB_PROFILES'

class JobOffer(models.Model):
	Organization = models.ForeignKey('Organization', null=True, blank=True)
	Group = models.ForeignKey('OrganizationGroup', null=True, blank=True)
	PostDate = models.DateField(auto_now_add=True)
	Url = models.URLField(null=True, blank=True)
	Industry = models.CharField(max_length=15, choices=Choices.INDUSTRY)
	ContractType = models.CharField(max_length=20, choices=Choices.JOB_CONTRACT)
	YearsExperience = models.PositiveSmallIntegerField(null=True, blank=True)
	LocationCountry = models.CharField(max_length=2)
	LocationCity = models.CharField(max_length=50)
	SalaryMin = models.PositiveIntegerField(null=True, blank=True)
	SalaryMax = models.PositiveIntegerField(null=True, blank=True)
	SalaryPubic = models.BooleanField(default=False)
	Title = models.CharField(max_length=50)
	Summary = models.CharField(max_length=120)
	Tags = models.ManyToManyField('users.Tag', null=True, blank=True)
	Skills = models.ManyToManyField('Skill', through='SkillJobOffer', null=True, blank=True)
	Description = models.TextField(null=True, blank=True)
	StartDate = models.DateField()
	Status = models.CharField(max_length=10, choices=())
	SectionName_1 = models.CharField(max_length=50, null=True, blank=True)
	SectionValue_1 = models.TextField(null=True, blank=True)
	SectionName_2 = models.CharField(max_length=50, null=True, blank=True)
	SectionValue_2 = models.TextField(null=True, blank=True)
	SectionName_3 = models.CharField(max_length=50, null=True, blank=True)
	SectionValue_3 = models.TextField(null=True, blank=True)
	SectionName_4 = models.CharField(max_length=50, null=True, blank=True)
	SectionValue_4 = models.TextField(null=True, blank=True)
	SectionName_5 = models.CharField(max_length=50, null=True, blank=True)
	SectionValue_5 = models.TextField(null=True, blank=True)
	Delete = models.BooleanField(default=False)
	DateCreate = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	DateModify = models.DateTimeField(auto_now=True, null=True, blank=True)
	UserCreateId = models.IntegerField(null=True, blank=True)
	UserModifyId = models.IntegerField(null=True, blank=True)
	objects = DeleteManager()
	objects_del = models.Manager()
	def __unicode__(self):
		return str(self.Title) + ' '  + str(self.Summary)
	class Meta:
		db_table = 'HR_JOB_OFFERS'

class JobCandidate(models.Model):
	Curriculum = models.ForeignKey('Curriculum')
	CoverLetter = models.ForeignKey('JobCoverLetter', null=True, blank=True)
	JobOffer = models.ForeignKey('JobOffer')
	Status = models.CharField(max_length=10, choices=Choices.JOB_CANDIDATE_STATUS, default=Choices.JOB_CANDIDATE_PENDING)
	Delete = models.BooleanField(default=False)
	DateCreate = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	DateModify = models.DateTimeField(auto_now=True, null=True, blank=True)
	UserCreateId = models.IntegerField(null=True, blank=True)
	UserModifyId = models.IntegerField(null=True, blank=True)
	objects = DeleteManager()
	objects_del = models.Manager()
	def __unicode__(self):
		return str(JobOffer) + ' ' + str(self.Curriculum)
	class Meta:
		db_table = 'HR_JOB_CANDIDATES'

class Custom(models.Model):
	Organization = models.ForeignKey('Organization')
	FieldId = models.CharField(max_length=30, db_index=True, null=True, blank=True)
	Zone = models.CharField(max_length=15, db_index=True, null=True, blank=True)
	Name = models.CharField(max_length=20)
	Label = models.CharField(max_length=50)
	Type = models.CharField(max_length=10, choices=Choices.CUSTOM_TYPE)
	Value = models.CharField(max_length=200)
	ValueComplex = models.TextField()
	Class = models.CharField(max_length=20, null=True, blank=True)
	Delete = models.BooleanField(default=False)
	DateCreate = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	DateModify = models.DateTimeField(auto_now=True, null=True, blank=True)
	UserCreateId = models.IntegerField(null=True, blank=True)
	UserModifyId = models.IntegerField(null=True, blank=True)
	objects = DeleteManager()
	objects_del = models.Manager()
	def __unicode__(self):
		return str(self.Name)
	class Meta:
		db_table = 'HR_CUSTOM'

##########################################################################################3



