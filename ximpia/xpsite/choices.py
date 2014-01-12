# coding: utf-8

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
            (K.SMS,'SMS'),
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
        (K.XING,'Xing'),
        (K.GOOGLE,'Google'),
        )
    # COUNTRY
    COUNTRY = (
        ('ad', _(u'Andorra')),
        ('ae', _(u'United Arab Emirates')),
        ('af', _(u'Afghanistan')),
        ('ag', _(u'Antigua and Barbuda')),
        ('ai', _(u'Anguilla')),
        ('al', _(u'Albania')),
        ('am', _(u'Armenia')),
        ('ao', _(u'Angola')),
        ('aq', _(u'Antarctica')),
        ('ar', _(u'Argentina')),
        ('as', _(u'American Samoa')),
        ('at', _(u'Austria')),
        ('au', _(u'Australia')),
        ('aw', _(u'Aruba')),
        ('ax', _(u'Aland Islands')),
        ('az', _(u'Azerbaijan')),
        ('ba', _(u'Bosnia and Herzegovina')),
        ('bb', _(u'Barbados')),
        ('bd', _(u'Bangladesh')),
        ('be', _(u'Belgium')),
        ('bf', _(u'Burkina Faso')),
        ('bg', _(u'Bulgaria')),
        ('bh', _(u'Bahrain')),
        ('bi', _(u'Burundi')),
        ('bj', _(u'Benin')),
        ('bl', _(u'Saint Barthélemy')),
        ('bm', _(u'Bermuda')),
        ('bn', _(u'Brunei Darussalam')),
        ('bo', _(u'Bolivia')),
        ('bq', _(u'Bonaire')),
        ('br', _(u'Brazil')),
        ('bs', _(u'Bahamas')),
        ('bt', _(u'Bhutan')),
        ('bv', _(u'Bouvet Island')),
        ('bw', _(u'Botswana')),
        ('by', _(u'Belarus')),
        ('bz', _(u'Belize')),
        ('ca', _(u'Canada')),
        ('cc', _(u'Cocos (Keeling) Islands')),
        ('cd', _(u'Congo, the Democratic Republic of the')),
        ('cf', _(u'Central African Republic')),
        ('cg', _(u'Congo')),
        ('ch', _(u'Switzerland')),
        ('ci', _(u'Cote d Ivoire')),
        ('ck', _(u'Cook Islands')),
        ('cl', _(u'Chile')),
        ('cm', _(u'Cameroon')),
        ('ch', _(u'China')),
        ('co', _(u'Colombia')),
        ('cr', _(u'Costa Rica')),
        ('cu', _(u'Cuba')),
        ('cv', _(u'Cape Verde')),
        ('cw', _(u'Curaçao')),
        ('cx', _(u'Christmas Island')),
        ('cy', _(u'Cyprus')),
        ('cz', _(u'Czech Republic')),
        ('de', _(u'Germany')),
        ('dj', _(u'Djibouti')),
        ('dk', _(u'Denmark')),
        ('dm', _(u'Dominica')),
        ('do', _(u'Dominican Republic')),
        ('dz', _(u'Algeria')),
        ('ec', _(u'Ecuador')),
        ('ee', _(u'Estonia')),
        ('eg', _(u'Egypt')),
        ('eh', _(u'Western Sahara')),
        ('er', _(u'Eritrea')),
        ('es', _(u'Spain')),
        ('et', _(u'Ethiopia')),
        ('fi', _(u'Finland')),
        ('fj', _(u'Fiji')),
        ('fk', _(u'Falkland Islands (Malvinas)')),
        ('fm', _(u'Micronesia')),
        ('fo', _(u'Faroe Islands')),
        ('fr', _(u'France')),
        ('ga', _(u'Gabon')),
        ('gb', _(u'United Kingdom')),
        ('gd', _(u'Grenada')),
        ('ge', _(u'Georgia')),
        ('gf', _(u'French Guiana')),
        ('gg', _(u'Guernsey')),
        ('gh', _(u'Ghana')),
        ('gi', _(u'Gibraltar')),
        ('gl', _(u'Greenland')),
        ('gm', _(u'Gambia')),
        ('gn', _(u'Guinea')),
        ('gp', _(u'Guadeloupe')),
        ('gq', _(u'Equatorial Guinea')),
        ('gr', _(u'Greece')),
        ('gs', _(u'South Georgia')),
        ('gt', _(u'Guatemala')),
        ('gu', _(u'Guam')),
        ('gw', _(u'Guinea-Bissau')),
        ('gy', _(u'Guyana')),
        ('hk', _(u'Hong Kong')),
        ('hm', _(u'Heard Island')),
        ('hn', _(u'Honduras')),
        ('hr', _(u'Croatia')),
        ('ht', _(u'Haiti')),
        ('hu', _(u'Hungary')),
        ('id', _(u'Indonesia')),
        ('ie', _(u'Ireland')),
        ('il', _(u'Israel')),
        ('im', _(u'Isle of Man')),
        ('in', _(u'India')),
        ('io', _(u'British Indian Ocean Territory')),
        ('iq', _(u'Iraq')),
        ('ir', _(u'Iran')),
        ('is', _(u'Iceland')),
        ('it', _(u'Italy')),
        ('je', _(u'Jersey')),
        ('jm', _(u'Jamaica')),
        ('jo', _(u'Jordan')),
        ('jp', _(u'Japan')),
        ('ke', _(u'Kenya')),
        ('kg', _(u'Kyrgyzstan')),
        ('kh', _(u'Cambodia')),
        ('ki', _(u'Kiribati')),
        ('km', _(u'Comoros')),
        ('kn', _(u'Saint Kitts and Nevis')),
        ('kp', _(u'Korea Democratic')),
        ('kr', _(u'Korea Republic')),
        ('kw', _(u'Kuwait')),
        ('ky', _(u'Cayman Islands')),
        ('kz', _(u'Kazakhstan')),
        ('la', _(u'Lao')),
        ('lb', _(u'Lebanon')),
        ('lc', _(u'Saint Lucia')),
        ('li', _(u'Liechtenstein')),
        ('lk', _(u'Sri Lanka')),
        ('lr', _(u'Liberia')),
        ('ls', _(u'Lesotho')),
        ('lt', _(u'Lithuania')),
        ('lu', _(u'Luxembourg')),
        ('lv', _(u'Latvia')),
        ('ly', _(u'Libya')),
        ('ma', _(u'Morocco')),
        ('mc', _(u'Monaco')),
        ('md', _(u'Moldova')),
        ('me', _(u'Montenegro')),
        ('mf', _(u'Saint Martin')),
        ('mg', _(u'Madagascar')),
        ('mh', _(u'Marshall Islands')),
        ('mk', _(u'Macedonia')),
        ('ml', _(u'Mali')),
        ('mm', _(u'Myanmar')),
        ('mn', _(u'Mongolia')),
        ('mo', _(u'Macao')),
        ('mp', _(u'Northern Mariana Islands')),
        ('mq', _(u'Martinique')),
        ('mr', _(u'Mauritania')),
        ('ms', _(u'Montserrat')),
        ('mt', _(u'Malta')),
        ('mu', _(u'Mauritius')),
        ('mv', _(u'Maldives')),
        ('mw', _(u'Malawi')),
        ('mx', _(u'Mexico')),
        ('my', _(u'Malaysia')),
        ('mz', _(u'Mozambique')),
        ('na', _(u'Namibia')),
        ('nc', _(u'New Caledonia')),
        ('ne', _(u'Niger')),
        ('nf', _(u'Norfolk Island')),
        ('ng', _(u'Nigeria')),
        ('ni', _(u'Nicaragua')),
        ('nl', _(u'Netherlands')),
        ('no', _(u'Norway')),
        ('np', _(u'Nepal')),
        ('nr', _(u'Nauru')),
        ('nu', _(u'Niue')),
        ('nz', _(u'New Zealand')),
        ('om', _(u'Oman')),
        ('pa', _(u'Panama')),
        ('pe', _(u'Peru')),
        ('pf', _(u'French Polynesia')),
        ('pg', _(u'Papua New Guinea')),
        ('ph', _(u'Philippines')),
        ('pk', _(u'Pakistan')),
        ('pl', _(u'Poland')),
        ('pm', _(u'Saint Pierre and Miquelon')),
        ('pn', _(u'Pitcairn')),
        ('pr', _(u'Puerto Rico')),
        ('ps', _(u'Palestine')),
        ('pt', _(u'Portugal')),
        ('pw', _(u'Palau')),
        ('py', _(u'Paraguay')),
        ('qa', _(u'Qatar')),
        ('re', _(u'Réunion')),
        ('ro', _(u'Romania')),
        ('rs', _(u'Serbia')),
        ('ru', _(u'Russian Federation')),
        ('rw', _(u'Rwanda')),
        ('sa', _(u'Saudi Arabia')),
        ('sb', _(u'Solomon Islands')),
        ('sc', _(u'Seychelles')),
        ('sd', _(u'Sudan')),
        ('se', _(u'Sweden')),
        ('sg', _(u'Singapore')),
        ('sh', _(u'Saint Helena')),
        ('si', _(u'Slovenia')),
        ('sj', _(u'Svalbard and Jan Mayen')),
        ('sk', _(u'Slovakia')),
        ('sl', _(u'Sierra Leone')),
        ('sm', _(u'San Marino')),
        ('sn', _(u'Senegal')),
        ('so', _(u'Somalia')),
        ('sr', _(u'Suriname')),
        ('ss', _(u'South Sudan')),
        ('st', _(u'Sao Tome and Principe')),
        ('sv', _(u'El Salvador')),
        ('sx', _(u'Sint Maarten (Dutch part)')),
        ('sy', _(u'Syrian Arab Republic')),
        ('sz', _(u'Swaziland')),
        ('tc', _(u'Turks and Caicos Islands')),
        ('td', _(u'Chad')),
        ('tf', _(u'French Southern Territories')),
        ('tg', _(u'Togo')),
        ('th', _(u'Thailand')),
        ('tj', _(u'Tajikistan')),
        ('tk', _(u'Tokelau')),
        ('tl', _(u'Timor-Leste')),
        ('tm', _(u'Turkmenistan')),
        ('tn', _(u'Tunisia')),
        ('to', _(u'Tonga')),
        ('tr', _(u'Turkey')),
        ('tt', _(u'Trinidad and Tobago')),
        ('tv', _(u'Tuvalu')),
        ('tw', _(u'Taiwan')),
        ('tz', _(u'Tanzania')),
        ('ua', _(u'Ukraine')),
        ('ug', _(u'Uganda')),
        ('um', _(u'United States Minor Outlying Islands')),
        ('us', _(u'United States')),
        ('uy', _(u'Uruguay')),
        ('uz', _(u'Uzbekistan')),
        ('va', _(u'Vatican City State')),
        ('vc', _(u'Saint Vincent and the Grenadines')),
        ('ve', _(u'Venezuela')),
        ('vg', _(u'Virgin Islands, British')),
        ('vi', _(u'Virgin Islands, U.S.')),
        ('vn', _(u'Viet Nam')),
        ('vu', _(u'Vanuatu')),
        ('wf', _(u'Wallis and Futuna')),
        ('ws', _(u'Samoa')),
        ('ye', _(u'Yemen')),
        ('yt', _(u'Mayotte')),
        ('za', _(u'South Africa')),
        ('zm', _(u'Zambia')),
        ('zw', _(u'Zimbabwe')),
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
    # CATEGORY_TYE
    CATEGORY_TYPE_DEFAULT = 'default'
    CATEGORY_TYPE = (
        (CATEGORY_TYPE_DEFAULT, _('Default')),
        )
    # USER_RELATIONSHIP
    ACCESS_RELATIONSHIP_OWNER = 'owner'
    ACCESS_RELATIONSHIP_ADMIN = 'admin'
    ACCESS_RELATIONSHIP_MANAGER = 'manager'
    ACCESS_RELATIONSHIP_USER = 'user'
    ACCESS_RELATIONSHIP = (
        (ACCESS_RELATIONSHIP_ADMIN, _('Admin')),
        (ACCESS_RELATIONSHIP_OWNER, _('Owner')),
        (ACCESS_RELATIONSHIP_MANAGER, _('Manager')),
        (ACCESS_RELATIONSHIP_USER, _('User')),
        )
