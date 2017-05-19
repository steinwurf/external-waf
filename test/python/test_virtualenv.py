#!/usr/bin/env python
# encoding: utf-8

import os
import sys
import pytest
import mock
import fnmatch

from wurf.virtualenv import VirtualEnv

def test_virtualenv_noname(test_directory):

    cwd = test_directory.path()
    env = dict(os.environ)
    name = None
    ctx = mock.Mock()
    pip_packages_path = '/tmp/pip_packages'

    venv = VirtualEnv.create(cwd=cwd, env=env, name=name, ctx=ctx,
        pip_packages_path=pip_packages_path)

    assert fnmatch.fnmatch(venv.path, os.path.join(cwd, 'virtualenv-*'))



def test_virtualenv_name(test_directory):

    cwd = test_directory.path()
    env = dict(os.environ)
    name = 'gogo'
    ctx = mock.Mock()
    pip_packages_path = '/tmp/pip_packages'

    # Lets make the directory to make sure it is removed
    test_directory.mkdir(name)
    assert test_directory.contains_dir(name)

    venv = VirtualEnv.create(cwd=cwd, env=env, name=name, ctx=ctx,
        pip_packages_path=pip_packages_path)

    assert fnmatch.fnmatch(venv.path, os.path.join(cwd, name))
    assert not test_directory.contains_dir(name)

    ctx.cmd_and_log.assert_called_once_with(
        [sys.executable,'-m', 'virtualenv', name, '--no-site-packages'],
        cwd=cwd, env=env)

    venv.pip_download('pytest', 'twine')

    ctx.exec_command.assert_called_once_with(
        'python -m pip download pytest twine --dest /tmp/pip_packages',
        cwd=venv.cwd, env=venv.env, stdout=None, stderr=None)

    # reset state
    ctx.exec_command = mock.Mock()

    # We have to make sure the pip_packages_path exists

    venv.pip_local_install('pytest', 'twine')

    ctx.exec_command.assert_called_once_with(
        'python -m pip install pytest twine --no-index '\
        '--find-links=/tmp/pip_packages',
        cwd=venv.cwd, env=venv.env, stdout=None, stderr=None)
