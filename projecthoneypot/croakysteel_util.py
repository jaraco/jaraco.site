from croakysteel import from_zope

class CherryPyZopeRequestAdapter(dict):
	"""
	An adapter that mimicks the Zope request object.
	"""
	def __init__(self):
		import cherrypy
		req = cherrypy.request
		for header, val in req.headers.items():
			header = 'HTTP_' + val.upper().replace('-', '_')
			self[header] = val
		self.update(REMOTE_ADDR = req.remote.ip)
		self.update(SERVER_PORT = req.local.port)
		self.update(SERVER_NAME = req.local.name)
		self.update(SERVER_ADDR = req.local.ip)
		self.update(SCRIPT_NAME = req.script_name)
		self.update(PATH_INFO = req.path_info)

def from_cherrypy():
	return from_zope(CherryPyZopeRequestAdapter())