import string
import os
import time
import struct
import cPickle
import zlib
import urlparse
import types
import urllib
import re
import random
import socket

"""Copyright (c) 2009, 2010 Tecor Communications S.L.
All rights reserved."""

class Cache:
	
	def __init__(self):
		pass

	def getFolder(self, partition, number_files):
		if partition != 0:
			if partition%number_files == 0:
				folder = partition/number_files - 1
			else:
				folder = partition/number_files
		else:
			folder = 0
		return folder	



class Url:

	TldDict = {'com':'','net':'','org':'','edu':'','info':'','biz':'','name':'','bz':'','tv':'','cc':''}
	
	def __init__(self):
		pass

	def isHome(self, url):
		UrlTuple = urlparse.urlparse(url)
		path = UrlTuple[2]
		pathDyn = UrlTuple[4]
		if path == '':
			path = '/'
		if pathDyn == '':
			slash_count = string.count(path, '/')
			if slash_count == 1 or slash_count == 2:
				if string.find(path, '/index.') != -1 or string.find(path, '/welcome.') != -1 or string.find(path, '/home.') != -1 or path[len(path)-1] == '/':
					home_code = 'Y'
				else:
					home_code = 'N'
			else:
				home_code = 'N'
		else:
			home_code = 'N'
		return home_code

	def validateForSession(self, url):
		validate = True
		url = string.lower(url)
		if string.find(url, 'session') != -1 and string.find(url, 'id') != -1:
			validate = False
		if string.find(url, 'user') != -1 and string.find(url, 'id') != -1:
			validate = False
		if string.find(url, 'user') != -1 and string.find(url, 'num') != -1:
			validate = False
		if string.find(url, 'sid') != -1:
			validate = False
		return validate


	def quote(self, urlUni):
		urlEncoded = urllib.quote_plus(urlUni.encode("utf-8"))
		return urlEncoded

	def unquote(self, urlEncoded):
		urlUni = unicode(urllib.unquote_plus(urlEncoded),"utf-8")
		return urlUni
	def quoteSimple(self, urlUni):
		urlQuote = urllib.quote(urlUni.encode("utf-8"))
		return urlQuote
	def unquoteSimple(self, urlEncoded):
		urlUni = unicode(urllib.unquote(urlEncoded),"utf-8")
		return urlUni

	def quotePath(self, urlUni, encoding='utf-8'):
		"""Quote an url in unicode, coding using urllib the host name and path.
		Returns urlStr."""
		UrlTuple = urlparse.urlparse(urlUni)
		schema = UrlTuple[0]
		host = UrlTuple[1]
		path = UrlTuple[2]
		schemaNew = str(schema)
		pathNew = urllib.quote(path.encode(encoding))
		hostNew = urllib.quote(host.encode(encoding))
		TupleNew = (schemaNew, hostNew, pathNew, str(UrlTuple[3]), str(UrlTuple[4]), str(UrlTuple[5]))
		urlNew = urlparse.urlunparse(TupleNew)
		return urlNew
	
	def quoteStr(self, urlStr):
		"""Quote a string url using urllib module. Returns urlEncoded."""
		if type(urlStr) == types.UnicodeType:
                        urlEncoded = urllib.quote_plus(urlStr.encode("utf-8"))
                else:
                        urlEncoded = urllib.quote_plus(urlStr)
		return urlEncoded
	
	def unquoteStr(self, urlEncoded):
		"""Unquote an urlEncoded using urllib module. Returns urlStr."""
		if type(urlEncoded) == types.UnicodeType:
                        urlStr = urllib.unquote_plus(urlEncoded.encode("utf-8"))
                else:
                        urlStr = urllib.unquote_plus(urlEncoded)
		return urlStr

	def encodeStr(self, value):
		if type(value) == types.UnicodeType:
			valueStr = value.encode("utf-8")
		else:
			valueStr = value
		return valueStr

	def unifyHomeUrl(self, url):
		"""Unify home urls. Example: http://myhost.com is same as http://myhost.com/.
		First is converted to http://myhost/. Returns url."""
		UrlFields = urlparse.urlparse(url)
		uri = UrlFields[2]
		uri2 = UrlFields[3]
		uri3 = UrlFields[4]
		uri4 = UrlFields[5]
		if uri == '' and uri2 == '' and uri3 == '' and uri4 == '':
			url = url + '/'
		elif uri == '' and uri3 != '':
			url = UrlFields[0] + '://' + UrlFields[1] + '/' + '?' + uri3
		return url
	
	def fixSchema(self, url):
		"""Forces schema to be lower case. Returns good url."""
		UrlFields = urlparse.urlparse(url)
		schema = UrlFields[0]
		if schema == 'HTTP://':
			urlNew = url.replace('HTTP://','http://')
		else:
			urlNew = url
		return urlNew

	def getHost(self, url):
		"""Get hostname from given URL. Returns host or Null."""
		urlType = type(url)
		host = urlparse.urlparse(url)[1]
		if host != '':
			if host[len(host)-1] == '.':
				host = host[:len(host)-1]
			if string.find(host,':') != -1:
				index = string.find(host,':')
				host = host[:index]
			host = string.lower(host)
		else:
			host = None
		hostType = type(host)
		if hostType != urlType:
			if hostType == types.UnicodeType:
				host = host.encode("utf-8")
		return host

	def getDomain(self, url):
		"""Get first-level domain name from given URL. Returns domain name or NULL."""
		host = urlparse.urlparse(url)[1]
		if host != '':
			if 1:
				try:
					checkIp = self.isIpUrl(url)
					a = int(string.split(host,'.')[0])
					b = int(string.split(host, '.')[len(string.split(host, '.'))-1])
					IpList = string.split(host, '.')
					if checkIp:
						domain = IpList[0]
					else:
						domain = None
				except ValueError:
					if host[len(host)-1] == '.':
						host = host[:len(host)-1]
					domain = host[string.rfind(host,'.')+1:]
					if string.find(domain,':') != -1:
						index = string.find(domain,':')
						domain = domain[:index]
					domain = string.lower(domain)
					if len(domain) != 0:
						if re.search("[a-z]",domain[len(domain)-1]):
							domain = domain
						else:
							domain = None
					else:
						domain = None
		else:
			domain = None
		return domain
	
	def getDomainName(self, url):
		"""Get domain name for given url. Returns domain name or NULL."""
		hostName = urlparse.urlparse(url)[1]
		TldDict = {'com':'','net':'','org':'','edu':'','info':'','biz':'','name':'','bz':'','tv':'','cc':'','gs':'','vg':'','tc':'','ws':'','ms':''}
		CountryDict = {'com':'','org':'','edu':'','ac':'','nom':'','name':'','gob':'','co':'','net':'','biz':'','info':'','cc':'','bz':'','us':'','tv':'','gov':'','mil':''}
		if hostName != '':
			if string.count(hostName, '.') == 1:
				domainName = hostName
			else:
				domain = self.getDomain(url)
				if domain:
					if TldDict.has_key(domain):
                                                List = string.split(hostName, '.')
                                                domainName = List[len(List)-2] + '.' + List[len(List)-1]
                                        else:
						try:
							List = string.split(hostName, '.')
							checkIp = self.isIpUrl(url)
							if checkIp:
								IpList = string.split(hostName, '.')
								domainName = IpList[0] + '.' + IpList[1]
							else:
								subDomainName = List[len(List)-2]
								if CountryDict.has_key(subDomainName):
								        domainName = List[len(List)-3] + '.' + subDomainName + '.' + domain
								else:
								        domainName = List[len(List)-2] + '.' + List[len(List)-1]
						except IndexError:
							domainName = None
                                else:
                                    domainName = None
		else:
			domainName = None
		if domainName:
			domainName = domainName.lower()
		return domainName
	
	def getBaseUrlList(self, url):
		"""Estimates BaseUrlList, a list of most common base url list up to one level for the
		given url. Like ['tecor.com:/', 'tecor.com:/dir']."""
		UrlTuple = urlparse.urlparse(url)
		path = UrlTuple[2]
		if path == '':
			m = re.search('http://(.*?)\.(.+)', url)
			if m:
				baseHost = m.groups()[1]
			else:
				baseHost = None
		else:
			if string.find(url, 'www') != -1:
				m = re.search('http://(.*?)\.(.*?)/', url)
				if m:
					baseHost = m.groups()[1]
				else:
					baseHost = None
			else:
				m = re.search('http://(.*?)/', url)
				if m:
					baseHost = m.groups()[0]
				else:
					baseHost = None
		#domain = self.getDomainName(url)
		BaseUrlList = []
		if baseHost:
			if path != '':
				BaseUrlList.append(baseHost + '/')
				if path != '/':
					if string.find(path, '/') == 0 and len(path) > 1:
						PathList = string.split(path[1:], '/')
						if len(PathList) >= 2:
							BaseUrlList.append(baseHost + '/' + PathList[0] + '/')
						if len(PathList) >= 3:
                                                        BaseUrlList.append(baseHost + '/' + PathList[0] + '/' + PathList[1] + '/')
                                                if len(PathList) >= 4:
                                                        BaseUrlList.append(baseHost + '/' + PathList[0] + '/' + PathList[1] + '/' + PathList[2] + '/')
			else:
				BaseUrlList.append(baseHost + '/')
		else:
			BaseUrlList = None
		return BaseUrlList
				
	def checkBase(self, url, baseUrl):
		"""This method verifies that an url belongs to a base url."""
		if type(url) == types.UnicodeType:
			urlStr = url.encode('utf-8')
		else:
			urlStr = url
		"""print 'urlUni=>', url, type(url)
		print 'urlStr=>', urlStr, type(urlStr)
		print 'baseUrl=>', baseUrl, type(baseUrl)"""
		host = self.getHost(url)
		if host:
			BaseUrlList = string.split(baseUrl, '/')
			baseUrlHost = BaseUrlList[0]
			BaseUrlTuple = urlparse.urlparse('http://' + baseUrl)
			index = string.find(host, baseUrlHost)
			if index != -1:
				checkHost = 1
			else:
				checkHost = 0
			if checkHost:
				UrlTuple = urlparse.urlparse(url)
				path = UrlTuple[2]
				#print 'path=>', path, type(path)
				if type(path) != types.UnicodeType:
					try:
						pathUni = unicode(urllib.unquote(path), 'utf-8')
					except UnicodeDecodeError:
						pathUni = urllib.unquote(path)
				else:
					pathUni = urllib.unquote(path)
				baseUrlPath = BaseUrlTuple[2]
				if type(baseUrlPath) == types.UnicodeType:
					baseUrlPathStr = baseUrlPath.encode('utf-8')
				else:
					baseUrlPathStr = baseUrlPath
				try:
					index = string.find(pathUni, baseUrlPath)
				except UnicodeDecodeError:
					index = -1
				printCheck = False
				if printCheck:
					try:
						pathPrint = pathUni.encode('latin1')
						baseUrlPathPrint = baseUrlPath.encode('latin1')
						print 'checkBase=>', pathPrint, baseUrlPathPrint, index
					except UnicodeEncodeError:
						print 'checkBase=>', 'UnicodeEncodeError'
				#a = raw_input('continue')
				if index != -1:
				    checkPath = 1
				else:
				    checkPath = 0
				if checkPath:
				    check = 1
				else:
				    check = 0
			else:
				check = 0
		else:
			check = 0
		return check

	def checkRobot(self, url):
		url = url.lower()
		Fields = urlparse.urlparse(url)
		if Fields[2] == '/robots.txt':
			check = True
		else:
			check = False
		return check

	def getTypeUR(self, url, baseUrl):
		"""Get UR type, "lr", "lk", or "n". In case the url belongs to baseUrl,
		the type is "lr". If it does not belong, and the domainName is different,
		"lk". In case it is the same domain, "n" (Ej.: urls in Yahoo under a dir name, like
		/Arts/ and finds other urls, like help.yahoo.com/, those urls are not "lk", but "n"
		type resources."""
		checkBase = self.checkBase(url, baseUrl)
		if checkBase:
			urlType = 'lr'
		else:
			domain = self.getDomainName(url)
			domainBaseUrl = self.getDomainName('http://' + baseUrl)
			if domain != domainBaseUrl:
				urlType = 'lk'
			else:
				urlType = 'n'
		return urlType

	def getBaseUrlListFilters(self, url):
            """Estimates a list of base urls that could exist in table filters of UR."""
            BaseUrlList = []
            host = self.getHost(url)
            BaseUrlList.append(host + '/')
            domain = self.getDomainName(url)
            BaseUrlList.append(domain + '/')
            path = urlparse.urlparse(url)[2]
            PathList = string.split(path, '/')
            if len(PathList) >= 2:
                if PathList[1] != '':
                    BaseUrlList.append(domain + '/' + PathList[1] + '/')
                    BaseUrlList.append(host + '/' + PathList[1] + '/')
            return BaseUrlList

	def getDepthCode(self, url):
		"""Calculate the depthCode.
		0 => For home pages (http://domain.com or http://domain.com/)
		1 => For first level home directory pages (http://www.domain.com/dir/)
		2 => All the rest...
		Return int."""
		UrlTuple = urlparse.urlparse(url)
		path = UrlTuple[2]
		dynPath = UrlTuple[4]
		if path == '':
			path = '/'
		counter = string.count(path, '/')
		if dynPath == '':
			if string.find(path, '/index.') != -1 or string.find(path, '/welcome.') != -1 or string.find(path, '/home.') != -1 or path[len(path)-1] == '/':
				if counter == 1:
					depthCode = 0
				elif counter == 2:
					depthCode = 1
				else:
					depthCode = 2
			else:
				depthCode = 2
		else:
			depthCode = 2
		return depthCode

	def isIpUrl(self, url):
		"""Checks that url has ip address instead of hostname. Must have
		four ints separated by "."."""
		host = urlparse.urlparse(url)[1]
		check = False
		if string.find(host, '.') != -1:
			List = string.split(host, '.')
			if len(List) == 4:
				i = 0
				checkList = True
				while i != len(List):
					try:
						ipField = int(List[i])
					except ValueError:
						checkList = False
						break
					i = i + 1
				if checkList:
					check = True
		return check
	
	def processIpUrl(self, url):
		"""Get hostname for ip, and construct new host url. In case a host
		could not be resolved, the ip url is returned."""
		ip = urlparse.urlparse(url)[1]
		try:
			HostTuple = socket.gethostbyaddr(ip)
			hostname = HostTuple[0]
			urlHost = string.replace(url, ip, hostname)
		except:
			urlHost = url
		return urlHost
	
	def join(self, base, path):
		"""Parse and join a base url and a path. Example, base => 'domain.com/manual/',
		and path '../index.html gives domain.com/index.html. Returns final url."""
		urlFinal = urlparse.urljoin(base, path)
		return urlFinal
	def toStr(self, url):
		"""Encode an url in unicode mode
		@param url: Url in unicode
		@return: urlStr: Url encoded in string mode"""
		if type(url) == types.UnicodeType:
			urlStr = url.encode("utf-8")
		else:
			urlStr = url
		return urlStr
	def toUnicode(self, urlStr):
		"""Convert an url in string mode to unicode mode.
		@param urlStr: Url in string
		@return: url: Url in unicode""" 
		if types(urlStr) == types.UnicodeType:
			url = urlStr
		else:
			url = unicode(urlStr, "utf-8")
		return url
	def toStrList(self, UrlList):
		"""Convert list of urls in unicode format to list in string format
		@param UrlList: List of urls in unicode
		@return: UrlList: List in string"""
		UrlList = []
		for sUrl in UrlList:
			UrlList.append(self.toStr(sUrl))
		return UrlList
	def toUnicodeList(self, UrlList):
		"""Convert list of urls in string format to list in unicode format
		@param UrlList: List of urls in string format
		@return: UrlList: List of urls in unicode format."""
		UrlList = []
		for sUrl in UrlList:
			pass
		return UrlList
	def getHostDict(self, UrlList):
		"""Get host dict from list of urls -> HostDict[sHost]=[sUrl,...]
		@param UrlList:
		@return: HostDict (sHost->[sUrl, ...])""" 
		HostDict = {}
		for sUrl in UrlList:
			uHost = self.getHost(sUrl)
			sHost = self.toStr(uHost)
			if not HostDict.has_key(sHost):
				HostDict[sHost] = []
			HostDict[sHost].append(sUrl)
		return HostDict
	
