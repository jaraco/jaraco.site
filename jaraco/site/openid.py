from __future__ import absolute_import

import cherrypy
import os
from jaraco.site import output as default_output, render
from openid.store.filestore import FileOpenIDStore
from openid.server.server import Server
from openid.consumer import discover
from urlparse import urljoin

def output(path, *args, **kwargs):
	return default_output('openid/{0}'.format(path), *args, **kwargs)

class OpenID(object):
	# todo: get this from cherrypy
	_base_url = 'http://www.jaraco.com/openid/'
	def __init__(self):
		store_loc = os.path.join(os.path.dirname(__file__), 'openid store')
		store = FileOpenIDStore(store_loc)
		self.store = FileOpenIDStore(store_loc)
		self.server = Server(self.store, self.endpoint_url)

	def relative_url(self, path):
		# TODO: ensure _base_url ends with /
		return urljoin(self._base_url, path)

	# todo: make these properties just decorators on the appropriate methods
	@property
	def endpoint_url(self):
		return self.relative_url('server/')

	@property
	def id_base_url(self):
		return self.relative_url('id/')

	@property
	def yadis_base_url(self):
		return self.relative_url('yadis/')

	@cherrypy.expose
	@output("id")
	def id(self, username):
		return render(
			endpoint_url = self.endpoint_url,
			yadis_url = urljoin(self.yadis_base_url, username),
			user_url = urljoin(self.id_base_url, username),
			)

	@cherrypy.expose
	@output("yadis", method="xml", content_type="application/xrds+xml")
	def yadis(self, username=None):
		return render(
			discover = discover,
			endpoint_url = self.endpoint_url,
			user_url = username and urljoin(self.id_base_url, username),
			)

