import os
from importlib_resources import files

import cherrypy

from .controllers import Root

cherrypy.config.update({
    'server.production': True,
    'server.socket_port': int(os.environ.get('PORT', 8080)),
    'server.socket_host': os.environ.get('SOCKET_HOST', '::'),
    'tools.encode.on': True,
    'tools.encode.encoding': 'utf-8',
    'tools.decode.on': True,
    'tools.sessions.on': True,
    'tools.trailing_slash.on': True,
    'tools.staticdir.root': os.fspath(files('jaraco.site')),
    'tools.proxy.on': True,
})

config = {
    '/static': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': 'static',
        'tools.staticdir.content_types': dict(svg='image/svg+xml'),
    }
}

app = cherrypy.tree.mount(Root(), '/', config)
