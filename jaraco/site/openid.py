from __future__ import absolute_import

import cherrypy
import os
import logging
from jaraco.site import output as default_output, render

log = logging.getLogger(__name__)

try:
	from openid.store.filestore import FileOpenIDStore
	from openid.server import server
	from openid.consumer import discover
	from openid.extensions import sreg
except ImportError:
	log.error("Unable to import openid modules - OpenID support disabled")

from urllib.parse import urljoin

def output(path, *args, **kwargs):
	return default_output('openid/{0}'.format(path), *args, **kwargs)

class OpenID(object):
	# todo: get this from cherrypy
	_base_url = 'http://drake.jaraco.com:8080/openid/'
	def __init__(self):
		store_loc = os.path.join(os.path.dirname(__file__), 'openid store')
		self.store = FileOpenIDStore(store_loc)
		self.openid = server.Server(self.store, self.endpoint_url)

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

	@cherrypy.expose
	def server(self, *args, **kwargs):
		try:
			params = cherrypy.request.params
			openid_request = self.openid.decodeRequest(params)
		except server.ProtocolError as openid_error:
			return self.handle_openid_response(openid_error)

		if openid_request is None:
			return output("about")(render)(endpoint_url=self.endpoint_url)

		if openid_request.mode in ["checkid_immediate", "checkid_setup"]:
			return self.check_id_request(openid_request)

		return self.handle_openid_response(self.openid.handleRequest(openid_request))

	def handle_openid_response(self, resp):
		try:
			web_resp = self.openid.encodeResponse(resp)
			body = web_resp.body or ''
			cherrypy.response.status = web_resp.code
			cherrypy.response.headers.update(web_resp.headers)
		except server.EncodingError as err:
			body = err.response.encodeToKVForm()
			cherrypy.response.status = 400
			cherrypy.response.headers['Content-Type'] = 'text/plain; charset=UTF-8'
		return body

	def check_id_request(self, request):
		authorized = cherrypy.request.login == request.identity
		trust_root = request.trust_root
		session = cherrypy.session
		request_params = dict({trust_root: request})
		session.setdefault('last_request', dict()).update(request_params)
		return self.handle_openid_response(request.answer(authorized))

	@cherrypy.expose
	def allow(self, *args, **kwargs):
		trust_root = kwargs['trust_root']
		openid_request = self.request_from_session(trust_root)
		if not openid_request:
			raise Exception("Last request could not be retrieved")
		if openid_request.idSelect():
			open_identity = urljoin(self.id_base_url, kwargs['identifier'])
		else:
			open_identity = openid_request.identity

		assert len(set(['yes', 'no']).intersection(kwargs)) == 1, "Expected yes or no in allow post"
		affirmative = 'yes' in kwargs
		openid_response = openid_request.answer(affirmative)

		if affirmative:
			self.add_sreg_fields(openid_request, kwargs, openid_response)

		if kwargs.get('remember', 'no') == 'yes':
			remember_value = ['never', 'always'][affirmative]
			cherrypy.session[(open_identity, openid_request.trust_root)] = remember_value

		return self.handle_openid_response(openid_response)

	def add_sreg_fields(self, request, params, response):
		sreg_req = sreg.SRegRequest.fromOpenIDRequest(request)
		fields = sreg_req.allRequestedFields()
		source_values = dict(
			# todo, get this from the identified user
			nickname = 'jaraco',
			email = 'jaraco@jaraco.com',
			fullname = 'Jason R. Coombs',
			)
		send_fields = params.get('sreg', dict()).get('send', dict())
		# send only the fields requested by 'yes'
		values = [
			(key, source_values[key])
			for key in send_fields
			if send_fields[key] == 'yes'
			]
		values = dict(values)
		sreg_resp = sreg.SRegResponse.extractResponse(sreg_req, values)
		sreg_resp.toMessage(response.fields)

	def request_from_session(self, trust_root):
		last_request = cherrypy.session.get('last_request', {})
		return last_request.get(trust_root, None)

# disable the OpenID class if openid modules aren't available
if not 'FileOpenIDStore' in globals():
	OpenID = lambda: None
