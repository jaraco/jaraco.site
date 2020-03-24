"""
Routines for installing, staging, and serving jaraco.com on Ubuntu.

To install on a clean Ubuntu Bionic box, simply run
fab bootstrap
"""

from fabric.api import sudo, run, task, env
from fabric.contrib import files
from more_itertools import flatten

if not env.hosts:
    env.hosts = ['spidey']

install_root = '/opt/jaraco.com'


python = 'python3.8'


@task
def bootstrap():
    install_dependencies()
    install_env()
    install_service()
    update()
    configure_nginx()
    install_cert()


@task
def install_dependencies():
    # fop required by the resume endpoint
    sudo('apt install -y fop')
    # certbot for certificates
    sudo('apt-add-repository -y ppa:certbot/certbot')
    sudo('apt update -y')
    sudo('apt install -y python-certbot-nginx')

    sudo('apt install -y software-properties-common')
    sudo('add-apt-repository -y ppa:deadsnakes/ppa')
    sudo('apt update -y')
    sudo(f'apt install -y {python} {python}-venv')


@task
def install_env():
    user = run('whoami')
    sudo(f'rm -R {install_root} || echo -n')
    sudo(f'mkdir -p {install_root}')
    sudo(f'chown {user} {install_root}')
    run(f'{python} -m venv {install_root}')
    run(f'{install_root}/bin/python -m pip install -U pip')


@task
def install_service():
    files.upload_template(
        "ubuntu/jaraco.site.service",
        "/etc/systemd/system",
        use_sudo=True,
        context=globals(),
    )
    sudo('systemctl enable jaraco.site')


@task
def update():
    install()
    sudo('systemctl restart jaraco.site')


def install():
    """
    Install jaraco.site to environment at root.
    """
    run('git clone https://github.com/jaraco/jaraco.site || echo -n')
    run('git -C jaraco.site pull')
    run(f'{install_root}/bin/python -m pip install -U ./jaraco.site')


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
    sudo('ln -sf ../sites-available/jaraco.com /etc/nginx/sites-enabled/')
    sudo('service nginx restart')


@task
def install_cert():
    sites = ('jaraco.com', 'www.jaraco.com', 'blog.jaraco.com', 'www.recapturedocs.com')
    cmd = ['certbot', '--agree-tos', '--non-interactive', '--nginx', 'certonly'] + list(
        flatten(['--domain', name] for name in sites)
    )
    sudo(' '.join(cmd))
