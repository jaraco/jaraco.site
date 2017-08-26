"""
Routines for installing, staging, and serving recapturedocs on Ubuntu.

To install on a clean Ubuntu Trusty box, simply run
fab bootstrap
"""

from fabric.api import sudo, run, task, env
from fabric.context_managers import shell_env
from fabric.contrib import files
from jaraco.text import local_format as lf
from more_itertools.recipes import flatten

if not env.hosts:
	env.hosts = ['punisher']

install_root = '/opt/jaraco.com'


@task
def bootstrap():
	install_dependencies()
	install_env()
	update()
	configure_nginx()
	install_cert()


@task
def install_dependencies():
	# fop required by the resume endpoint
	sudo('apt install -y fop')
	# lets encrypt for certificates
	sudo('apt install -y letsencrypt')


@task
def install_env():
	sudo('rm -R {install_root} || echo -n'.format(**globals()))
	sudo('apt -q install -y python3-lxml python3-pip')
	install_service()


@task
def install_service(install_root=install_root):
	sudo(lf('mkdir -p {install_root}'))
	files.upload_template(
		"ubuntu/jaraco.site.service", "/etc/systemd/system",
		use_sudo=True, context=vars())
	sudo('systemctl enable jaraco.site')


@task
def update(version=None):
	install_to(install_root, version, use_sudo=True)
	sudo('systemctl restart jaraco.site')


def install_to(root, version=None, use_sudo=False):
	"""
	Install jaraco.site to a PEP-370 environment at root. If version is
	not None, install that version specifically. Otherwise, use the latest.
	"""
	action = sudo if use_sudo else run
	pkg_spec = 'jaraco.site'
	if version:
		pkg_spec += '==' + version
	with shell_env(PYTHONUSERBASE=root):
		usp = run('python3 -c "import site; print(site.getusersitepackages())"')
		action('mkdir -p {usp}'.format(**locals()))
		# can't run with '-U' because that will cause lxml to upgrade/build
		cmd = [
			'python3',
			'-m', 'pip',
			'install',
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
	sudo('apt install -y nginx')
	source = "ubuntu/nginx config"
	target = "/etc/nginx/sites-available/jaraco.com"
	files.upload_template(filename=source, destination=target, use_sudo=True)
	sudo(
		'ln -sf '
		'../sites-available/jaraco.com '
		'/etc/nginx/sites-enabled/'
	)
	sudo('service nginx restart')


@task
def install_cert():
	sudo('service nginx stop')
	sites = 'jaraco.com', 'www.jaraco.com', 'blog.jaraco.com'
	opts = flatten(['-d', name] for name in sites)
	sudo('letsencrypt certonly ' + ' '.join(opts))
	sudo('service nginx start')
