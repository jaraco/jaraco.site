#!/usr/bin/env python

import cherrypy
import jaraco.site

def main():
	# Some global configuration; note that this could be moved into a
	# configuration file
	jaraco.site.init()
	cherrypy.engine.start()

if __name__ == '__main__':
	main()
