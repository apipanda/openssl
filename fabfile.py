"""
Summary.

Attributes:
    local_dir (str): Description
    PRODUCTION (str): Description
    remote_dir (str): Description
    REMOTE_USER (str): Description
    STAGING (str): Description
"""
from fabric.api import (local, cd, run, task, env, sudo,
                        open_shell, put, get)


# STAGING = '162.243.53.17'
# PRODUCTION = '104.196.59.185'
REMOTE_USER = 'root'

# local_dir = './'
# remote_dir = '/site'

# env.hosts = [
#     # STAGING,
#     PRODUCTION
# ]

# env.key_filename = '~/.ssh/google_compute_engine.pub'
env.colorize_errors = True
env.user = REMOTE_USER


@task
def dev(port=8000):
    """Run local webserver.

    Args:
        port (int, optional): Description
    """
    local("./manage.py runserver %s:%s" % ('127.0.0.1', port))


@task
def install(version=""):
    """Install project artifacts.

    Args:
        version (str, optional): Description
    """
    local("pip install -r requirements.txt")
    local("python%s manage.py makemigrations" % version)
    local("python%s manage.py syncdb" % version)
    local("python%s manage.py schemamigration --initial app" % version)
    local("python%s manage.py migrate" % version)
    local("python%s manage.py createsuperuser" % version)


@task
def clean():
    """Remove all the .pyc files."""
    local("find . -name '*.pyc' -print0|xargs -0 rm", capture=False)


@task
def push(msg):
    """Push to github.

    Args:
        msg (str, required): Description
    """
    local("git add . && git commit -m '{}'".format(msg))
    local("git push")


# @task
# def deploy(msg="deploy to server"):
#     """Deploy the app to the live server on Digital Ocean.

#     Deleted Parameters:
#         msg (str, optional): Description
#     """
#     clean()
#     push(msg)
#     server = run("cd {}".format(remote_dir))
#     if server.succeeded:
#         with cd(remote_dir):
#             remote_pull = run("git pull")
#             if remote_pull.succeeded:
#                 deps_install = run("pip install -r requirements.txt")
#                 if deps_install.succeeded:
#                     print("Deployment was successful")
#     if server.failed:
#         print("Something bad happened!!", server)


# @task
# def launch():
#     """
#     Summary.

#     Returns:
#         TYPE: Description
#     """
#     server = run("cd {}".format(remote_dir))
#     if server.succeeded:
#         with cd(remote_dir):
#             sudo("service gunicorn restart")
#             sudo("service nginx restart")
#             print("New VERSION was launched successfully")


@task
def debug():
    """
    Summary.

    Returns:
        TYPE: Description
    """
    server = run("cd {}".format(remote_dir))
    if server.succeeded:
        with cd(remote_dir):
            open_shell()


@task
def ssl():
    """
    Summary.

    Returns:
        TYPE: Description
    """
    key = put('./key', '/key')
    if key.succeeded:
        sudo('cat /key >> ~/.ssh/authorized_keys ')
        # sudo('cat /key | ssh root@162.243.113.95 "cat >> ~/.ssh/authorized_keys" ')


@task
def config():
    """
    Summary.

    Returns:
        TYPE: Description
    """
    put('.env', '~/.env')
    env = run('cat ~/.env > ~/.bashrc')
    if env.succeeded:
        # sudo("mv /etc/init/gunicorn.conf /etc/init/gunicorn.conf.bak")
        # Refresh Bash
        # run('exec bash')
        gunicorn = put('gunicorn.conf', '/etc/init/gunicorn.conf')
        if gunicorn.succeeded:
            # sudo(
            #     'mv /etc/nginx/sites-available/django\
            #      /etc/nginx/sites-available/django.bak')
            nginx = put('django', '/etc/nginx/sites-available/django')
            if nginx.succeeded:
                print('Deployed config.')
                launch()


@task
def provision(name="", email=""):
    """
    Summary.

    Args:
        name (str, optional): Description
        email (str, optional): Description

    Returns:
        TYPE: Description
    """
    server = run("cd {}".format(remote_dir))
    if server.succeeded:
        deps = sudo("apt-get update")
        if deps.succeeded:
            git = sudo(
                'apt-get install git mysql-server libmysqlclient-dev -y')
            if git.succeeded:
                run("git config --global user.email %s" % email)
                run("git config --global user.name %s" % name)
                sudo('mysql_install_db')
                sudo('/usr/bin/mysql_secure_installation')

                pydev = sudo("sudo apt-get install python-dev")
                if pydev.succeeded:
                    sudo("sudo apt-get install libevent-dev")
