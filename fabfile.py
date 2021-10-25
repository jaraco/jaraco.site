"""
Routines for installing, staging, and serving jaraco.com on Ubuntu.

To install on a clean Ubuntu Bionic box, simply run
fab bootstrap
"""

import itertools

from fabric import task
from jaraco.fabric import files

flatten = itertools.chain.from_iterable

host = 'spidey'
hosts = [host]

install_root = '/opt/jaraco.com'


python = 'python3.8'


@task(hosts=hosts)
def bootstrap(c):
    install_dependencies(c)
    install_env(c)
    install_service(c)
    update(c)
    configure_nginx(c)
    install_cert(c)


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


@task(hosts=hosts)
def install_env(c):
    user = c.run('whoami')
    c.sudo(f'rm -R {install_root} || echo -n')
    c.sudo(f'mkdir -p {install_root}')
    c.sudo(f'chown {user} {install_root}')
    c.run(f'{python} -m venv {install_root}')
    c.run(f'{install_root}/bin/python -m pip install -U pip')


@task(hosts=hosts)
def install_service(c):
    files.upload_template(
        "ubuntu/jaraco.site.service",
        "/etc/systemd/system",
        use_sudo=True,
        context=globals(),
    )
    c.sudo('systemctl enable jaraco.site')


@task(hosts=hosts)
def update(c):
    install(c)
    c.sudo('systemctl restart jaraco.site')


def install(c):
    """
    Install jaraco.site to environment at root.
    """
    c.run('git clone https://github.com/jaraco/jaraco.site || echo -n')
    c.run('git -C jaraco.site pull')
    c.run(f'{install_root}/bin/python -m pip install -U ./jaraco.site')


@task(hosts=hosts)
def remove_all(c):
    c.sudo('stop jaraco.site || echo -n')
    c.sudo('rm /etc/init/jaraco-site.conf || echo -n')
    c.sudo('rm -Rf /opt/jaraco.com')


@task(hosts=hosts)
def configure_nginx(c):
    c.sudo('apt install -y nginx')
    source = "ubuntu/nginx config"
    target = "/etc/nginx/sites-available/jaraco.com"
    files.upload_template(c, src=source, dest=target)
    c.sudo('ln -sf ../sites-available/jaraco.com /etc/nginx/sites-enabled/')
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
