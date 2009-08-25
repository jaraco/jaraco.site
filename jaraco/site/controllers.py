
import cherrypy
from genshi.template import TemplateLoader
import os

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
		import urllib2
		if name: redirect('http://pypi.python.org/pypi/'+name)
		py_projects = urllib2.urlopen('https://svn.jaraco.com/jaraco/python')
		from BeautifulSoup import BeautifulSoup
		soup = BeautifulSoup(py_projects)
		projects = []
		for anchor in soup.findAll('a'):
			href = anchor['href']
			if 'jaraco' in href:
				projects.append(href)
		tmpl = loader.load('project_list.html')
		return tmpl.generate(projects=projects).render('html', doctype='html')
