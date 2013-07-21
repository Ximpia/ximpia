import os
import sys
import shutil
import getpass

from string import Template
from django.utils.crypto import get_random_string
from distutils.sysconfig import get_python_lib

XIMPIA_CORE_PATH = get_python_lib() + '/ximpia/core'

class Command(object):
	db_engine = ''
	args = '<full_app_name>'
	help = """Creates ximpia app directories and files
	Attributes
	- full_app_name: project_name.app_name. Example my_project.my_app
	
	"""

	"""
	args
	app: ximpia_site.web (project_name.app_name)	

	Directory structure:
	- fixtures
	- migrations (package)
	- static
	- templates
	   - site
			   - popup
			   - window
	   - myapp
			   - popup
			   - window
	- tests
	
	Files:
	- __init__.py
	- business.py
	- components.py
	- constants.py
	- data.py
	- forms.py
	- messages.py
	- models.py
	- service.py
	- views.py
	"""

	def __feed_password(self):
		pprompt = lambda: (getpass.getpass(), getpass.getpass('Retype password: '))
		p1, p2 = pprompt()
		while p1 != p2:
			print('Passwords do not match. Try again')
			p1, p2 = pprompt()
		return p1

	def create_project(self, project_name, app_name):
		"""
			my_project
				manage.py
				my_project
					init__.py
					settings.py
					urls.py
					wsgi.py
			
			**Attributes**
			
			* ``project_name``(str) : Project name
			
			**Returns**
			None
		"""
		os.mkdir(project_name)
		os.mkdir(project_name + '/' + project_name)
		# manage.py file...
		with open(self.core_src_path + '/project/' + 'manage.py.txt', 'r') as f:
			manage = f.read()
		manage = manage.replace('$project_name', project_name)
		with open(project_name + '/manage.py', 'w') as f:
			f.write(manage)
		os.chmod(project_name + '/manage.py', 0755)
		with open(project_name + '/' + project_name + '/' + '__init__.py', 'w') as f:
			f.write('')
		# settings_local
		with open(self.core_src_path + '/project/' + 'settings_local.py.txt', 'r') as f:
			settings_local = f.read()
		# substitutions for settings local
		db_engine = raw_input('Db Engine: <mysql> ') or 'mysql'
		settings_local = Template(settings_local).substitute(project_name=project_name,
															db_engine=db_engine,
															db_host=raw_input('Db Host: '),
															db_name=raw_input('Db Name: '),
															db_user=raw_input('Db User: '),
															db_password=self.__feed_password())
		self.db_engine = db_engine
		with open(project_name + '/' + project_name + '/' + 'settings_local.py', 'w') as f:
			f.write(settings_local)
		# settings
		# get settings and settings_local file from core sources
		with open(self.core_src_path + '/project/' + 'settings.py.txt', 'r') as f:
			settings = f.read()
		# substitutions for settings
		chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
		self.project_title = project_name.replace('_', ' ').capitalize()
		settings = Template(settings).substitute(project_name=project_name,
												app_name=app_name,
												admin_name=raw_input('Admin Name: '),
												admin_email=raw_input('Admin Email: '),
												time_zone=raw_input('Timezone: <America/Chicago> ') or 'America/Chicago',
												language_code=raw_input('Language code <en-us> : ') or 'en-us',
												project_title=self.project_title,
												project_path=self.project_path,
												secret_key=get_random_string(50, chars))
		with open(project_name + '/' + project_name + '/' + 'settings.py', 'w') as f:
			f.write(settings)
		# get urls file from core sources
		with open(self.core_src_path +  '/project' + '/' + 'urls.py.txt', 'r') as f:
			urls = f.read()
		urls = urls.replace('$project_name', project_name)
		urls = urls.replace('$app_name', app_name)
		with open(project_name + '/' + project_name + '/' + 'urls.py', 'w') as f:
			f.write(urls)
		# get wsgi file from core sources
		with open(self.core_src_path +  '/project' + '/' + 'wsgi.py.txt', 'r') as f:
			wsgi = f.read()
		wsgi = wsgi.replace('$project_name', project_name)
		with open(project_name + '/' + project_name + '/' + 'wsgi.py', 'w') as f:
			f.write(wsgi)
		print 'Created project {}'.format(project_name)

	def create_app_dirs(self, app_name):
		"""
			Create directories...
			Directory structurefor app:
			- fixtures
			- migrations (package)
			- static
			- templates
			   - site
					   - popup
					   - window
			   - myapp
					   - popup
					   - window
			- tests
		"""
		if not os.path.isdir(self.project_path + '/static/media'):
			os.makedirs(self.project_path + '/static/media')
		if not os.path.isdir(self.project_path + '/' + app_name):
			os.mkdir(self.project_path + '/' + app_name)
		if not os.path.isdir(self.project_path + '/' + app_name + '/fixtures'):
			os.mkdir(self.project_path + '/' + app_name + '/fixtures')
		if not os.path.isdir(self.project_path + '/' + app_name + '/migrations'):
			os.mkdir(self.project_path + '/' + app_name + '/migrations')
		if not os.path.isdir(self.project_path + '/' + app_name + '/static'):
			os.mkdir(self.project_path + '/' + app_name + '/static')
		if not os.path.isdir(self.project_path + '/' + app_name + '/static/images'):
			os.mkdir(self.project_path + '/' + app_name + '/static/images')
		if not os.path.isdir(self.project_path + '/' + app_name + '/static/' + app_name):
			os.mkdir(self.project_path + '/' + app_name + '/static/' + app_name)
		if not os.path.isdir(self.project_path + '/' + app_name + '/static/' + app_name+ '/css'):
			os.mkdir(self.project_path + '/' + app_name + '/static/' + app_name + '/css')
		if not os.path.isdir(self.project_path + '/' + app_name + '/static/' + app_name + '/images'):
			os.mkdir(self.project_path + '/' + app_name + '/static/' + app_name + '/images')
		if not os.path.isdir(self.project_path + '/' + app_name + '/static/' + app_name + '/scripts'):
			os.mkdir(self.project_path + '/' + app_name + '/static/' + app_name + '/scripts')
		if not os.path.isdir(self.project_path + '/' + app_name + '/templates'):
			os.mkdir(self.project_path + '/' + app_name + '/templates')
		if not os.path.isdir(self.project_path + '/' + app_name + '/templates/site'):
			os.mkdir(self.project_path + '/' + app_name + '/templates/site')
		if not os.path.isdir(self.project_path + '/' + app_name + '/templates/site/popup'):
			os.mkdir(self.project_path + '/' + app_name + '/templates/site/popup')
		if not os.path.isdir(self.project_path + '/' + app_name + '/templates/site/window'):
			os.mkdir(self.project_path + '/' + app_name + '/templates/site/window')
		if not os.path.isdir(self.project_path + '/' + app_name + '/templates/' + app_name):
			os.mkdir(self.project_path + '/' + app_name + '/templates/' + app_name)
		if not os.path.isdir(self.project_path + '/' + app_name + '/templates/' + app_name + '/popup'):
			os.mkdir(self.project_path + '/' + app_name + '/templates/' + app_name + '/popup')
		if not os.path.isdir(self.project_path + '/' + app_name + '/templates/' + app_name + '/window'):
			os.mkdir(self.project_path + '/' + app_name + '/templates/' + app_name + '/window')
		if not os.path.isdir(self.project_path + '/' + app_name + '/tests'):
			os.mkdir(self.project_path + '/' + app_name + '/tests')

	def create_app_files(self, app_name):
		"""
			Create app files...
			Files:
			- __init__.py
			- business.py
			- components.py
			- constants.py
			- choices.py
			- data.py
			- forms.py
			- messages.py
			- models.py
			- service.py
			- views.py
		"""
		with open(self.project_path + '/' + app_name + '/' + '__init__.py', 'w') as f:
			f.write('')
		with open(self.project_path + '/' + app_name + '/' + 'business.py', 'w') as f:
			f.write('')
		# components
		with open(self.core_src_path + '/app/' + 'components.py.txt', 'r') as f:
			components = f.read()
		with open(self.project_path + '/' + app_name + '/' + 'components.py', 'w') as f:
			f.write(Template(components).substitute(project_title=self.project_title, project_name=self.project_name))
		# constants
		with open(self.project_path + '/' + app_name + '/' + 'constants.py', 'w') as f:
			f.write('')
		# choices
		with open(self.core_src_path + '/app/' + 'choices.py.txt', 'r') as f:
			choices = f.read()
		with open(self.project_path + '/' + app_name + '/' + 'choices.py', 'w') as f:
			f.write(choices)
		# data
		with open(self.core_src_path + '/app/' + 'data.py.txt', 'r') as f:
			data = f.read()
		with open(self.project_path + '/' + app_name + '/' + 'data.py', 'w') as f:
			f.write(data)
		# forms
		with open(self.core_src_path + '/app/' + 'forms.py.txt', 'r') as f:
			forms = f.read()
		with open(self.project_path + '/' + app_name + '/' + 'forms.py', 'w') as f:
			f.write(forms)
		# messages
		with open(self.core_src_path + '/app/' + 'messages.py.txt', 'r') as f:
			messages = f.read()
		with open(self.project_path + '/' + app_name + '/' + 'messages.py', 'w') as f:
			f.write(messages)
		# models
		with open(self.core_src_path + '/app/' + 'models.py.txt', 'r') as f:
			models = f.read()
		with open(self.project_path + '/' + app_name + '/' + 'models.py', 'w') as f:
			f.write(models)
		# service
		with open(self.core_src_path + '/app/' + 'service.py.txt', 'r') as f:
			service = f.read()
		with open(self.project_path + '/' + app_name + '/' + 'service.py', 'w') as f:
			f.write(service)
		# views
		with open(self.core_src_path + '/app/' + 'views.py.txt', 'r') as f:
			views = f.read()
		with open(self.project_path + '/' + app_name + '/' + 'views.py', 'w') as f:
			f.write(Template(views).substitute(project_name=self.project_name))
		# tests
		with open(self.core_src_path + '/app/' + 'tests.py.txt', 'r') as f:
			tests = f.read()
		with open(self.project_path + '/' + app_name + '/' + 'tests/tests.py', 'w') as f:
			f.write(tests)
		# templates
		if not os.path.isfile(self.project_path + '/' + app_name + '/' + 'templates/site/popup/change_password.html'):
			# site
			tmpl_src = self.core_src_path + '/app/templates/site/'
			tmpl_dst = self.project_path + '/' + app_name + '/templates/site/'
			shutil.copyfile(tmpl_src + 'popup/change_password.html', tmpl_dst + 'popup/change_password.html')
			shutil.copyfile(tmpl_src + 'popup/password_reminder.html', tmpl_dst + 'popup/password_reminder.html')
			shutil.copyfile(tmpl_src + 'window/activation_user.html', tmpl_dst + 'window/activation_user.html')
			shutil.copyfile(tmpl_src + 'window/home_login.html', tmpl_dst + 'window/home_login.html')
			shutil.copyfile(tmpl_src + 'window/login.html', tmpl_dst + 'window/login.html')
			shutil.copyfile(tmpl_src + 'window/logout.html', tmpl_dst + 'window/logout.html')
			shutil.copyfile(tmpl_src + 'window/reminder_new_password.html', tmpl_dst + 'window/reminder_new_password.html')
			shutil.copyfile(tmpl_src + 'window/signup.html', tmpl_dst + 'window/signup.html')
			shutil.copyfile(tmpl_src + 'site.html', tmpl_dst + 'site.html')
			# app
			tmpl_src = self.core_src_path + '/app/templates/app/'
			tmpl_dst = self.project_path + '/' + app_name + '/templates/' + app_name + '/'
			shutil.copyfile(tmpl_src + 'app.html', tmpl_dst + app_name + '.html')
			# TODO: create home template with name of app in big grey letters
			with open(self.core_src_path + '/app/' + 'templates/app/window/home.html', 'r') as f:
				home = f.read()
			with open(self.project_path + '/' + app_name + '/' + 'templates/' + app_name + '/window/home.html', 'w') as f:
				f.write(Template(home).substitute(app_name=app_name))
		# images
		img_src = self.core_src_path + '/images/'
		img_dst = self.project_path + '/' + app_name + '/static/images/'
		if os.path.isfile(img_src + 'logo.png'):
			shutil.copyfile(img_src + 'logo.png', img_dst + 'logo.png')

	def create_fixtures(self, app_name):
		"""
			Create fixtures initial_data.json and site_additional.json files
		"""
		'''with open(self.project_path + '/' + app_name + '/' + 'fixtures/initial_data.json', 'w') as f:
			f.write('')'''
		with open(self.project_path + '/' + app_name + '/' + 'fixtures/site_additional.json', 'w') as f:
			f.write('[]')
		# Home: Group, Application, Service, View, XpTemplate
		# Write fixture based on data
		# project_name, app_name, date_now, user_id, project_title, app_slug, group_id
		# date: "2013-06-16T16:34:32"

	def handle(self, *args, **options):
		if len(args) != 1:
			raise CommandError(_('You must inform full application name like manage.py xpapp my_project.my_app'))
		full_app_name = args[0]
		self.stdout.write('This command will create project, app, directory structure, etc--- {}'.format(full_app_name))
		project_name, app_name = full_app_name.split('.')
		self.project_name = project_name
		self.project_path = os.getcwd() + '/' + project_name + '/' + project_name
		self.core_src_path = XIMPIA_CORE_PATH + '/sources'
		if not os.path.isdir(project_name):
			self.create_project(project_name, app_name)
		self.create_app_dirs(app_name)
		self.create_app_files(app_name)
		self.create_fixtures(app_name)
		# create home template with name of app in big grey letters

