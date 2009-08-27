from __future__ import absolute_import

"""
Things to remember when deploying an isapi_wsgi app:
 - easy_install munges permissions on zip eggs (the easiest solution is to just install them with -Z)
 - any dependency that's installed in a user folder (i.e. setup develop) will probably not work due to insufficient permissions
"""

import sys
import os
import isapi_wsgi
import traceback
import isapi

if hasattr(sys, "isapidllhandle"):
	import win32traceutil

def setup_environment(entry_file):
	"""
	Set up the ISAPI environment. <entry_file> should be the
	script/dll that is the entry point for the application.
	"""
	global appdir
	appdir = os.path.dirname(__file__)
	egg_cache = os.path.join(appdir, 'egg-tmp')
	if not os.path.exists(egg_cache):
		os.makedirs(egg_cache)
		# todo: make sure NETWORK_SERVICE has write permission
	os.environ['PYTHON_EGG_CACHE'] = egg_cache
	os.chdir(appdir)

def setup_application():
	import jaraco.site
	print "starting cherrypy application server"
	app = jaraco.site.init()
	print "successfully set up the application"
	return app

def factory():
	"The entry point for when the ISAPIDLL is triggered"
	try:
		return isapi_wsgi.ISAPISimpleHandler(setup_application())
	except:
		f = open(os.path.join(appdir, 'critical error.txt'), 'w')
		traceback.print_exc(file=f)
		f.close()
		print "Traceback occurred starting up the application"
		traceback.print_exc()

def handle_command_line():
	"Install or remove the extension to the virtual directory"
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
		Server="Primary Web Site",
		Name="/",
		Description = "CherryPy Application",
		ScriptMaps = sm,
		ScriptMapUpdate = "end",
		)
	params.VirtualDirs = [vd]
	isapi.install.HandleCommandLine(params)
