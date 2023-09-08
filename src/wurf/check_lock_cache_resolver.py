#! /usr/bin/env python
# encoding: utf-8

from .error import DependencyError


class CheckLockCacheResolver(object):
    """Iterates through a list of resolvers until a path is resolved."""

    def __init__(self, resolver, lock_cache, dependency):
        """Construct an instance.

        :param resolvers: A list of resolvers object for the available
           sources
        :param lock_cache: A dict containing the lock cache information
        :param dependency: A Dependency instance.
        """
        self.resolver = resolver
        self.lock_cache = lock_cache
        self.dependency = dependency

    def resolve(self):
        """Resolve the dependency.

        :return: Path to resolved dependency as a string
        """

        if self.dependency not in self.lock_cache:
            raise DependencyError(
                msg=f"Not found in lock cache: {self.lock_cache}",
                dependency=self.dependency,
            )

        if self.lock_cache.check_sha1(dependency=self.dependency):
            raise DependencyError(
                msg=(
                    "Locked dependency inconsistent with the "
                    "dependency specified in the project."
                ),
                dependency=self.dependency,
            )

        path = self.resolver.resolve()
        if self.lock_cache.check_content(dependency=self.dependency):
            raise DependencyError(
                msg=(
                    "The content does not match the data "
                    "when the dependency was locked."
                ),
                dependency=self.dependency,
            )
        return path