class Partition:

	def __init__(self):
		pass
	
	def getPartition(self, input_str, type):
		# Convert to string in case it is int
		input_str = str(input_str)
		if type == 'site':
			list = string.split(input_str,'.')
			partition_str = list[len(list)-2]
			if len(partition_str) >= 2:
				partition = struct.unpack('H',partition_str[:2])[0]
			elif len(partition_str) == 1:
				partition = struct.unpack('H',partition_str + ' ')[0]
			else:
				partition = struct.unpack('H','  ')[0]
			return partition
		else:
			if len(input_str) >= 2:
				partition_str = input_str[:2]
			elif len(input_str) == 1:
				partition_str = input_str + ' '
			else:
				partition_str = '  '
			partition = struct.unpack('H',partition_str)[0]
		return partition

	def getWordPartition(self, input_str):
		first_char = input_str[0]
		if len(input_str) == 3:
			last_index = 2
		elif len(input_str) > 3:
			last_index = len(input_str)-3
		else:
			last_index = len(input_str)-1
		last_char = input_str[last_index]
		if len(input_str) != 1:
			data_str = first_char + last_char
		else:
			data_str = input_str[0] + ' '
		partition = struct.unpack('H', data_str)[0]
		return partition

class ShowTools:

	#CHUNK_PIECE = '<font face="arial,helvetica" size="-1" color="red"><b>...</b></font>'
	CHUNK_PIECE = ''
	HtmlDict = {}
	Query = u''
	DowngradeDict = {}
	WordDictList = []
	RelDict = {'max_limit': 5000, 'chunk_size': 300, 'score_add': 1.5, 'score_normal': 1.0}
	
	def __init__(self, query, downgrade_dict, html_dict):
		self.Query = query
		self.DowngradeDict = downgrade_dict
		self.HtmlDict = html_dict
		#self.WordDictList = self.getWordDictList()
		list = string.split(query, ';')
		add_list = []
		other_list = []
		AddDict = {}
		WordDict = {}
		i = 0
		while i != len(list):
			word = list[i]
			if string.find(word, '+') != -1:
				word = re.sub('[+]', '', word)
				if string.find(word, '&') != -1 and string.find(word, ';') != -1:
					word = self.processHtml(add_list[i])
				#print 'step 1'
				#print word
				# downgrade chars
				j = 0
				target = word
				#print 'target'
				#print target
				while j != len(target):
					char = target[j]
					if self.DowngradeDict.has_key(char):
						#print downgrade_dict[char]
						target = re.sub(char, self.DowngradeDict[char], target)
					j = j + 1
				word = target
				#print 'step 2'
				#print word
				AddDict[word]=''
				WordDict[word]=''
			else:
				WordDict[word]=''
			i = i + 1		
		self.WordDict = WordDict
		self.AddDict = AddDict
		
	def processHtml(self, word):
		index = string.find(word, '&')
		index2 = string.find(word, ';')
		target_i = word[index:index2+1]
		if self.HtmlDict.has_key(target_i):
			word = re.sub(target_i, self.HtmlDict[target_i], word)
		return word

	def downgradeWord(self, word):
		i = 0
		while i != len(word):
			if self.DowngradeDict.has_key(word[i]):
				word = re.sub(word[i], self.DowngradeDict[word[i]], word)
			i = i + 1
		return word

	def boldCData(self, text):
		# Bug for things like "Angeles, ...", "Angeles."
		text_main = text
		text_lower = string.lower(text)
		i = 0
		list = string.split(text_main, ' ')
		out_list = []
		while i != len(list):
			list_i = list[i]
			list_i = re.sub('\s+',' ', list_i)
			if string.find(list_i, '&') != -1 and string.find(list_i, ';') != -1:
				list_i = self.processHtml(list_i)
				#print list_i
			list_i_lower = self.downgradeWord(list_i)
			list_i_lower = string.lower(list_i_lower)
			list_i_lower = re.sub('\A\W+', '', list_i_lower)
			list_i_lower = re.sub('\W\Z', '', list_i_lower)
			list_i_lower = re.sub('\W', ' ', list_i_lower)
			WordFieldList = string.split(list_i_lower)
			if len(WordFieldList) == 1:
				if self.WordDict.has_key(list_i_lower):
					#list_i = re.sub('\W+', '', list_i)
					#print list_i_lower, list_i
					repl_str = '<b>' + list_i + '</b>'
				else:
					repl_str = list_i
			else:
				if string.find(list_i, '-') != -1:
					WordFieldSrcList = string.split(list_i,'-')
					if len(WordFieldSrcList) == len(WordFieldList):
						if len(WordFieldSrcList) != 1:
							FieldFinalList = []
							j = 0
							while j != len(WordFieldList):
								wordField = WordFieldList[j]
								if self.WordDict.has_key(wordField):
									FieldFinalList.append('<b>' + WordFieldSrcList[j] + '</b>')
								else:
									FieldFinalList.append(WordFieldSrcList[j])
								j = j + 1
							repl_str = string.join(FieldFinalList, '-')
					else:
						repl_str = list_i
				elif string.find(list_i, '/') != -1:
					WordFieldSrcList = string.split(list_i,'/')
					if len(WordFieldSrcList) == len(WordFieldList):
						if len(WordFieldSrcList) != 1:
							FieldFinalList = []
							j = 0
							while j != len(WordFieldList):
								wordField = WordFieldList[j]
								if self.WordDict.has_key(wordField):
									FieldFinalList.append('<b>' + WordFieldSrcList[j] + '</b>')
								else:
									FieldFinalList.append(WordFieldSrcList[j])
								j = j + 1
							repl_str = string.join(FieldFinalList, '/')
					else:
						repl_str = list_i
				else:
					repl_str = list_i
			out_list.append(repl_str)
			i =i + 1
		out_str = string.join(out_list)
		return out_str
	def bold(self, text):
		# Bug for things like "Angeles, ...", "Angeles."
		#print 'text=>', text.encode('latin1'), type(text)
		text_main = text
		text_lower = string.lower(text)
		i = 0
		list = string.split(text_main, ' ')
		out_list = []
		while i != len(list):
			list_i = list[i]
			list_i = re.sub('\s+',' ', list_i)
			if string.find(list_i, '&') != -1 and string.find(list_i, ';') != -1:
				list_i = self.processHtml(list_i)
				#print list_i
			#print 'list_i=>', list_i
			list_i_lower = self.downgradeWord(list_i)
			list_i_lower = string.lower(list_i_lower)
			list_i_lower = re.sub('\A\W+^' + chr(241) + '^' + chr(231), '', list_i_lower)
			list_i_lower = re.sub('\W\Z^' + chr(241) + '^' + chr(231), '', list_i_lower)
			list_i_lower = re.sub('\-', ' ', list_i_lower)
			list_i_lower = re.sub('\/', ' ', list_i_lower)
			list_i_lower = re.sub('\.', ' ', list_i_lower)
			list_i_lower = re.sub('\,', ' ', list_i_lower)
			list_i_lower = re.sub('\!', ' ', list_i_lower)
			list_i_lower = re.sub('\\' + chr(161), ' ', list_i_lower)
			list_i_lower = re.sub('\?', ' ', list_i_lower)
			list_i_lower = re.sub('\\' + chr(191), ' ', list_i_lower)
			list_i_lower = re.sub('\(', ' ', list_i_lower)
			list_i_lower = re.sub('\)', ' ', list_i_lower)
			list_i_lower = re.sub('\W^' + chr(241) + '^' + chr(231), ' ', list_i_lower)
			#list_i_lower = re.sub('\W', ' ', list_i_lower)
			list_i_lower = list_i_lower.strip()
			WordFieldList = string.split(list_i_lower)
			#print 'WordFieldList=>', WordFieldList
			#print 'list_i_lower=> *'+ list_i_lower + '*'
			if len(WordFieldList) == 1:
				if self.WordDict.has_key(list_i_lower):
					#list_i = re.sub('\W+', '', list_i)
					#print list_i_lower, list_i
					repl_str = '<b>' + list_i + '</b>'
				else:
					repl_str = list_i
			else:
				if string.find(list_i, '-') != -1:
					WordFieldSrcList = string.split(list_i,'-')
					if len(WordFieldSrcList) == len(WordFieldList):
						if len(WordFieldSrcList) != 1:
							FieldFinalList = []
							j = 0
							while j != len(WordFieldList):
								wordField = WordFieldList[j]
								if self.WordDict.has_key(wordField):
									FieldFinalList.append('<b>' + WordFieldSrcList[j] + '</b>')
								else:
									FieldFinalList.append(WordFieldSrcList[j])
								j = j + 1
							repl_str = string.join(FieldFinalList, '-')
					else:
						repl_str = list_i
				elif string.find(list_i, '/') != -1:
					WordFieldSrcList = string.split(list_i,'/')
					#print 'WordFieldSrcList=>', WordFieldSrcList
					if len(WordFieldSrcList) == len(WordFieldList):
						if len(WordFieldSrcList) != 1:
							FieldFinalList = []
							j = 0
							while j != len(WordFieldList):
								wordField = WordFieldList[j]
								wordFieldSrc = WordFieldSrcList[j].replace('/','')
								#print 'wordField=>', wordField, wordFieldSrc
								if self.WordDict.has_key(wordField):
									FieldFinalList.append('<b>' + WordFieldSrcList[j] + '</b>')
								else:
									FieldFinalList.append(WordFieldSrcList[j])
								j = j + 1
							repl_str = string.join(FieldFinalList, '/')
					else:
						repl_str = list_i
				elif string.find(list_i, '.') != -1:
					WordFieldSrcList = string.split(list_i,'.')
					#print 'WordFieldSrcList=>', WordFieldSrcList
					if len(WordFieldSrcList) == len(WordFieldList):
						if len(WordFieldSrcList) != 1:
							FieldFinalList = []
							j = 0
							while j != len(WordFieldList):
								wordField = WordFieldList[j]
								wordFieldSrc = WordFieldSrcList[j].replace('.','')
								#print 'wordField=>', wordField, wordFieldSrc
								if self.WordDict.has_key(wordField):
									FieldFinalList.append('<b>' + WordFieldSrcList[j] + '</b>')
								else:
									FieldFinalList.append(WordFieldSrcList[j])
								j = j + 1
							repl_str = string.join(FieldFinalList, '.')
					else:
						repl_str = list_i
				else:
					repl_str = list_i
			out_list.append(repl_str)
			i =i + 1
		out_str = string.join(out_list)
		return out_str

	def getRelevance(self, chunk_str, score_add, score_normal):
		chunk_str = string.lower(chunk_str)
		WordDict = self.WordDict
		AddDict = self.AddDict
		WordList = WordDict.keys()
		i = 0
		rel_chunk = 0
		while i != len(WordList):
			word = WordList[i]
			if string.find(chunk_str, word) != -1:
				word_count = string.count(chunk_str, word)
				if AddDict.has_key(word):
					word_rel = score_add*word_count
				else:
					word_rel = score_normal*word_count
				rel_chunk = rel_chunk + word_rel
			i = i + 1
		return rel_chunk

	def getChunkEnd(self, body_lower, chunk_end):
		chunk_end = string.find(body_lower, ' ', chunk_end)
		return chunk_end

	def dynDescr(self, doc):
		#rel_dict = {'max_limit': 1000, 'chunk_size': 180, 'score_add': 1.5, 'score_normal': 1.0}
		max_limit = self.RelDict['max_limit']
		chunk_size = self.RelDict['chunk_size']
		score_add = self.RelDict['score_add']
		score_normal = self.RelDict['score_normal']
		#print max_limit, chunk_size, score_add, score_normal
		#doc = get_doc(resource_number)
		DocList = string.split(doc, '\012')
		title = DocList[0]
		description = DocList[1]
		body = DocList[2]
		body_lower = string.lower(body)
		#WordDictList = self.getWordDictList()
		#WordDict = WordDictList[0]
		WordList = self.WordDict.keys()
		i = 0
		if len(body_lower) > max_limit:
			if body_lower[max_limit] != ' ':
				index = string.find(body_lower, ' ', max_limit)
				real_limit = index
			else:
				real_limit = len(body_lower)
		else:
			real_limit = len(body_lower)
		if len(body_lower) > max_limit:
			if max_limit%chunk_size != 0:
				number_chunks = max_limit/chunk_size+1
			else:
				number_chunks = max_limit/chunk_size
		else:
			if len(body_lower)%chunk_size != 0:
				number_chunks = (len(body_lower)/chunk_size) + 1
			else:
				number_chunks = (len(body_lower)/chunk_size)
		i = 0
		chunk_dict = {}
		chunk_end = 0
		chunk_sel = 0
		chunk_rel_str = ''
		#print 'number_chunks => ' + str(number_chunks) + ' length => ' + str(len(body_lower))
		while i != number_chunks:
			chunk = i + 1
			chunk_start = chunk_end
			chunk_end = chunk_size*chunk
			if len(body_lower) > chunk_size:
				if chunk_end > len(body_lower):
					chunk_end = len(body_lower)
				if len(body_lower) > max_limit:
					if max_limit%chunk_size != 0:
						chunk_final = max_limit/chunk_size + 1
					else:
						chunk_final = max_limit/chunk_size
				else:
					if len(body_lower)%chunk_size != 0:
						chunk_final = len(body_lower)/chunk_size + 1
					else:
						chunk_final = len(body_lower)/chunk_size
				#print chunk, chunk_start, chunk_final
				if chunk == chunk_final:
					chunk_end = real_limit
				else:
					if body_lower[chunk_end] != ' ':
						check_end = self.getChunkEnd(body_lower, chunk_end)
				if chunk_end-chunk_start <= chunk_size:
					chunk_str = body[chunk_start:chunk_end]
					#chunk_str = string.capitalize(chunk_str)
					chunk_rel = self.getRelevance(chunk_str, score_add, score_normal)
					chunk_dict[chunk] = chunk_str
					if chunk_rel > chunk_sel:
						chunk_rel_str = chunk_str
						chunk_sel = chunk_rel
				#print chunk, chunk_rel
				#print chunk_rel_str
				#print chunk, chunk_final, chunk_start, chunk_end, len(body_lower), len(chunk_rel_str), chunk_rel
			else:
				chunk_rel_str = body_lower
			i = i + 1
		if chunk_rel_str == '':
			chunk_rel_str = description
		space_list = string.split(chunk_rel_str, ' ')
		i = 0
		while i != len(space_list):
			if len(space_list[i]) > 100:
				space_list[i] = space_list[i][:len(space_list[i])/2] + ' ' + space_list[i][len(space_list[i])/2:]
			i = i + 1
		chunk_rel_str = string.join(space_list, ' ')
		# Finish chunk format and return
		#chunk_rel_str = self.CHUNK_PIECE + ' ' + chunk_rel_str + ' ' + self.CHUNK_PIECE
		#print chunk_rel_str
		chunk_rel_str = string.strip(chunk_rel_str)
		return [chunk_dict, chunk_rel_str]

						