#python ../ximpia/ximpia/bin/ximpia-app.py myproject.myapp

if __name__ == "__main__":
	args = sys.argv[1:]
	msg = ''
	if len(args) != 1:
		print 'You must inform full application name like ximpia-app my_project.my_app'
		sys.exit()
	full_app_name = args[0]
	print 'This command will create project, app, directory structure, etc--- {}'.format(full_app_name)
	project_name, app_name = full_app_name.split('.')
	command = Command()
	command.project_name = project_name
	command.project_path = os.getcwd() + '/' + project_name + '/' + project_name
	command.core_src_path = XIMPIA_CORE_PATH + '/sources'
	if not os.path.isdir(project_name):
		command.create_project(project_name, app_name)
	else:
		print 'Project already exists'
		sys.exit()
	command.create_app_dirs(app_name)
	command.create_app_files(app_name)
	command.create_fixtures(app_name)
	# Create tables, first syncdb, migration, etc...
	print './{}/manage.py syncdb'.format(project_name)
	os.system('./{}/manage.py syncdb'.format(project_name))
	print './{}/manage.py migrate ximpia.core'.format(project_name)
	os.system('./{}/manage.py migrate ximpia.core'.format(project_name))
	print './{}/manage.py migrate ximpia.site'.format(project_name)
	os.system('./{}/manage.py migrate ximpia.site'.format(project_name))
	# Import site and app components
	os.system('./{}/manage.py xpcomponents ximpia.site'.format(project_name))
	os.system('./{}/manage.py xpcomponents myproject.myapp'.format(project_name))
	os.system('./{}/manage.py customdashboard'.format(project_name))
	if os.path.isfile('dashboard.py'):
		shutil.move('dashboard.py', '{}/{}/dashboard.py'.format(project_name, project_name))
