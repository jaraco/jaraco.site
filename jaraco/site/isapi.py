"""
Things to remember when deploying an isapi_wsgi app:
	- easy_install munges permissions on zip eggs (the easiest solution is to
	just install them with -Z)
	- any dependency that's installed in a user folder (i.e. setup develop)
	will probably not work due to insufficient permissions
"""

from __future__ import absolute_import, print_function

import sys
import os
import traceback
import importlib

import isapi_wsgi
import isapi.install

import jaraco.site

if hasattr(sys, "isapidllhandle"):
	importlib.import_module('win32traceutil')

appdir = None

def setup_environment(entry_file):
	"""
	Set up the ISAPI environment. <entry_file> should be the
	script/dll that is the entry point for the application.
	"""
	global appdir
	appdir = os.path.dirname(entry_file)
	egg_cache = os.path.join(appdir, 'egg-tmp')
	if not os.path.exists(egg_cache):
		os.makedirs(egg_cache)
		# todo: make sure NETWORK_SERVICE has write permission
	os.environ['PYTHON_EGG_CACHE'] = egg_cache
	os.chdir(appdir)

def setup_application():
	print("starting cherrypy application server")
	app = jaraco.site.init()
	print("successfully set up the application")
	return app

def factory():
	"The entry point for when the ISAPIDLL is triggered"
	try:
		return isapi_wsgi.ISAPISimpleHandler(setup_application())
	except:
		print("Traceback occurred starting up the application")
		traceback.print_exc()
		with open(os.path.join(appdir, 'critical error.txt'), 'w') as f:
			traceback.print_exc(file=f)

def handle_command_line():
	"Install or remove the extension to the virtual directory"
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
