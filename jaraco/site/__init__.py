import os
import cherrypy
from jaraco.site.controllers import Root

def init():
	cherrypy.config.update({
		'tools.encode.on': True, 'tools.encode.encoding': 'utf-8',
		'tools.decode.on': True,
		'tools.trailing_slash.on': True,
		'tools.staticdir.root': os.path.abspath(os.path.dirname(__file__)),
	})

	app = cherrypy.tree.mount(Root(), '/', {
		'/static': {
			'tools.staticdir.on': True,
			'tools.staticdir.dir': 'static',
			'tools.staticdir.content_types': dict(svg='image/svg+xml'),
		}
	})

	return app