class Zone:
	
	def __init__(self):
		pass
	
	def checkLinkZone(self, zone, LinkZoneDict):
		if len(LinkZoneDict) != 0:
			if LinkZoneDict.has_key(zone):
				check = True
			else:
				check = False
		else:
			check = True
		return check

class Score:
	__DEFAULT_WEIGHT = 50
	def __init__(self):
		pass
	def __getScoreFloat(self, score):
		scoreFloat = (float(score)/100)*4.0
		return scoreFloat
	def calculate(self, EnAccount, EnData, linkScoreRatio, fieldTarget=None):
		numberDaysToday = time.time()/86400
		if EnData:
			zoneCode = EnData.getZoneCode()
			langCode = EnData.getLangCode()
			homeCode = EnData.getHome()
			domainNumber = EnData.getDomainNumber()
			hostNumber = EnData.getHostNumber()
			contentTypeCode = EnData.getContentTypeCode()
			numberDays = EnData.getNumberDays()
			EnScoreWord = EnAccount.getEnConfigScoreWord()
			EnScoreResource = EnAccount.getEnConfigScoreResource()
			if not fieldTarget:
				scoreUrl = float(EnScoreWord.getUrl())*EnData.getUrl()
				scoreTitle = float(EnScoreWord.getTitle())*EnData.getTitle()
				scoreDescription = float(EnScoreWord.getDescriptionMeta())*EnData.getDescription()
				scoreDescriptionTxt = float(EnScoreWord.getDescriptionFirstLines())*EnData.getDescriptionTxt()
				scoreKeywords = float(EnScoreWord.getKeywordsMeta())*EnData.getKeywords()
				scoreBody = float(EnScoreWord.getBody())*EnData.getBody()
				scoreDomain = float(EnScoreWord.getDomain())*EnData.getDomain()
				scoreBodyBold = float(EnScoreWord.getBodyBold())*EnData.getBodyBold()
				scoreBodyH1 = float(EnScoreWord.getBodyH1())*EnData.getBodyH1()
				scoreBodyH2 = float(EnScoreWord.getBodyH2())*EnData.getBodyH2()
				scoreBodyH3 = float(EnScoreWord.getBodyH3())*EnData.getBodyH3()
				scoreWord = int(scoreUrl + scoreTitle + scoreDescription + scoreDescriptionTxt + scoreKeywords + scoreBody + scoreDomain + scoreBodyBold + scoreBodyH1 + scoreBodyH2 + scoreBodyH3)
			else:
				if fieldTarget == 'url':
					scoreUrl = float(EnScoreWord.getUrl())*EnData.getUrl()
					scoreWord = scoreUrl
				elif fieldTarget == 'title':
					scoreTitle = float(EnScoreWord.getTitle())*EnData.getTitle()
					scoreWord = scoreTitle
				elif fieldTarget == 'descr':
					scoreDescription = float(EnScoreWord.getDescriptionMeta())*EnData.getDescription()
					scoreWord = scoreDescription
				elif fieldTarget == 'keyb':
					scoreKeywords = float(EnScoreWord.getKeywordsMeta())*EnData.getKeywords()
					scoreWord = scoreKeywords
				elif fieldTarget == 'descr_txt':
					scoreDescriptionTxt = float(EnScoreWord.getDescriptionFirstLines())*EnData.getDescriptionTxt()
					scoreWord = scoreDescriptionTxt
				elif fieldTarget == 'body':
					scoreBody = float(EnScoreWord.getBody())*EnData.getBody()
					scoreWord = scoreBody
				elif fieldTarget == 'Domain':
					scoreDomain = float(EnScoreWord.getDomain())*EnData.getDomain()
					scoreWord = scoreDomain
				elif fieldTarget == 'BodyBold':
					scoreBodyBold = float(EnScoreWord.getBodyBold())*EnData.getBodyBold()
					scoreWord = scoreBodyBold
				elif fieldTarget == 'BodyH1':
					scoreBodyH1 = float(EnScoreWord.getBodyH1())*EnData.getBodyH1()
					scoreWord = scoreBodyH1
				elif fieldTarget == 'BodyH2':
					scoreBodyH2 = float(EnScoreWord.getBodyH2())*EnData.getBodyH2()
					scoreWord = scoreBodyH2
				elif fieldTarget == 'BodyH3':
					scoreBodyH3 = float(EnScoreWord.getBodyH3())*EnData.getBodyH3()
					scoreWord = scoreBodyH3
			if scoreWord > 100:
				scoreWord = 100
			checkForce = False
			counter = 0
			scoreResource = 0
			scoreDate = EnScoreResource.getDate()
			if scoreDate != 0:
				dateRatio = numberDays/numberDaysToday
				scoreDate = int(scoreDate*dateRatio)
				counter = counter + 1
				scoreResource = (scoreResource+scoreDate)/counter
			LangCodeDict = EnScoreResource.getLangCodeDict()
			if len(LangCodeDict) != 0:
				if LangCodeDict.has_key(str(langCode)):
					scoreLang = int(LangCodeDict[str(langCode)])
					if scoreLang == 0:
						checkForce = True
					else:
						counter = counter + 1
						scoreResource = (scoreResource+scoreLang)/counter
				else:
					#checkForce = True
					# When mapping dicts found, not defined weights have default value
					#scoreResource = (scoreResource+self.__DEFAULT_WEIGHT)/counter
					pass
			ZoneCodeDict = EnScoreResource.getZoneCodeDict()
			if len(ZoneCodeDict) != 0:
				if ZoneCodeDict.has_key(str(zoneCode)):
					scoreZone = int(ZoneCodeDict[str(zoneCode)])
					if scoreZone == 0:
						checkForce = True
					else:
						counter = counter + 1
						scoreResource = (scoreResource+scoreZone)/counter
				else:
					#checkForce = True
					#scoreResource = (scoreResource+self.__DEFAULT_WEIGHT)/counter
					pass
			scoreHome = EnScoreResource.getHome()
			if homeCode != 0:
				counter = counter + 1
				scoreResource = (scoreResource+scoreHome)/counter
			DomainNumberDict = EnScoreResource.getDomainNumberDict()
			if DomainNumberDict.has_key(str(domainNumber)):
				scoreDomainNumber = int(DomainNumberDict[str(domainNumber)])
				counter = counter + 1
				scoreResource = (scoreResource+scoreDomainNumber)/counter
			HostNumberDict = EnScoreResource.getHostNumberDict()
			if HostNumberDict.has_key(str(hostNumber)):
				scoreHostNumber = int(HostNumberDict[str(hostNumber)])
				counter = counter + 1
				scoreResource = (scoreResource+scoreHostNumber)/counter
			ContentTypeCodeDict = EnScoreResource.getContentTypeCodeDict()
			if ContentTypeCodeDict.has_key(str(contentTypeCode)):
				scoreContentType = int(ContentTypeCodeDict[str(contentTypeCode)])
				counter = counter + 1
				scoreResource = (scoreResource+scoreContentType)/counter
			if scoreResource > 100:
				scoreResource = 100
			scoreLinkResource = int(EnScoreResource.getLinkRelevance()*linkScoreRatio)
			# return score is 0-1200
			score = scoreWord*4 + scoreResource*4 + scoreLinkResource*4
			#print 'Score->', score, scoreWord*4, scoreResource*4, scoreLinkResource*4
			if checkForce:
				score = 0
		else:
			score = 0
		return score

class Index (object):
	"""Doc."""
	@staticmethod
	def parseText(text):
		"""Parse text. Spaces will be word separator, as well as "-", "_", ".". Returns list of words 
		@param text: Text to index
		@return: wordList : List of words"""
		# TODO: Try to integrate B+ code for the downgrade characters and filters for words
		text = re.sub('[-_.]', ' ', text.lower()).strip()
		list1 = text.split()
		wordNew = ''
		listFinal = []
		for word in list1:
			wordNew = word.strip()
			wordNew = re.sub('[,]', '', wordNew).strip()
			listFinal.append(wordNew)
		wordList = listFinal
		return wordList
