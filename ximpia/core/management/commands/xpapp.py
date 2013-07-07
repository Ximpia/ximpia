import os

from string import Template
from django.utils.crypto import get_random_string

from django.core.management.base import BaseCommand, CommandError
from django.utils.translation import ugettext as _

import ximpia.core

class Command(BaseCommand):
	args = '<full_app_name>'
	help = """Creates ximpia app directories and files
	Attributes
	- full_app_name: project_name.app_name. Example my_project.my_app
	"""

	"""
	args
	app: ximpia_site.web (project_name.app_name)
	
	1. Check if project exists. If not, create project structure 

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

	def __create_project(self, project_name, app_name):
		"""
			my_project
				manage.py
				my_project
					__init__.py
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
		with open(project_name + '/' + project_name + '/' + '__init__.py', 'w') as f:
			f.write('')
		# settings_local
		with open(self.core_src_path + '/project/' + 'settings_local.py.txt', 'r') as f:
			settings_local = f.read()
		# substitutions for settings local
		settings_local = Template(settings_local).substitute(project_name=project_name,
															db_engine=raw_input('Db Engine: <mysql> ') or 'mysql',
															db_host=raw_input('Db Host: '),
															db_name=raw_input('Db Name: '),
															db_user=raw_input('Db User: '),
															db_password=raw_input('Db Password: '))
		with open(project_name + '/' + project_name + '/' + 'settings_local.py', 'w') as f:
			f.write(settings_local)
		# settings
		# get settings and settings_local file from core sources
		with open(self.core_src_path + '/project/' + 'settings.py.txt', 'r') as f:
			settings = f.read()
		# substitutions for settings
		chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
		settings = Template(settings).substitute(project_name=project_name,
												app_name=app_name,
												admin_name=raw_input('Admin Name: '),
												admin_email=raw_input('Admin Email: '),
												time_zone=raw_input('Timezone: <America/Chicago> ') or 'America/Chicago',
												language_code=raw_input('Language code <en-us> : ') or 'en-us',
												project_title=project_name.replace('_', ' ').capitalize(),
												project_path=self.project_path,
												secret_key=get_random_string(50, chars))
		with open(project_name + '/' + project_name + '/' + 'settings.py', 'w') as f:
			f.write(settings)
		# get urls file from core sources
		with open(self.core_src_path +  '/project' + '/' + 'urls.py.txt', 'r') as f:
			urls = f.read()
		urls = urls.replace('$project_name', project_name)
		with open(project_name + '/' + project_name + '/' + 'urls.py', 'w') as f:
			f.write(urls)
		# get wsgi file from core sources
		with open(self.core_src_path +  '/project' + '/' + 'wsgi.py.txt', 'r') as f:
			wsgi = f.read()
		wsgi = wsgi.replace('$project_name', project_name)
		with open(project_name + '/' + project_name + '/' + 'wsgi.py', 'w') as f:
			f.write(wsgi)
		self.stdout.write(_('Created project {}'.format(project_name)))

	def __create_app_dirs(self, app_name):
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

	def __create_app_files(self, app_name):
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
			f.write(components)
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
			f.write(views)

	def handle(self, *args, **options):
		if len(args) != 1:
			raise CommandError(_('You must inform full application name like manage.py xpapp my_project.my_app'))
		full_app_name = args[0]
		self.stdout.write('This command will create project, app, directory structure, etc--- {}'.format(full_app_name))
		project_name, app_name = full_app_name.split('.')
		self.project_name = project_name
		self.project_path = os.getcwd() + '/' + project_name + '/' + project_name
		self.core_src_path = ximpia.core.__path__[0] + '/sources'
		if not os.path.isdir(project_name):
			self.__create_project(project_name, app_name)
		self.__create_app_dirs(app_name)
		self.__create_app_files(app_name)
