import pytest
import mock
import argparse

from wurf.registry import Options


def test_bundle_path():

    default_path = 'bundle_dependencies'

    parser = argparse.ArgumentParser()
    args = ['--foo', '-b']

    options = Options(args=args, parser=parser,
        default_bundle_path=default_path,
        default_symlinks_path="", supported_git_protocols="")

    assert options.bundle_path() == default_path


    parser = argparse.ArgumentParser()
    args = ['--foo', '--bundle-path', '/tmp/bundlehere', '-b']

    options = Options(args=args, parser=parser, default_bundle_path="",
        default_symlinks_path="", supported_git_protocols="")

    assert options.bundle_path() == '/tmp/bundlehere'

    dependency = mock.Mock()
    dependency.name = 'foo'

    options.add_dependency(dependency)

    assert options.path(dependency=dependency) == None


def test_symlinks_path():

    default_path = 'build_symlinks'

    parser = argparse.ArgumentParser()
    args = ['--foo', '-b']

    options = Options(args=args, parser=parser, default_bundle_path="",
        default_symlinks_path=default_path, supported_git_protocols="")

    assert options.symlinks_path() == default_path

    parser = argparse.ArgumentParser()
    args = ['--foo', '--symlinks-path', '/tmp/symlinks', '-b']

    options = Options(args=args, parser=parser, default_bundle_path="",
        default_symlinks_path=default_path, supported_git_protocols="")

    assert options.symlinks_path() == '/tmp/symlinks'


def test_user_path_to_dependency():

    dependency = mock.Mock()
    dependency.name = 'foo'

    # Path specified
    parser = argparse.ArgumentParser()
    args = ['--foo', '--bundle-path', '/tmp/bundlehere',
            '--foo-path', '/home/stw/code', '-b']

    options = Options(args=args, parser=parser, default_bundle_path="",
        default_symlinks_path="", supported_git_protocols="")

    options.add_dependency(dependency)

    assert options.path(dependency=dependency) == '/home/stw/code'

    # Path specified
    parser = argparse.ArgumentParser()
    args = ['--foo', '--bundle-path', '/tmp/bundlehere',
            '--foo-path', '/home/stw/code1', '-b']

    options = Options(args=args, parser=parser, default_bundle_path="",
        default_symlinks_path="", supported_git_protocols="")

    options.add_dependency(dependency)

    assert options.path(dependency=dependency) == '/home/stw/code1'


def test_git_protocol():

    parser = argparse.ArgumentParser()
    args = ['--foo', '-b']

    options = Options(args=args, parser=parser, default_bundle_path="",
        default_symlinks_path="", supported_git_protocols="")

    assert options.git_protocol() == None

    parser = argparse.ArgumentParser()
    args = ['--foo', '--git-protocol', 'myproto://', '-b']

    options = Options(args=args, parser=parser, default_bundle_path="",
        default_symlinks_path="", supported_git_protocols="")

    assert options.git_protocol() == 'myproto://'


def test_fast_resolve():

    parser = argparse.ArgumentParser()
    args = ['--foo', '-b']

    options = Options(args=args, parser=parser, default_bundle_path="",
        default_symlinks_path="", supported_git_protocols="")

    assert options.fast_resolve() == False

    parser = argparse.ArgumentParser()
    args = ['--foo', '--fast-resolve', '-b']

    options = Options(args=args, parser=parser, default_bundle_path="",
        default_symlinks_path="", supported_git_protocols="")

    assert options.fast_resolve() == True
