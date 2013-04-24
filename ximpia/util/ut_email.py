import string
import os
import time
import smtplib
import mimetypes
import random
import types

from email import Encoders
from email.Message import Message
from email.MIMEAudio import MIMEAudio
from email.MIMEBase import MIMEBase
from email.MIMEMultipart import MIMEMultipart
from email.MIMEImage import MIMEImage
from email.MIMEText import MIMEText

# Settings
from ximpia.core.util import get_class
settings = get_class(os.getenv("DJANGO_SETTINGS_MODULE"))

import xml_lib

"""Copyright (c) 2012 Ximpia Inc
All rights reserved."""

class EmailConnect:
	# Change username to Buscaplus Webmaster or System User, and include in config file
	def __init__(self):
		pass
	def send(self, MeAddress, EmailAddressList, messageStr):
		oSmtp = smtplib.SMTP()
		oSmtp.connect(settings.XIMPIA_EMAIL_HOST)
		oSmtp.login(settings.XIMPIA_EMAIL_USERNAME, settings.XIMPIA_EMAIL_PASSWORD)
		ConnDict = oSmtp.sendmail(MeAddress, EmailAddressList, messageStr)
		oSmtp.quit()

class EmailSimple(EmailConnect):
	"""Handles simple email, with no boundaries. Message can be HTML or text."""
	__MeAddress = ''
	__ToAddressList = []
	__Subject = ''
	__Message = ''
	__SubType = ''
	__Charset = ''
	def __init__(self, subType='plain', charSet='latin1'):
		self.__SubType = subType
		self.__CharSet = charSet
		self.oEmailConnect = EmailConnect()
	def __parseEmailAddressList(self, EmailAddressList):
		List = []
		i = 0
		while i != len(EmailAddressList):
			emailAddress = EmailAddressList[i]
			if string.find(emailAddress, '<') != -1:
				index1 = string.find(emailAddress,'<')
				index2 = string.find(emailAddress,'>', index1+1)
				List.append(emailAddress[index1+1:index2])
			else:
				List.append(emailAddress)
			i = i + 1
		return List
	def build(self, meAddress, ToAddressList, subject, message):
		if type(message) == types.UnicodeType:
			message = message.encode(self.__CharSet)
		self.__MeAddress = meAddress
		self.__ToAddressList = ToAddressList
		self.__Subject = subject
		self.__Message = message
		self.__oMIMEText = MIMEText(message, self.__SubType, self.__CharSet)
		messageIdStr = '<' + str(int(time.time())) + '-' + str(random.randint(0,9999999)) + '@buscaplus.com' + '>'
		self.__oMIMEText['Message-ID'] = messageIdStr
		dateStr = time.strftime("%a, %d %b %Y %H:%M:%S +0000",time.localtime())
		self.__oMIMEText['Date'] = dateStr
		self.__oMIMEText['Subject'] = subject
		self.__oMIMEText['From'] = meAddress
		self.__oMIMEText['To'] = string.join(ToAddressList, ',')
	def send(self):
		EmailAddressList = self.__parseEmailAddressList(self.__ToAddressList)
		messageStr = self.__oMIMEText.as_string()
		oEmailConnect = EmailConnect()
		oEmailConnect.send(self.__MeAddress, EmailAddressList, messageStr)

class EmailAlternative:
        """This class handles the emails with alternative parts, text and html.
        The html part does not have images loaded in the email."""
        def __init__(self):
                pass

class EmailAlternativeInside:
        """This class handles the emails with alternative parts, text and html.
        The html part has images loaded in the email."""
        def __init__(self):
                pass

class EmailAttach(EmailConnect):
	"""This class handles attachments in email, being the body text."""
	__MeAddress = ''
	__ToAddressList = []
	__Subject = ''
	__Message = ''
	__Charset = ''
	def __init__(self, charSet='ISO-8859-1'):
		self.__CharSet = charSet
		self.oEmailConnect = EmailConnect()
	def __parseEmailAddressList(self, EmailAddressList):
		List = []
		i = 0
		while i != len(EmailAddressList):
			emailAddress = EmailAddressList[i]
			if string.find(emailAddress, '<') != -1:
				index1 = string.find(emailAddress,'<')
				index2 = string.find(emailAddress,'>', index1+1)
				List.append(emailAddress[index1+1:index2])
			else:
				List.append(emailAddress)
			i = i + 1
		return List
	def build(self, meAddress, ToAddressList, subject, message, AttachPathList):
		dateStr = time.strftime("%a, %d %b %Y %H:%M:%S +0000",time.localtime())
		self.__MeAddress = meAddress
		self.__ToAddressList = ToAddressList
		self.__Subject = subject
		self.__Message = message
		self.__oMIME = MIMEMultipart()
		self.__oMIME['Date'] = dateStr
		messageIdStr = '<' + str(int(time.time())) + '-' + str(random.randint(0,9999999)) + '@buscaplus.com' + '>'
		self.__oMIME['Message-ID'] = messageIdStr
		self.__oMIME['Subject'] = subject
		self.__oMIME['From'] = meAddress
		self.__oMIME['To'] = string.join(ToAddressList, ',')
		# Add Text
		oPart = MIMEText(message, 'plain', self.__CharSet)
		self.__oMIME.attach(oPart)
		# Add Attachments
		i = 0
		while i != len(AttachPathList):
			attachPath = AttachPathList[i]
			PathList = attachPath.split('/')
			fileName = PathList[len(PathList)-1]
			attachType, attachEncoding = mimetypes.guess_type(attachPath)
			mainType, subType = attachType.split('/')
			if mainType == 'image':
				fp = open(attachPath, 'rb')
				msg = MIMEImage(fp.read(), _subtype=subType)
				fp.close()
			elif mainType == 'audio':
				fp = open(attachPath, 'rb')
				msg = MIMEAudio(fp.read(), _subtype=subType)
				fp.close()
			else:
				fp = open(attachPath, 'rb')
				msg = MIMEBase(mainType, subType)
				msg.set_payload(fp.read())
				fp.close()
				# Encode the payload using Base64
				Encoders.encode_base64(msg)
			msg.add_header('Content-Disposition', 'attachment', filename=fileName)
			self.__oMIME.attach(msg)
			i = i + 1
	def send(self):
		EmailAddressList = self.__parseEmailAddressList(self.__ToAddressList)
		messageStr = self.__oMIME.as_string()
		oEmailConnect = EmailConnect()
		oEmailConnect.send(self.__MeAddress, EmailAddressList, messageStr)

def getMessage(xmlStr):
	oPageXML = xml_lib.PageXML()
	oPageXML.parse(xmlStr)
	xPath = 'PageXML/EmailContainer[@id="DICT_EMAIL"]/Subject'
	subject = oPageXML.getKeySimple(xPath).getValue()
	xPath = 'PageXML/EmailContainer[@id="DICT_EMAIL"]/Message'
	message = oPageXML.getKeySimple(xPath).getValue()
	Tuple = (subject, message)
	return Tuple
