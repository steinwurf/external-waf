import os
import sys
import subprocess
import glob
import time
import fnmatch

import pytest
import py

def run_command(args):
    print("Running: {}".format(args))
    sys.stdout.flush()
    subprocess.check_call(args)

run_string = """RunResult
stdout:\n{}
stderr:\n{}
returncode:\n{}
time:\n{}"""

class CheckOutput:
    def __init__(self, output):
        self.output = output.splitlines()

    def match(self, pattern):

        match_lines = fnmatch.filter(self.output, pattern)
        return len(match_lines) > 0

    def __str__(self):
        return '\n'.join(self.output)

class RunResult:
    def __init__(self, command, stdout, stderr, returncode, time):
        self.command = command
        self.stdout = CheckOutput(stdout)#CheckOutput(stdout.decode('utf-8'))
        self.stderr = CheckOutput(stdout)#CheckOutput(stderr.decode('utf-8'))
        self.returncode = returncode
        self.time = time

    def __str__(self):
        return run_string.format(self.stdout, self.stderr, self.returncode, self.time)

class TestDir:
    def __init__(self, request, tmpdir):
        self.tmpdir = tmpdir

    def dir(self):
        return self.tmpdir

    def copy_file(self, filename):

        # Expand filename by expanding wildcards e.g. 'dir/*/file.txt', the
        # glob should return only one file
        files = glob.glob(filename)

        assert len(files) == 1

        filename = files[0]

        # Copy the file to the tmpdir
        filepath = py.path.local(filename)
        filepath.copy(self.tmpdir)
        print("Copy: {} -> {}".format(filepath, self.tmpdir))

    def copy_files(self, filename):

        # Expand filename by expanding wildcards e.g. 'dir/*', the
        # glob returns a list of files
        files = glob.glob(filename)

        for f in files:
            self.copy_file(f)


    def run(self, *args):
        """Runs the command in the test directory

        :param args: List of arguments

        :return: A RunResult object representing the result of the command
        """

        start_time = time.time()

        popen = subprocess.Popen(args,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    # Need to decode the stdout and stderr with the correct
                    # character encoding (http://stackoverflow.com/a/28996987)
                    universal_newlines=True,
                    cwd=str(self.tmpdir))

        stdout, stderr = popen.communicate()

        end_time = time.time()

        return RunResult(' '.join(args),
            stdout, stderr, popen.returncode, end_time - start_time)

@pytest.fixture
def testdir(request, tmpdir):
    return TestDir(request, tmpdir)

def test_copy_file(testdir):
    testdir.copy_files('test/prog1/*')
    testdir.copy_file('build/*/waf')
    r = testdir.run('python','waf','configure')

    assert r.returncode == 0
    assert r.stdout.match('*finished successfully*')

    r = testdir.run('python', 'waf', 'build')

    assert r.returncode == 0

    print(str(r))
