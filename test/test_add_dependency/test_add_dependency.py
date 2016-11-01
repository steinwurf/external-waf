#!/usr/bin/env python
# encoding: utf-8

def test_add_dependency(test_directory):
    """ Integration testing of adding a dependency."""

    test_directory.copy_file('build/*/waf')
    test_directory.copy_file('test/test_add_dependency/wscript')

    # The bundle_dependencies directory is the default, so when we do
    # configure without any arguments dependencies are expected to be
    # placed there.
    bundle_directory = test_directory.mkdir('bundle_dependencies')


    bundle_directory.copy_dir('test/test_add_dependency/libfoo')

    ##libfoo_directory = bundle_directory.mkdir('libbar-h4sh')
    #libfoo_directory.copy_dir('test/test_add_dependency/libbar')

    r = test_directory.run('python', 'waf', 'configure', '-v')

    assert r.returncode == 0, str(r)

    r = test_directory.run('python', 'waf', 'build', '-v')

    assert r.returncode == 0, str(r)

    r = test_directory.run('python', 'waf', 'configure', '-v', '--waf-use-checkout=waf-1.9.4')

    assert r.returncode == 0, str(r)

    r = test_directory.run('python', 'waf', 'build', '-v')

    assert r.returncode == 0, str(r)

    r = test_directory.run('python', 'waf', 'configure', '-v', '--waf-path=/tmp')

    assert r.returncode == 0, str(r)

    r = test_directory.run('python', 'waf', 'build', '-v')

    assert r.returncode == 0, str(r)


    print(str(r))
