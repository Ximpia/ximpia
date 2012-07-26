import constants as K
from django.utils.translation import ugettext as _

class Choices(object):
	# MSG_MEDIA
	MSG_MEDIA = (
			(K.XIMPIA,'Ximpia'),
			(K.TWITTER,'Twitter'),
			(K.FACEBOOK,'Facebook'),
			(K.LINKEDIN,'LinkedIn'),
			(K.EMAIL,'Email'),
			('sms','SMS'),
			)
	# MSG_PREFERRED
	MSG_PREFERRED = (
			(K.XIMPIA,'Ximpia'),
			(K.TWITTER,'Twitter'),
			(K.FACEBOOK,'Facebook'),
			(K.LINKEDIN,'LinkedIn'),
			(K.EMAIL,'Email'),
			)
	# SOCIAL_NETS
	SOCIAL_NETS = (
		(K.TWITTER,'Twitter'),
		(K.FACEBOOK,'Facebook'),
		(K.LINKEDIN,'LinkedIn'),
		(K.LINKEDIN,'Xing'),
		(K.GOOGLE,'Google'),
		)
	# COUNTRY
	COUNTRY = (
		('fr', _('France')),
		('es', _('Spain')),
		('us', _('United States')),
		('ag', _('Antigua and Barbuda')),
		('ai', _('Angilla')),
		('al', _('Albania')),
		('am', _('Armenia')),
		('an', _('Netherlands Antilles')),
		('ao', _('Angola')),
		('aq', _('Antartica')),
		('ar', _('Argentina')),
		('as', _('American Samoa')),
		('at', _('Australia')),
		('aw', _('Aruba')),
		('ax', _('Aland Islands')),
		('az', _('Azerbaijan')),
		('ba', _('Bosnia and Herzegovina')),
		('bb', _('Barbados')),
		('bd', _('Bangladesh')),
		('be', _('Belgium')),
		('bf', _('Burkina Faso')),		
		)
	MSG_LOG_ACTION_READ = 'read'
	MSG_LOG_ACTION_DOWNLOAD = 'download'
	MSG_LOG_ACTION = (
			(MSG_LOG_ACTION_READ,_('Read')),
			(MSG_LOG_ACTION_DOWNLOAD, _('File Download')),
			)
	# FOLLOW_STATUS
	FOLLOW_STATUS = (
			(K.OK,'Ok'),
			(K.BLOCKED, _('Blocked')),
			(K.UNBLOCKED, _('UnBlocked')),
			)
	# CONTACT_SOURCE
	CONTACT_SOURCE = (
			(K.TWITTER,'Twitter'),
			(K.FACEBOOK,'Facebook'),
			(K.LINKEDIN,'LinkedIn'),
			(K.IMPORT, _('Imported')),
			(K.GMAIL,'Gmail'),
			(K.YAHOO,'Yahoo'),
			(K.MSN,'MSN'),
			)
	# ADDRESS_TYPE
	ADDRESS_TYPE_BILL = 'bill'
	ADDRESS_TYPE_SHIP = 'ship'
	ADDRESS_TYPE_HOME = 'home'
	ADDRESS_TYPE_OTHER = 'other'
	ADDRESS_TYPE = (
		(ADDRESS_TYPE_BILL, _('Billing')),
		(ADDRESS_TYPE_SHIP, _('Shipping & Handling')),
		(ADDRESS_TYPE_HOME, _('Home')),
		(ADDRESS_TYPE_SHIP, _('Other')),
		)
	# SCHDULE
	SCHEDULE_FULL = 'full'
	SCHEDULE_PART = 'part'
	SCHEDULE = (
		(SCHEDULE_FULL, _('Full Time')),
		(SCHEDULE_PART, _('Part Time')),
			)
	# CONTRACT_TYPE
	CONTRACT_TYPE_REGULAR = 'regular'
	CONTRACT_TYPE_TEMP = 'temporary'
	CONTRACT_TYPE = (
			(CONTRACT_TYPE_REGULAR, _('Regular')),
			(CONTRACT_TYPE_TEMP, _('Temporary')),
				)
	# STATUS
	STATUS_SELF = 'self'
	STATUS_EMPLOYEE = 'employee'
	STATUS_DIRECTOR = 'director'
	STATUS_CONTRACTOR = 'contractor'
	STATUS = (
		(STATUS_SELF, _('Self Employed')),
		(STATUS_EMPLOYEE, _('Employee')),
		(STATUS_DIRECTOR, _('Director')),
		(STATUS_CONTRACTOR, _('Contractor')),
			)
	# SALUTATION
	SALUTATION_MR = 'mr'
	SALUTATION_MS = 'ms'
	SALUTATION_DR = 'dr'
	SALUTATION = (
			(SALUTATION_MR, _('Mr.')),
			(SALUTATION_MS, _('Miss')),
			(SALUTATION_DR, _('Dr.')),
			)
	# CONTACT_COMM
	CONTACT_COMM = (
		(K.EMAIL, 'Email'),
		(K.HOME, _('Home Phone')),
		(K.WORK, _('Work Phone')),
		(K.MOBILE, _('Mobile')),
		(K.WORK_MOBILE, _('Work Mobile')),
		(K.FAX, 'Fax'),
		(K.NETWORK, _('Social Network')),
		(K.SITE, _('Site')),
		(K.BLOG, _('Blog')),
		(K.FACEBOOK_PAGE, _('Facebook Page')),
		(K.IM, _('Instant Messenger')),
		)
	# MILITARY
	MILITARY_NA = 'na'
	MILITARY_COMPLETED = 'completed'
	MILITARY_PENDING = 'pending'
	MILITARY = (
		(MILITARY_NA, 'N/A'),
		(MILITARY_COMPLETED, _('Completed')),
		(MILITARY_PENDING, _('Pending')),
		)
	# ETHNIC
	ETHNIC_WHITE = 'white'
	ETHNIC = (
		(ETHNIC_WHITE, _('White/Causasian')),
		)
	# SUBSCRIPTION
	SUBSCRIPTION_TRIAL = 'trial'
	SUBSCRIPTION_VALID = 'valid'
	SUBSCRIPTION_NONE = 'None'
	SUBSCRIPTION = (
			(SUBSCRIPTION_TRIAL, _('30-Day Free Trial')),
			(SUBSCRIPTION_VALID, _('Valid')),
			(SUBSCRIPTION_NONE, _('None')),
			)
	# EDUCATION
	EDUCATION_DEGREE = 'degree'
	EDUCATION_COURSE = 'course'
	EDUCATION_CERT = 'cert'
	EDUCATION = (
		(EDUCATION_DEGREE, _('Degree')),
		(EDUCATION_COURSE, _('Course')),
		(EDUCATION_CERT, _('Certification')),
			)
	# COURSE_MEDIA
	COURSE_MEDIA_VIDEO = 'video'
	COURSE_MEDIA_PRESENTATION = 'slides'
	COURSE_MEDIA = (
		(COURSE_MEDIA_VIDEO, 'Video'),
		(COURSE_MEDIA_PRESENTATION, _('Presentation')),
		)
	# SEX
	SEX_MAN = 'male'
	SEX_WOMAN = 'female'
	SEX = (
		(SEX_MAN, _('Male')),
		(SEX_WOMAN, _('Female'))
		)
	# RELATIONSHIP
	SINGLE = 'single'
	IN_RELATIONSHIP = 'in_relationship'
	MARRIED = 'married'
	RELATIONSHIP = (
			(SINGLE, _('Single')),
			(IN_RELATIONSHIP, _('In a Relationship')),
			(MARRIED, _('Married')))
	# CUSTOM_TYPE
	CUSTOM_TYPE_INPUT = 'input'
	CUSTOM_TYPE_COMBO = 'combo'
	CUSTOM_TYPE = (
		(CUSTOM_TYPE_INPUT, 'Input'),
		(CUSTOM_TYPE_COMBO, 'Combo'),
		)
	# SKILL_TYPE
	SKILL_TYPE_TECH = 'tech'
	SKILL_TYPE_TEAM_WORK = 'team_work'
	SKILL_TYPE = (
		(SKILL_TYPE_TECH, _('Technical')),
		(SKILL_TYPE_TEAM_WORK, _('Team Work')),
		)
	# INDUSTRY
	INDUSTRY = (
		(101, _('Accounting')),
		(102, _('Airlines/Aviation')),
		(103, _('Alternative Dispute Resolution')),
		(104, _('Alternative Medicine')),
		(105, _('Animation')),
		(106, _('Apparel & Fashion')),
		(107, _('Architecture & Planning')),
		(108, _('Arts and Crafts')),
		(109, _('Automotive')),
		(110, _('Aviation & Aerospace')),
		(111, _('Banking')),
		(112, _('Biotechnology')),
		(113, _('Broadcast Media')),
		(114, _('Building Materials')),
		(115, _('Business Supplies and Equipment')),
		(116, _('Capital Markets')),
		(117, _('Chemicals')),
		(118, _('Civic & Social Organization')),
		(119, _('Civil Engineering')),
		(120, _('Commercial Real Estate')),
		(121, _('Computer & Network Security')),
		(122, _('Computer Games')),
		(123, _('Computer Hardware')),
		(124, _('Computer Networking')),
		(125, _('Computer Software')),
		(126, _('Construction')),
		(127, _('Consumer Electronics')),
		(128, _('Consumer Goods')),
		(129, _('Consumer Services')),
		(130, _('Cosmetics')),
		(131, _('Dairy')),
		(132, _('Defense & Space')),
		(133, _('Design')),		
		(134, _('Education Management')),
		(135, _('E-Learning')),
		(136, _('Electrical/Electronic Manufacturing')),
		(137, _('Entertainment')),
		(138, _('Environmental Services')),
		(139, _('Events Services')),
		(140, _('Executive Office')),
		(141, _('Facilities Services')),
		(142, _('Farming')),
		(143, _('Financial Services')),
		(144, _('Fine Art')),
		(145, _('Fishery')),
		(146, _('Food & Beverages')),
		(147, _('Food Production')),
		(148, _('Fund-Raising')),
		(149, _('Furniture')),
		(150, _('Gambling & Casinos')),
		(151, _('Glass, Ceramics & Concrete')),
		(152, _('Government Administration')),
		(153, _('Government Relations')),
		(154, _('Graphic Design')),
		(155, _('Health, Wellness and Fitness')),
		(156, _('Higher Education')),
		(157, _('Hospital & Health Care')),
		(158, _('Hospitality')),
		(159, _('Human Resources')),
		(160, _('Import and Export')),
		(161, _('Individual & Family Services')),
		(162, _('Industrial Automation')),
		(163, _('Information Services')),
		(164, _('Information Technology and Services')),
		(165, _('Insurance')),
		(166, _('International Affairs')),
		(167, _('International Trade and Development')),
		(168, _('Internet')),
		(169, _('Investment Banking')),
		(170, _('Investment Management')),
		(171, _('Judiciary')),
		(172, _('Law Enforcement')),
		(173, _('Law Practice')),
		(174, _('Legal Services')),
		(175, _('Legislative Office')),
		(176, _('Leisure, Travel & Tourism')),
		(177, _('Libraries')),
		(178, _('Logistics and Supply Chain')),
		(179, _('Luxury Goods & Jewelry')),
		(180, _('Machinery')),
		(181, _('Management Consulting')),
		(182, _('Maritime')),
		(183, _('Marketing and Advertising')),
		(184, _('Market Research')),
		(185, _('Mechanical or Industrial Engineering')),
		(186, _('Media Production')),
		(187, _('Medical Devices')),
		(188, _('Medical Practice')),
		(189, _('Mental Health Care')),
		(190, _('Military')),
		(191, _('Mining & Metals')),
		(192, _('Motion Pictures and Film')),
		(193, _('Museums and Institutions')),
		(194, _('Music')),
		(195, _('Nanotechnology')),
		(196, _('Newspapers')),
		(197, _('Non-Profit Organization Management')),
		(198, _('Oil & Energy')),
		(199, _('Online Media')),
		(200, _('Outsourcing/Offshoring')),
		(201, _('Package/Freight Delivery')),
		(202, _('Packaging and Containers')),
		(203, _('Paper & Forest Products')),
		(204, _('Performing Arts')),
		(205, _('Pharmaceuticals')),
		(206, _('Philanthropy')),
		(207, _('Photography')),
		(208, _('Plastics')),
		(209, _('Political Organization')),
		(210, _('Primary/Secondary Education')),
		(211, _('Printing')),
		(212, _('Professional Training & Coaching')),
		(213, _('Program Development')),
		(214, _('Public Policy')),
		(215, _('Public Relations and Communications')),
		(216, _('Public Safety')),
		(217, _('Publishing')),
		(218, _('Railroad Manufacture')),
		(219, _('Ranching')),
		(220, _('Real Estate')),
		(221, _('Recreational Facilities and Services')),
		(222, _('Religious Institutions')),
		(223, _('Renewables &amp; Environment')),
		(224, _('Research')),
		(225, _('Restaurants')),
		(226, _('Retail')),
		(227, _('Security and Investigations')),
		(228, _('Semiconductors')),
		(229, _('Shipbuilding')),
		(230, _('Sporting Goods')),
		(240, _('Sports')),
		(250, _('Staffing and Recruiting')),
		(251, _('Supermarkets')),
		(252, _('Telecommunications')),
		(253, _('Textiles')),
		(254, _('Think Tanks')),
		(255, _('Tobacco')),
		(256, _('Translation and Localization')),
		(257, _('Transportation/Trucking/Railroad')),
		(258, _('Utilities')),
		(259, _('Venture Capital & Private Equity')),
		(260, _('Veterinary')),
		(261, _('Warehousing')),
		(262, _('Wholesale')),
		(263, _('Wine and Spirits')),
		(264, _('Wireless')),
		(265, _('Writing and Editing')),
		)
	JOB_CANDIDATE_PENDING = 'pending'
	JOB_CANDIDATE_STATUS = (
			(JOB_CANDIDATE_PENDING, _('Pending')),
			)
	JOB_CONTRACT = ()
	# INVITATION STATUS
	INVITATION_STATUS = (
		(K.PENDING, _('Pending')),
		(K.USED, _('Used')),
			)
	# CALENDAR TYPE
	CALENDAR_TYPE_BIRTHDAY = 'birthday'
	CALENDAR_TYPE_ANNIVERSARY = 'anniversary'
	CALENDAR_TYPE = (
		('meeting', _('Meeting')),
		('event', _('Event')),
		('birthday', _('Birthday')),
		('anniversary', _('Anniversary')),
		('appointment', _('Appointment')),
			)
	# CALENDAR REPEAT
	CALENDAR_REPEAT_YEARLY = 'yearly'
	CALENDAR_REPEAT = (
		('daily', _('Daily')),
		('weekly', _('Weekly')),
		('monthly', _('Monthly')),
		('yearly', _('Yearly')),
			)
	# CALENDAR_INVITE_STATUS
	CALENDAR_INVITE_STATUS_PENDING = K.PENDING
	CALENDAR_INVITE_STATUS = (
		(K.PENDING, _('Pending')),
		('accepted', _('Accepted')),
		('declined', _('Declined')),
			)
	# TASK_FINISH_TYPE
	TASK_FINISH_TYPE_DEFAULT = 'all'
	TASK_FINISH_TYPE = (
		('all', _('All')),
		('any', _('Any')),
			)
	# TASK_STATUS
	TASK_STATUS_DEFAULT = 'notStarted'
	TASK_STATUS = (
		('notStarted', _('Not Started')),
		('inProgress', _('In Progress')),
		('completed', _('Completed')),
		('waiting', _('Waiting')),
		('deferred', _('Deferred')),
		)
	# SUBSCRIPTION ITEMS
	SUBSCRIPTION_ITEMS = (
		('sms', 'SMS'),
		)
	# FILE TYPES
	FILE_TYPE = (
				('pdf', 'Pdf'),
				('word', 'Word')
				)
	# INVITATION TYPE
	"""INVITATION_TYPE_ORDINARY = 'ordinary'
	INVITATION_TYPE_PROMOTION = 'promotion'
	INVITATION_TYPE = (
				(INVITATION_TYPE_ORDINARY, _('Ordinary')),
				(INVITATION_TYPE_PROMOTION, _('Promotion'))
				)"""
	# INVITATION_ACC_TYPE
	INVITATION_ACC_TYPE_USER = 'user'
	INVITATION_ACC_TYPE_ORG = 'organization'
	INVITATION_ACC_TYPE = (
				(INVITATION_ACC_TYPE_USER, _('User')),
				(INVITATION_ACC_TYPE_ORG, _('Organization'))
				)
				
	# INVITATION_PAY_TYPE
	INVITATION_PAY_TYPE_FREE = 'free'
	INVITATION_PAY_TYPE_PAY = 'pay'
	INVITATION_PAY_TYPE_PROMOTION = 'promotion'
	INVITATION_PAY_TYPE = (
				(INVITATION_PAY_TYPE_FREE, _('Free')),
				(INVITATION_PAY_TYPE_PAY, _('Pay')),
				(INVITATION_PAY_TYPE_PROMOTION, _('Promotion'))
			)
	# ACCOUNT_TYPE
	ACCOUNT_TYPE_ORDINARY = 'ordinary'
	ACCOUNT_TYPE_PROMOTION = 'promotion'
	ACCOUNT_TYPE = (
				('ordinary', _('Ordinary')),
				('promotion', _('Promotion'))
				)
	# LANG
	LANG_ENGLISH = 'en'
	LANG = (
			('en', _('English')),
			('es', _('Spanish')))
	# ORG GROUPS
	ORG_GROUPS = (
				(1, _('Management')),
				(2, _('Engineering')),
				(3, _('Sales')),
				(4, _('Customer Support')),
				(5, _('Finance')),
				(6, _('Software Development')),
				(7, _('Legal')),
				)
	# JOB TITLES
	JOB_TITLES = (
				(1, _('Project Manager')),
				(2, _('CEO')),
				(3, _('Founder')),
				(4, _('CFO')),
				(5, _('Director')),
				(6, _('Manager')),
				(7, _('Sales Director')),
				(8, _('Marketing Director')),
				)
	# PARAM_TYPE
	PARAM_TYPE = (
				('param', _('Parameter')),
				('table', _('Table')),
				)
