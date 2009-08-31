
import cherrypy
import os
from lxml import etree
import urllib2
from BeautifulSoup import BeautifulSoup
import binascii
import codecs
from jaraco.util import PasswordGenerator
from jaraco.site.charts import Charts
from jaraco.site import render, output

import logging
log = logging.getLogger(__name__)

class Root(object):
	charts = Charts()

	@cherrypy.expose
	@output('welcome')
	def index(self):
		return render()

	@cherrypy.expose
	@output('project list')
	def projects(self, name=None):
		if name: redirect('http://pypi.python.org/pypi/'+name)
		py_projects = urllib2.urlopen('https://svn.jaraco.com/jaraco/python')
		soup = BeautifulSoup(py_projects)
		projects = []
		for anchor in soup.findAll('a'):
			href = anchor['href']
			if 'jaraco' in href:
				projects.append(href)
		return render(projects=projects)

	@cherrypy.expose
	def allurbase(self):
		return str(cherrypy.request.base)

	def get_default_resume_url(self):
		return cherrypy.request.base + urllib2.quote(
			'/static/Jason R. Coombs resume.xml')

	@cherrypy.expose
	def resume(self, url=None):
		url = url or self.get_default_resume_url()
		transform_name = os.path.join(
			os.path.dirname(__file__), 'static',
			'resume-1.5.1/xsl/output/us-html.xsl',
			)
		transform = etree.XSLT(etree.parse(open(transform_name)))
		src = etree.parse(urllib2.urlopen(url))
		return str(transform(src))

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
				raise ValueError, "Blank passwords not allowed"
			if not new_password == new_password_confirm:
				raise ValueError, "Passwords don't match"
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
			newpass = PasswordGenerator.make_password(int(length), encoding=None)
			password = userstr(binascii.b2a_hex(newpass))
			password.alternatives = []
			for encoding in ('base-64',):
				encoded, newlen = codecs.getencoder(encoding)(password)
				password.alternatives.append((encoded, encoding))
		else:
			length=8
		return render(password=password, length=length)

Root.acctmgmt = AcctMgmt()