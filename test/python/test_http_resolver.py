import mock
import os

from wurf.http_resolver import HttpResolver


def test_http_resolver(testdirectory):
    url_download = mock.Mock()
    dependency = mock.Mock()
    dependency.filename = None
    dependency.source = "http://example.com/file.zip"
    cwd = testdirectory.path()

    def create_file(cwd, source, filename):
        assert dependency.source == source
        assert filename is None

        httpdir = testdirectory.from_path(cwd)
        httpdir.write_binary("file.zip", b"hello_world")

        return os.path.join(httpdir.path(), "file.zip")

    url_download.download.side_effect = create_file

    resolver = HttpResolver(url_download=url_download, dependency=dependency, cwd=cwd)

    path = resolver.resolve()
    assert os.path.isfile(path)

    assert testdirectory.contains_file("download/file.zip")


def test_http_resolver_filename(testdirectory):
    url_download = mock.Mock()
    dependency = mock.Mock()
    dependency.filename = "foo.zip"

    dependency.source = "http://example.com/file.zip"
    cwd = testdirectory.path()

    def create_file(cwd, source, filename):
        assert dependency.source == source
        assert filename == "foo.zip"

        httpdir = testdirectory.from_path(cwd)
        httpdir.write_binary("foo.zip", b"hello_world")

        return os.path.join(httpdir.path(), "foo.zip")

    url_download.download.side_effect = create_file

    resolver = HttpResolver(url_download=url_download, dependency=dependency, cwd=cwd)

    path = resolver.resolve()
    assert os.path.isfile(path)

    assert testdirectory.contains_file("download/foo.zip")
