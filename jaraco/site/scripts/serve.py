#!/usr/bin/env python

import cherrypy
import jaraco.site

def main():
	jaraco.site.init()
	cherrypy.config.update({
		'server.socket_host': '0.0.0.0',
		})
	cherrypy.engine.start()

if __name__ == '__main__':
	main()
