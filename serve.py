#!/usr/bin/env python

import operator, os, pickle, sys

import cherrypy

from jaraco.site.controllers import Root
import jaraco.site

def main():
    # Some global configuration; note that this could be moved into a
    # configuration file
    cherrypy.config.update({
        'tools.encode.on': True, 'tools.encode.encoding': 'utf-8',
        'tools.decode.on': True,
        'tools.trailing_slash.on': True,
        'tools.staticdir.root': os.path.abspath(os.path.dirname(jaraco.site.__file__)),
    })

    cherrypy.quickstart(Root(), '/', {
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'static'
        }
    })

if __name__ == '__main__':
    main()
