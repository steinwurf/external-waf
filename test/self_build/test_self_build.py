#!/usr/bin/env python
# encoding: utf-8

import os
import pytest


@pytest.mark.networktest
def test_self_build(testdirectory):
    root = testdirectory

    # Note: waf will call "git config --get remote.origin.url" in this folder,
    # so "git init" is required to test the default behavior (https resolver)
    root.run("git init")

    src_dir = root.mkdir("src")
    src_dir.copy_dir(directory="src/wurf")
    root.copy_file("wscript")
    root.copy_file("build/waf")

    r = root.run("python waf configure")

    assert r.returncode == 0
    assert r.stdout.match("*finished successfully*")

    # Configure again with an existing "resolved_dependencies" folder
    r = root.run("python waf configure")

    assert r.returncode == 0
    assert r.stdout.match("*finished successfully*")

    r = root.run("python waf build")

    assert r.returncode == 0

    waf_path = os.path.join(root.path(), "build", "waf")

    assert os.path.isfile(waf_path)
