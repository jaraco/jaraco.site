"""
Routines for installing, staging, and serving jaraco.com on Ubuntu.

To install on a clean Ubuntu Bionic box, simply run
fab bootstrap
"""

import itertools

from fabric import task
from jaraco.fabric import files
from jaraco.fabric import monkey

flatten = itertools.chain.from_iterable

host = 'spidey'
hosts = [host]

project = 'jaraco.site'
site = 'jaraco.com'
install_root = '/opt/jaraco.com'
python = 'python3.8'
ubuntu = 'jaraco/site/ubuntu'


@task(hosts=hosts)
def bootstrap(c):
    install_dependencies(c)
    install_env(c)
    install_service(c)
    update(c)
    configure_nginx(c)
    install_cert(c)
    install_scicomm(c)


@task(hosts=hosts)
def install_dependencies(c):
    # fop required by the resume endpoint
    c.sudo('apt install -y fop')
    # certbot for certificates
    c.sudo('apt-add-repository -y ppa:certbot/certbot')
    c.sudo('apt update -y')
    c.sudo('apt install -y python-certbot-nginx')

    c.sudo('apt install -y software-properties-common')
    c.sudo('add-apt-repository -y ppa:deadsnakes/ppa')
    c.sudo('apt update -y')
    c.sudo(f'apt install -y {python} {python}-venv')


def create_env(c, root):
    user = c.run('whoami').stdout.strip()
    c.sudo(f'mkdir -p {root}')
    c.sudo(f'chown {user} {root}')


@task(hosts=hosts)
@monkey.workaround_2090
def install_env(c):
    c.sudo(f'rm -R {install_root} || echo -n')
    create_env(c, install_root)
    c.run(f'{python} -m venv {install_root}')
    c.run(f'{install_root}/bin/python -m pip install -U pip')


@task(hosts=hosts)
def install_service(c):
    files.upload_template(
        c,
        f"{ubuntu}/{project}.service",
        "/etc/systemd/system",
        context=globals(),
    )
    c.sudo(f'systemctl enable {project}')


@task(hosts=hosts)
@monkey.workaround_2090
def update(c):
    install(c)
    install_scicomm(c)
    c.sudo(f'systemctl restart {project}')


def install(c):
    """
    Install project to environment at root.
    """
    c.run(f'git clone https://github.com/jaraco/{project} || echo -n')
    c.run(f'git -C {project} pull')
    c.run(f'{install_root}/bin/python -m pip install -U ./{project}')


@task(hosts=hosts)
@monkey.workaround_2090
def install_scicomm(c):
    root = '/opt/scicomm.pro'
    create_env(c, root)
    c.run(f'git clone https://github.com/jaraco/scicomm.pro {root} || echo -n')
    c.run(f'git -C {root} pull')


@task(hosts=hosts)
def remove_all(c):
    c.sudo(f'systemctl stop {project} || echo -n')
    c.sudo(f'rm /etc/systemd/system/{project}.service')
    c.sudo(f'rm -Rf {install_root}')


@task(hosts=hosts)
@monkey.workaround_2090
def configure_nginx(c):
    c.sudo('apt install -y nginx')
    source = f"{ubuntu}/nginx config"
    target = f"/etc/nginx/sites-available/{site}"
    files.upload_template(c, src=source, dest=target)
    c.sudo(f'ln -sf ../sites-available/{site} /etc/nginx/sites-enabled/')
    c.sudo('service nginx restart')


@task(hosts=hosts)
def install_cert(c):
    cmd = [
        'certbot',
        '--agree-tos',
        '--email',
        'jaraco@jaraco.com',
        '--non-interactive',
        '--nginx',
        'certonly',
    ]
    sites = (
        'jaraco.com',
        'www.jaraco.com',
        'blog.jaraco.com',
        'www.recapturedocs.com',
        'scicomm.pro',
        'www.scicomm.pro',
    )
    cmd += list(flatten(['--domain', name] for name in sites))
    c.sudo(' '.join(cmd))
