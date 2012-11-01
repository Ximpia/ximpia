import random
from ximpia import settings

# Logging
import logging.config
logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger(__name__)

class MasterSlaveRouter ( object ):
	def db_for_read(self, model, **hints):
		"Point all read operations to a random slave"
		names = settings.DATABASES.keys()
		slaves = []
		dbName = ''
		for name in names:
			if name.find('slave') == 0:
				slaves.append(name)
		if len(slaves) == 0:
			dbName = 'default'
		else:
			dbName = random.choice(slaves)
		dbName = 'default'
		#logger.debug( 'dbName: ' + dbName )
		return dbName
	def db_for_write(self, model, **hints):
		"Point all write operations to the master"
		names = settings.DATABASES.keys()
		masters = []
		dbName = ''
		for name in names:
			if name.find('master') == 0:
				masters.append(name)
		if len(masters) == 0:
			dbName = 'default'
		else:
			dbName = random.choice(masters)
		dbName = 'default'
		#logger.debug( 'dbName: ' + dbName )
		return dbName
	def allow_relation(self, obj1, obj2, **hints):
		"Allow any relation between two objects in the db pool"
		return True
	def allow_syncdb(self, db, model):
		"Explicitly put all models on all databases."
		return True
