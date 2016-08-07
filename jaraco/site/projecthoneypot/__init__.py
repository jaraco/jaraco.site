import sys
import os

from unittest import mock
import cherrypy

with mock.patch.object(sys, 'dont_write_bytecode', True):
	from . import croakysteel

cs_file = croakysteel.__file__
if not cs_file.endswith('.py'):
	print("croakysteel file is", cs_file)
	base = os.path.dirname(cs_file)
	croakysteel.__file__ = os.path.join(base, 'croakysteel.py')

class CherryPyZopeRequestAdapter(dict):
	"""
	An adapter that mimicks the Zope request object.
	"""
	def __init__(self):
		req = cherrypy.request
		for header, val in req.headers.items():
			header = 'HTTP_' + header.upper().replace('-', '_')
			self[header] = val
		self.update(REMOTE_ADDR = req.remote.ip)
		self.update(SERVER_PORT = str(req.local.port))
		self.update(SERVER_NAME = req.local.name)
		self.update(SERVER_ADDR = req.local.ip)
		self.update(SCRIPT_NAME = req.script_name)
		self.update(PATH_INFO = req.path_info)

def from_cherrypy():
	return croakysteel.from_zope(CherryPyZopeRequestAdapter())
