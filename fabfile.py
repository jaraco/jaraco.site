"""
Routines for installing, staging, and serving recapturedocs on Ubuntu.

To install on a clean Ubuntu Trusty box, simply run
fab bootstrap
"""

import contextlib
import os
import subprocess

from fabric.api import sudo, run, task, env
from fabric.context_managers import shell_env
from fabric.contrib import files
from jaraco.text import local_format as lf

if not env.hosts:
	env.hosts = ['elektra']

install_root = '/opt/jaraco.com'

@task
def bootstrap():
	install_env()
	update()
	configure_nginx()

@task
def install_env():
	sudo('rm -R {install_root} || echo -n'.format(**globals()))
	sudo('aptitude install -y python3-lxml')
	install_upstart_conf()

@task
def install_upstart_conf(install_root=install_root):
	sudo(lf('mkdir -p {install_root}'))
	files.upload_template("ubuntu/jaraco-site.conf", "/etc/init",
		use_sudo=True, context=vars())

@task
def update(version=None):
	install_to(install_root, version, use_sudo=True)
	sudo('restart jaraco-site || start jaraco-site')

def install_to(root, version=None, use_sudo=False):
	"""
	Install jaraco.site to a PEP-370 environment at root. If version is
	not None, install that version specifically. Otherwise, use the latest.
	"""
	action = sudo if use_sudo else run
	pkg_spec = 'jaraco.site'
	if version:
		pkg_spec += '==' + version
	action('mkdir -p {root}/lib/python3.4/site-packages'.format(**locals()))
	with shell_env(PYTHONUSERBASE=root):
		cmd = [
			'python3', '-m',
			'easy_install',
			'--user',
			'-U',
			pkg_spec,
		]
		action(' '.join(cmd))

@task
def remove_all():
	sudo('stop jaraco-site || echo -n')
	sudo('rm /etc/init/jaraco-site.conf || echo -n')
	sudo('rm -Rf /opt/jaraco.com')

@task
def configure_nginx():
	sudo('aptitude install -y nginx')
	source = "ubuntu/nginx config"
	target = "/etc/nginx/sites-available/jaraco.com"
	files.upload_template(filename=source, destination=target, use_sudo=True)
	sudo(
		'ln -sf '
		'../sites-available/jaraco.com '
		'/etc/nginx/sites-enabled/'
	)
	if not files.exists('/opt/jaraco.com/jaraco.com.pem'):
		install_cert()
	sudo('service nginx restart')

@task
def install_cert():
	with generate_pem() as source:
		target = '/opt/jaraco.com/'
		files.upload_template(filename=source, destination=target,
			use_sudo=True)

@contextlib.contextmanager
def generate_pem():
	root = os.path.expanduser('~/Documents/Computing/Certificates')
	source = os.path.join(root, 'star.jaraco.com (2013).pfx')
	target = 'jaraco.com.pem'
	cmd = [
		'openssl',
		'pkcs12',
		'-in', source,
		'-out', target,
		'-nodes',
	]
	subprocess.check_call(cmd)
	try:
		yield target
	finally:
		os.remove(target)
