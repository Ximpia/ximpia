import fpformat
import simplejson as json

import settings

#from ximpia.social_network.models import Choices

class ConfData(object):
    """Doc."""
    _dataDict = []
    _dataDictStr = ''
    def getDataDict(self):
        """Generate social network icon data"""
        return self._dataDict
    def getConf(self):
        """Doc."""
        return self._dataDict[0]
    def getData(self):
        """Doc."""
        return self._dataDict[1]
    def getS(self):
        """Returns json mode of dataDict"""
        self._dataDictStr = json.dumps(self._dataDict)
        return self._dataDictStr
    def parse(self):
        """Doc."""
        dict = json.loads(self._dataDictStr)
        return dict
    def __str__(self):
        return json.dumps(self._dataDict)
    def setData(self, dataDict):
        """Doc."""
        self._dataDict[1] = dataDict

class SocialNetworkIconData(ConfData):
    """Social network icon generation input field and accesors"""
    def __init__(self, service='', oauthVersion='', jsonData=''):
        if service != '' and oauthVersion != '':
            self._dataDict = [
                {'windowUrl': '', 'oauthVersion': fpformat.fix(oauthVersion, 1)},
                {'status': '', 'token': '', 'tokenSecret': ''}
            ]
            if oauthVersion == 2:
                self._dataDict[0]['windowUrl'] = settings.OAUTH_URL_DICT[service]['authorize']
            else:
                self._dataDict[0]['windowUrl'] = '/oauth/' + service
        elif jsonData != '':
            self._dataDict = json.loads(jsonData)
    def getToken(self):
        """Get token"""
        return self._dataDict[1]['token']
    def setToken(self, token):
        """Sets token"""
        self._dataDict[1]['token'] = token
    def getTokenSecret(self):
        """Get token password, secret"""
        return self._dataDict[1]['tokenSecret']
    def setTokenSecret(self, tokenSecret):
        """Sets token secret"""
        self._dataDict[1]['tokenSecret'] = tokenSecret
    def getStatus(self):
        """Get status of icon"""
        return self._dataDict[1]['status']

class SuggestBox(object):
    """Suggest box. It takes on constructor the tuple from Choices. It supports id,text and can be upgraded to images, etc..."""
    _tuple = ()
    def __init__(self, tuple):
        self._tuple = tuple
    def __str__(self):
        list = []
        for tupleData in self._tuple:
            if len(tupleData) == 2:
                dict = {'id': tupleData[0], 'text': tupleData[1]}
            list.append(dict)
        str = json.dumps(list)
        return str
    def getText(self, id):
        """Get text for id in list"""
        txt = ''
        for tuple in self._tuple:
            if tuple[0] == id:
                txt = tuple[1]
        return txt
    def getTupleList(self):
        """Get tuple list"""
        return self._tuple

class GenericComponent(ConfData):
    """Generic visual component."""
    def __init__(self, list=None, configDict=None, obj=None):
        if obj != None:
            self._dataDict = json.loads(obj)
        else:
            self._dataDict = [
                    {},
                    {'status': '', 'data': []}
            ]
            if list != None:
                self._dataDict[1]['data'] = list
            if configDict != None:
                self._dataDict[0] = configDict
    def addConfVariable(self, name, value):
        """Add config variable"""
        pass
    def getDataList(self):
        """Get data list"""
        return self._dataDict[1]['data']
    def setDataList(self, list):
        """Set data list"""
        self._dataDict[1]['data'] = list
    def getStatus(self):
        """Get status"""
        return self._dataDict[1]['status']
    def setStatus(self, status):
        """Set status"""
        self._dataDict[1]['status'] = status
    def filter(self, name):
        """Filter data from dataList attribute.
        @return: list : List"""
        listTmp = self.dataList
        list = []
        for dict in listTmp:
            if dict.has_key(name):
                list.append(dict[name])
        return list
    status = property(getStatus, setStatus)
    dataList = property(getDataList, setDataList)
