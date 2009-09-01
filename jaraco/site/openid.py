from openid.store.filestore import FileOpenIDStore
from openid.server.server import Server
from urlparse import urljoin

class OpenID(object):
	# todo: get this from cherrypy
	_base_url = 'http://www.jaraco.com/'
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
		self.relative_url('server/')

	@property
	def id_base_url(self):
		self.relative_url('id/')

	@property
	def yadis_base_url(self):
		self.relative_url('yadis/')

	@cherrypy.expose
	@output("openid/id")
	def id(self, username):
		return dict(
			endpoint_url = self.endpoint_url,
			yadis_url = urljoin(self.yadis_url, username)
			user_url = urljoin(self.id_base_url, username)
			)

	