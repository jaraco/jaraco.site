#!python

"""
Things to remember:
easy_install munges permissions on zip eggs.
anything that's installed in a user folder (i.e. setup develop) will probably not work.
There may still exist an issue with static files.
"""


import sys
import os
import isapi_wsgi

if hasattr(sys, "isapidllhandle"):
	import win32traceutil

appdir = os.path.dirname(__file__)
egg_cache = os.path.join(appdir, 'egg-tmp')
if not os.path.exists(egg_cache):
	os.makedirs(egg_cache)
os.environ['PYTHON_EGG_CACHE'] = egg_cache
os.chdir(appdir)

import traceback

def setup_application():
	print "starting cherrypy application server"
	import jaraco.site
	app = jaraco.site.init()
	print "successfully set up the application"
	return app

def __ExtensionFactory__():
	"The entry point for when the ISAPIDLL is triggered"
	try:
		# import the wsgi app creator
		app = setup_application()
		return isapi_wsgi.ISAPISimpleHandler(app)
	except:
		f = open(os.path.join(appdir, 'critical error.txt'), 'w')
		traceback.print_exc(file=f)
		f.close()

def install_virtual_dir():
	import isapi.install
	params = isapi.install.ISAPIParameters()
	# Setup the virtual directories - this is a list of directories our
	# extension uses - in this case only 1.
	# Each extension has a "script map" - this is the mapping of ISAPI
	# extensions.
	sm = [
		isapi.install.ScriptMapParams(Extension="*", Flags=0)
	]
	vd = isapi.install.VirtualDirParameters(
		Server="CherryPy Web Server",
		Name="/",
		Description = "CherryPy Application",
		ScriptMaps = sm,
		ScriptMapUpdate = "end",
		)
	params.VirtualDirs = [vd]
	isapi.install.HandleCommandLine(params)
	
if __name__=='__main__':
	# If run from the command-line, install ourselves.
	install_virtual_dir()
