import os
import mock

from wurf.git_resolver import GitResolver


def test_git_resolver(testdirectory):
    ctx = mock.Mock()
    git = mock.Mock()
    url = "https://gitlab.com/steinwurf/links.git"

    git_url_rewriter = mock.Mock()
    git_url_rewriter.rewrite_url.return_value = url

    cwd = testdirectory.path()

    # GitResolver checks that the directory is created during git.clone,
    # so we create it within the testdirectory as a side effect
    def fake_git_clone(repository, directory, cwd):
        os.makedirs(os.path.join(cwd, directory))

    git.clone = mock.Mock(side_effect=fake_git_clone)

    dependency = mock.Mock()
    dependency.name = "links"
    dependency.source = "gitlab.com/steinwurf/links.git"

    resolver = GitResolver(
        git=git,
        ctx=ctx,
        dependency=dependency,
        git_url_rewriter=git_url_rewriter,
        cwd=cwd,
    )

    path = resolver.resolve()

    repo_name = os.path.basename(os.path.normpath(path))
    assert repo_name.startswith("master-")
    repo_folder = os.path.dirname(os.path.normpath(path))

    git.clone.assert_called_once_with(
        repository=url, directory=repo_name, cwd=repo_folder
    )

    git.pull_submodules.assert_called_once_with(cwd=path)

    # Reset the git mock
    git.reset_mock()

    # The destination folder is already created, so the next resolve
    # should just run git pull
    path2 = resolver.resolve()

    assert path2 == path

    assert git.clone.called is False
    git.pull.assert_called_once_with(cwd=path)
    git.pull_submodules.assert_called_once_with(cwd=path)

    # Reset the git mock
    git.reset_mock()

    # Make sure we don't pull submodules if this attribute is specified
    dependency.pull_submodules = False

    path2 = resolver.resolve()

    assert path2 == path

    assert git.clone.called is False
    git.pull.assert_called_once_with(cwd=path)
    assert not git.pull_submodules.called
