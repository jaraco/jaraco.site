
import cherrypy
from genshi.template import TemplateLoader
import os
from lxml import etree
import urllib2
from BeautifulSoup import BeautifulSoup

import logging
log = logging.getLogger(__name__)

loader = TemplateLoader(
	os.path.join(os.path.dirname(__file__), 'templates'),
	auto_reload=True
)

class Root(object):
	@cherrypy.expose
	def index(self):
		tmpl = loader.load('welcome.html')
		return tmpl.generate().render('html', doctype='html')

	@cherrypy.expose
	def projects(self, name=None):
		if name: redirect('http://pypi.python.org/pypi/'+name)
		py_projects = urllib2.urlopen('https://svn.jaraco.com/jaraco/python')
		soup = BeautifulSoup(py_projects)
		projects = []
		for anchor in soup.findAll('a'):
			href = anchor['href']
			if 'jaraco' in href:
				projects.append(href)
		tmpl = loader.load('project_list.html')
		return tmpl.generate(projects=projects).render('html', doctype='html')

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