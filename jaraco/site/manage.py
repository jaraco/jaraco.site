from __future__ import print_function

import os
import sys
import shutil
import subprocess

import pkg_resources

def install():
	"""
	Command to install the static content.
	"""
	base = r'\inetpub\jaraco.site'
	os.makedirs(base)
	scripts = ('create-iis-site.cmd isapiapp.py recycle-site.py serve.py '
		'update-site.cmd'.split())
	for script in scripts:
		script_name = 'scripts/' + script
		shutil.copy(pkg_resources.resource_filename('jaraco.site', script_name),
			os.path.join(base, script))
	create_site()
	register_isapi()

def create_site():
	app_cmd = r'\windows\system32\inetsrv\appcmd.exe'
	subprocess.check_call([
		app_cmd,
		'add', 'site',
		'/id:3', '/name:Primary Web Site',
		r'/physicalPath:c:\inetpub\jaraco.site',
		'/bindings:http/*:80:www.jaraco.com,https/*:443:www.jaraco.com',
		],
	)
	subprocess.check_call([
		app_cmd,
		'add', 'apppool',
		'/name:Primary Web Site',
	])
	subprocess.check_call([
		app_cmd,
		'set', 'app',
		'Primary Web Site/',
		'/applicationPool:Primary Web Site',
	])

def register_isapi():
	subprocess.check_call([
		sys.executable,
		'/inetpub/jaraco.site/isapiapp.py',
		'install',
		'--server=Primary Web Site',
	])
