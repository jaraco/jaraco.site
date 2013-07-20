from __future__ import print_function

import os
import sys
import shutil
import subprocess

import six
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

def appcmd(cmd, **kwargs):
	if isinstance(cmd, six.string_types):
		cmd = cmd.split()
	args = [
		'/{key}:{value}'.format(**vars())
		for key, value in kwargs.items()
	]
	return subprocess.check_call([
		r'\Windows\System32\InetSrv\appcmd.exe',
		] + cmd + args)

bindings = 'http/*:80:www.jaraco.com,https/*:443:www.jaraco.com'

def reset_bindings():
	"""
	Creating the site unfortunately doesn't assign the certificate, and
	setting the certificate manually disallows setting the https hostname,
	so the bindings need to be reset.
	See http://sarafianalex.wordpress.com/2010/08/04/setting-host-name-on-ssl-binding-on-iis7/
	"""
	appcmd(
		'set site',
		name = 'Primary Web Site',
		bindings = bindings,
	)

def create_site():
	appcmd(
		'add site',
		id=3,
		name = 'Primary Web Site',
		physicalPath = r'C:\InetPub\jaraco.site',
		bindings = bindings,
	)
	appcmd('add apppool', name='Primary Web Site')
	appcmd('set app', name="Primary Web Site",
		applicationPool="Primary Web Site")

def register_isapi():
	subprocess.check_call([
		sys.executable,
		'/inetpub/jaraco.site/isapiapp.py',
		'install',
		'--server=Primary Web Site',
	])
