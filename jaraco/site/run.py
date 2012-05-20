import cherrypy
import pkg_resources

try:
	from . import sspi
except ImportError:
	pass

from .controllers import Root

cherrypy.config.update({
	'tools.encode.on': True, 'tools.encode.encoding': 'utf-8',
	'tools.decode.on': True,
	'tools.sessions.on': True,
	'tools.trailing_slash.on': True,
	'tools.staticdir.root': pkg_resources.resource_filename('jaraco.site', '')
})

config = {
	'/static': {
		'tools.staticdir.on': True,
		'tools.staticdir.dir': 'static',
		'tools.staticdir.content_types': dict(svg='image/svg+xml'),
	},
}

if 'sspi' in globals():
	basic_auth = {
		'tools.auth_basic.on': True,
		'tools.auth_basic.realm': 'jaraco.com',
		'tools.auth_basic.checkpassword': sspi.check,
	}
	config['/auth'] = basic_auth
	config['/openid/server'] = basic_auth

app = cherrypy.tree.mount(Root(), '/', config)
