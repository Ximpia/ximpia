import string
import os
import MySQLdb
import socket

#from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpRequest, HttpResponseServerError

"""Copyright (c) 2010 Tecor Communications S.L.
All rights reserved."""

"""def doSession(request, AnonSessionDict, th=None, sth=None):
	# Session check
	if not AnonSessionDict.has_key('theme'):
		if th and sth:
			AnonSessionDict['theme'] = th
			AnonSessionDict['search_theme'] = sth
			AnonSessionDict['SearchThemesDict'] = {}
			sSearchTheme = sth
			sTheme = th
		else:
			AnonSessionDict['theme'] = config.DEFAULT_THEME
			AnonSessionDict['search_theme'] = config.DEFAULT_SEARCH_THEME
			AnonSessionDict['SearchThemesDict'] = {}
			sSearchTheme = config.DEFAULT_SEARCH_THEME
			sTheme = config.DEFAULT_THEME
	else:
		sTheme = AnonSessionDict['theme']
		sSearchTheme = AnonSessionDict['search_theme']
		if not AnonSessionDict.has_key('SearchThemesDict'):
			AnonSessionDict['SearchThemesDict'] = {}
	if request.COOKIES.has_key('anon_session_id'):
		sSession = request.COOKIES['anon_session_id']
	else:
		sSession = None
	Tuple = (sTheme, sSearchTheme, sSession, AnonSessionDict)
	return Tuple"""

"""def getLangZoneBrowser(request):
	Get local information from browser. Returns first language from browser and zone plus a list of all variables for language and zone from browser settings. -> Tuple(sLang, sZone, LangList, ZoneList).
	if request.META.has_key('HTTP_ACCEPT_LANGUAGE'):
		BrowserLanguageList = request.META['HTTP_ACCEPT_LANGUAGE'].split(',')
	else:
		BrowserLanguageList = []
	LangList = []
	ZoneList = []
	#print 'BrowserLanguageList->', BrowserLanguageList
	for sField in BrowserLanguageList:
		sLangTuple = sField.split(';')[0]
		if sLangTuple.find('-') != -1:
			sLangBrowser, sZoneBrowser = sLangTuple.split('-')
		else:
			sLangBrowser = sLangTuple.split('-')[0]
			sZoneBrowser = None
		if not sLangBrowser in LangList:
			LangList.append(sLangBrowser)
		if sZoneBrowser and not sZoneBrowser in ZoneList:
			ZoneList.append(sZoneBrowser)
	#print 'Langs/Zones->', LangList, ZoneList
	if len(LangList) != 0:
		sLang = LangList[0]
	else:
		sLang = ''
	if len(ZoneList) != 0:
		sZone = ZoneList[0]
	else:
		sZone = ''
	Tuple = (sLang, sZone, LangList, ZoneList)
	return Tuple

def selectLanguage(request, sLang):
	if not sLang:
		LangList = getLangZoneBrowser(request)[2]
		bLang = False
		for sLangTmp in LangList:
			if sLangTmp in config.LANG_DICT:
				bLang = True
				sLang = str(sLangTmp) 
		if not bLang:
			sLang = str(config.DEFAULT_LANG)
	if not config.LANG_DICT.has_key(sLang):
		raise Http404
	return sLang"""

class Request(object):
	
	@staticmethod
	def getReqParams(request, paramList, method='GET'):
		"""Get params from request, either by GET, REQUEST or POST. 
		@param paramList: param:type. It accepts either type and not type, like kk=aid and kk=aid:int
		@param method: Either GET or POST
		@return: myList : List of values from request. In case not found, None is returned"""
		myList = []
		typesNone = {'int': None, 'str': None, 'long': None}
		for paramFields in paramList:
			hasType = True
			if paramFields.find(':') != -1:
				param, paramType = paramFields.split(':') #@UnusedVariable
			else:
				hasType = False
			try:
				if hasType == True:
					value = eval(paramType + '(request.' + method + '[param])')
				else:
					value = eval('request.' + method + '[param]')					
			except:
				value = typesNone[paramType]
			myList.append(value)
		return myList
