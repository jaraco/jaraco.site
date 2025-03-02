"""
Routines for installing, staging, and serving jaraco.com on Ubuntu.

To install on an Ubuntu box, run

fab bootstrap
"""

import functools
import re
import textwrap

from fabric import task

from jaraco.fabric import certs, files, monkey

host = 'kelvin'
hosts = [host]

project = 'jaraco.site'
site = 'jaraco.com'
install_root = '/opt/jaraco.com'
python = 'python3'
ubuntu = 'jaraco/site/ubuntu'


@task(hosts=hosts)
def bootstrap(c):
    install_dependencies(c)
    install_env(c)
    install_service(c)
    update(c)
    configure_nginx(c)
    install_cert(c)
    enable_nginx(c)


@task(hosts=hosts)
def install_dependencies(c):
    # fop required by the resume endpoint
    c.sudo('apt install -y fop')

    install_certbot(c)

    c.sudo('apt install -y python3-venv')


@task(hosts=hosts)
def install_certbot(c):
    # certbot for certificates
    # https://certbot.eff.org/instructions?ws=nginx&os=ubuntufocal
    c.sudo('snap install --classic certbot')
    # c.sudo('ln -s /snap/bin/certbot /usr/bin/certbot')


def create_env(c, root):
    user = c.run('whoami').stdout.strip()
    c.sudo(f'mkdir -p {root}')
    c.sudo(f'chown {user} {root}')


@task(hosts=hosts)
@monkey.workaround_2090
def install_env(c):
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
    configure_nginx_restart(c)
    c.sudo('service nginx restart')


@task(hosts=hosts)
def configure_nginx_restart(c):
    """
    Configures Nginx on an Ubuntu 24.04 server to restart on failure after 60 seconds,
    because sometimes it restarts and fails to restart if there are DNS issues.
    (jaraco/jaraco.site#3)
    """
    service_file = "/lib/systemd/system/nginx.service"
    section = '[Service]'
    insertion = (
        textwrap.dedent(
            """
            Restart=on-failure
            RestartSec=60s
            """
        )
        .rstrip()
        .replace('\n', '\\n')
    )

    instruction = f's/{re.escape(section)}/{section}{insertion}/'
    cmd = f"sed -i {escape_for_shell(c, instruction)} {service_file}"
    c.sudo(cmd)
    c.sudo("systemctl daemon-reload")
    c.sudo("systemctl restart nginx")


@functools.cache
def get_shell(c):
    return c.run('echo $SHELL', hide=True).stdout


def escape_for_shell(c, param):
    shell = get_shell(c)
    if 'xonsh' in shell:
        return repr(param)
    return f"'{param}'"


@task(hosts=hosts)
def enable_nginx(c):
    # only enable after certificates are installed
    c.sudo(f'ln -sf ../sites-available/{site} /etc/nginx/sites-enabled/')
    c.sudo('service nginx restart')


@task(hosts=hosts)
def install_cert(c):
    certs.install(c, 'jaraco.com', 'www.jaraco.com', 'blog.jaraco.com')
    certs.install(c, 'scicomm.pro', 'www.scicomm.pro')
