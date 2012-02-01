
import cherrypy
import os
from lxml import etree
import urllib2
import binascii
import codecs
from jaraco.util import auth
from jaraco.site.charts import Charts
from jaraco.site.openid import OpenID
from jaraco.site import render, output
from jaraco.site.projecthoneypot import from_cherrypy

import logging
log = logging.getLogger(__name__)

class Root(object):
	charts = Charts()
	openid = OpenID()

	@cherrypy.expose
	@output('welcome')
	def index(self):
		return render()

	@cherrypy.expose
	@output('project list')
	def projects(self, name=None):
		return render()

	@cherrypy.expose
	def allurbase(self):
		return str(cherrypy.request.base)

	def get_default_resume_url(self):
		return 'http://dl.dropbox.com' + urllib2.quote(
			'/u/54081/Jason R. Coombs resume.xml'
		)

	@cherrypy.expose
	def resume(self, url=None):
		url = url or self.get_default_resume_url()
		transform_name = os.path.join(
			os.path.dirname(__file__), 'static',
			'resume-1.5.1/xsl/output/us-html.xsl',
			)
		transform = etree.XSLT(etree.parse(open(transform_name)))
		res = urllib2.urlopen(url)
		# TODO: update date_modified in the XML from res.headers
		src = etree.parse(res)
		return str(transform(src))

	@cherrypy.expose
	def auth(self):
		return "You authenticated as %s" % cherrypy.request.login

	@cherrypy.expose
	def croakysteel_py(self):
		return from_cherrypy()

class AcctMgmt(object):
	@cherrypy.expose
	@output('Account Management')
	def index(self):
		return render()

	@cherrypy.expose
	@output('Change Password')
	def change_password(self, submit, username, old_password, new_password, new_password_confirm, system=None):
		from jaraco.site.sysadmin import NTUser
		try:
			if not new_password:
				raise ValueError("Blank passwords not allowed")
			if not new_password == new_password_confirm:
				raise ValueError("Passwords don't match")
			nt = NTUser(username, system or '.')
			nt.reset(old_password, new_password)
		except ValueError, e:
			response_messages = [
				'Password change has failed.',
				str(e),
				]
		else:
			name = nt.user.FullName
			response_messages = ['Password change for %(name)s was successful!' % vars()]
		return render(response_messages=response_messages)

	@cherrypy.expose
	@output('password gen')
	def password_gen(self, length=None):
		password = None

		class userstr(str): pass
		if length:
			newpass = auth.PasswordGenerator.make_password(int(length),
				encoding=None)
			password = userstr(binascii.b2a_hex(newpass))
			password.alternatives = []
			for encoding in ('base-64',):
				encoded, newlen = codecs.getencoder(encoding)(newpass)
				password.alternatives.append((encoded, encoding))
		else:
			length = 8
		return render(password=password, length=length)

class IPTool(object):
	def __init__(self):
		self.registry = dict()

	@cherrypy.expose
	def register(self, hostname, ip):
		self.registry[hostname] = ip

	@cherrypy.expose
	def report(self):
		return str(self.registry)


Root.acctmgmt = AcctMgmt()
Root.ip = IPTool()
