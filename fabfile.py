"""
Routines for installing, staging, and serving jaraco.com on Ubuntu.

To install on a clean Ubuntu Xenial box, simply run
fab bootstrap
"""

from fabric.api import sudo, run, task, env
from fabric.contrib import files
from more_itertools.recipes import flatten

if not env.hosts:
	env.hosts = ['punisher']

install_root = '/opt/jaraco.com'


@task
def bootstrap():
	install_dependencies()
	install_env()
	update()
	install_service()
	configure_nginx()
	install_cert()


@task
def install_dependencies():
	# fop required by the resume endpoint
	sudo('apt install -y fop')
	# lets encrypt for certificates
	sudo('apt install -y letsencrypt')

	sudo('apt install -y software-properties-common')
	sudo('add-apt-repository -y ppa:deadsnakes/ppa')
	sudo('apt update -y')
	sudo('apt install -y python3.6 python3.6-venv')


@task
def install_env():
	user = run('whoami')
	sudo(f'rm -R {install_root} || echo -n')
	sudo(f'mkdir -p {install_root}')
	sudo(f'chown {user} {install_root}')
	run(f'python3.6 -m venv {install_root}')
	run(f'{install_root}/bin/python -m pip install -U setuptools')


@task
def install_service():
	files.upload_template(
		"ubuntu/jaraco.site.service", "/etc/systemd/system",
		use_sudo=True, context=globals())
	sudo('systemctl enable jaraco.site')


@task
def update():
	install()
	sudo('systemctl restart jaraco.site')


def install():
	"""
	Install jaraco.site to a PEP-370 environment at root. If version is
	not None, install that version specifically. Otherwise, use the latest.
	"""
	run('git clone https://github.com/jaraco/jaraco.site || echo -n')
	run('git -C jaraco.site pull')
	run(f'{install_root}/bin/python -m pip install ./jaraco.site')


@task
def remove_all():
	sudo('stop jaraco.site || echo -n')
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
