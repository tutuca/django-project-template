#!/usr/bin/env python
#-- coding: utf-8 --

"""Deployment script.
This script is coded so it can make the deployments automagically in the
designed servers, it also works as a documentation of where are the programs
installed.
USE: fab <hosts>:<username> <action>
EX: fab staging:admin release
"""
import os
import datetime
from contextlib import contextmanager
from os.path import expanduser
from fabric.api import env, run, local, require, put, cd, lcd, prefix
from fabric.utils import puts
from fabric.contrib.files import exists


env.project_name = '{{project_name}}'

env.tar = '%s-%s.tar.gz' % (
    env.project_name,
    datetime.datetime.now().strftime('%Y%m%d%H%M%S'),
)
env.bundle = '%s-static.tar.gz' % (
    env.project_name,
)
env.use_ssh_config = True

@contextmanager
def virtualenv():
    with prefix('. %(venv_dir)s/bin/activate' % env):
        yield

def production(username, host):
    """Production environment."""
    env.hosts = host
    env.user = username
    base_dir = '/home/%s' % username
    env.static_dir = os.path.join(base_dir,'webapps', '%s_web' % env.project_name)
    env.deploy_dir = os.path.join(base_dir, 'webapps', '%s_service' % env.project_name)
    env.venv_dir = os.path.join(base_dir, 'venvs', env.project_name)
    env.server_command = os.path.join(env.deploy_dir, 'apache2/bin/restart')


def setup_env():
    """
    Creates required directories for deployment.
    It also attempts to install pip requirements on remote host.
    While not intended you might run it for local setup.
    """

    dirs = (env[x] for x in env if x.endswith('_dir'))

    for directory in dirs:
        if not exists(directory):
            run('mkdir -p %s' % directory)

    if not exists('%(venv_dir)s/bin/activate' % env):
        run('virtualenv -q -ppython3 %(venv_dir)s' % env)

    put('service/requirements.txt', 'requirements.txt')

    with virtualenv():
        run('pip -q install -U pip')
        run('pip -q install -Ur requirements.txt')


def upload_service(rev='HEAD'):
    """
    Create a tarball honoring git's ignored and non-tracked files,
    uploads it and decompresses it in the rigth path.
    """
    require('host', provided_by=[production])
    require('deploy_dir', provided_by=[production])
    require('venv_dir', provided_by=[production])
    
    tar = env.tar
    with lcd('service'):
        local('git archive %s -o %s' % (rev, tar))
        put(tar, tar)
        
        run('tar xfz %s -C %s' % (tar, env.deploy_dir))
        run('rm %s' % tar)
        local('rm %s' % tar)


def build_static_bundle():
    """
    Create a tarball of the static files
    to be uploaded later.
    It invokes django's collectstatic method and
    runs a regular grunt build.
    Requires your local development environment to be activated and the
    `{{project_name}}` management command to be available.
    """
    
    require('project_name', provided_by=[production])
    require('static_dir')
    require('bundle')

    local('{{project_name}} collectstatic --noinput')
    
    with lcd('web'):
        local('grunt build')
        local('tar cf %s -C ./build/ .' % env.bundle)
        local('mv %s ../' % env.bundle)


def upload_static(force=False):
    """
    Uploads `env.bundle` and decompresses it in the right path
    This will attempt to create and delete local gzips. 
    Cleanup is not always what it should...
    """
    require('project_name', provided_by=[production])
    require('static_dir', provided_by=[production])

    bundle_path = os.path.join(os.path.dirname(__file__), env.bundle)
    
    if force or not os.path.exists(bundle_path):
        build_static_bundle()

    put(bundle_path, env.bundle)

    run('tar xf %s -C %s' % (env.bundle, env.static_dir))    
    run('rm %s' % env.bundle)
    local('rm %s' % bundle_path)

def release(rev='HEAD', force=False):
    """
    End-to-end release.
    It's a wrapper for the other functions.
    """
    require('host', provided_by=[production])
    setup_env()
    upload_service(rev=rev)
    upload_static(force=force)


def apache_restart():
    """Restart the program in the servers."""
    require('server_command', provided_by=[production])
    run(env.server_command)
