from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm

packages = ['poster']

env.hosts = ['root@md.stage.01']

def staging():
    for package in packages:
        run('pip install %s' % package)

    with cd('/usr/local/www/dashboard'):
        run("git pull")
        run("git status")
    run("service apache2 restart")