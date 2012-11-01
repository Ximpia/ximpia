import simplejson as json

from django.http import Http404
from django.utils.translation import ugettext as _

from ximpia.core.models import ContextDecorator, XpMsgException
from ximpia.core.data import ActionDAO, ViewDAO
from ximpia.core.util import getClass
from ximpia.core.business import ViewDecorator

from constants import Constants as K
import business
from ximpia.util.http import Request


@ContextDecorator(app=K.APP)
def jxBusiness(request, **args):
	"""Excutes the business class: bsClass, method {bsClass: '', method: ''}
	@param request: Request
	@param result: Result"""
	print 'jxBusiness...'
	print request.REQUEST.items()
	request.session.set_test_cookie()
	request.session.delete_test_cookie()
	print 'session: ', request.session.items()
	#print 'session: ', request.session.items(), request.session.session_key
	if (request.REQUEST.has_key('view') or request.REQUEST.has_key('action')) and request.is_ajax() == True:
		viewAttrs = {}
		if request.REQUEST.has_key('view'):
			view = request.REQUEST['view']
			print 'view: ', view
			dbView = ViewDAO(args['ctx'])
			impl = dbView.get(application__code=K.APP, name=view).implementation
			# view attributes 
			viewAttrs = json.loads(request.REQUEST['params'])
			args['ctx']['viewNameSource'] = view
		elif request.REQUEST.has_key('action'):
			action = request.REQUEST['action']
			print 'action: ', action
			dbAction = ActionDAO(args['ctx'])
			dbView = ViewDAO(args['ctx'])
			actionObj = dbAction.get(application__code=K.APP, name=action)
			if args['ctx'].has_key('viewNameSource') and len(args['ctx']['viewNameSource']) != 0:
				print 'viewNameSource', args['ctx']['viewNameSource']
				viewObj = dbView.get(name=args['ctx']['viewNameSource'])
				if actionObj.application.code != viewObj.application.code:
					raise XpMsgException(None, _('Action is not in same application as view source'))
			impl = actionObj.implementation
		implFields = impl.split('.')
		method = implFields[len(implFields)-1]
		#bsClass = implFields[len(implFields)-2]
		classPath = ".".join(implFields[:-1])
		# TODO: Place this code into core
		if method.find('_') == -1 or method.find('__') == -1:
			cls = getClass( classPath ) 
			obj = cls(args['ctx'])
			if (len(viewAttrs) == 0) :
				result = eval('obj.' + method)()
			else:
				result = eval('obj.' + method)(**viewAttrs)
		else:
			print 'private methods...'
			raise Http404
	else:
		print 'Unvalid business request'
		raise Http404
	return result


# *******************************
# ****     Server Content     ***
# *******************************

@ContextDecorator(app=K.APP)
@ViewDecorator(K.APP, 'newPassword')
def changePassword(request, ximpiaId, reminderId, **args):
	"""View to show change password form. User will enter new password and click save. New password then would be saved
	and user logged in"""
	login = business.LoginBusiness(args['ctx'])
	result = login.showNewPassword(ximpiaId=ximpiaId, reminderId=reminderId)
	return result

@ContextDecorator(app=K.APP)
@ViewDecorator(K.APP, 'signup')
def signupUser(request, invitationCode, **args):
	"""Signup user with invitation."""
	affiliateId = Request.getReqParams(request, ['aid:int'])[0]
	signup = business.SignupBusiness(args['ctx'])
	result = signup.showSignupUser(invitationCode=invitationCode, affiliateId=affiliateId)
	return result
