#! /usr/bin/env python
# encoding: utf-8

import os
import json

from .error import DependencyError

class OnPassiveLoadPathResolver(object):

    def __init__(self, dependency, bundle_config_path):
        """ Construct an instance.

        :param dependency: A Dependency instance.
        :param bundle_config_path: A string containing the path to where the
            dependencies config json files should be / is stored.
        """
        self.dependency = dependency
        self.bundle_config_path = bundle_config_path

    def resolve(self):
        """ Resolve a path to a dependency.

        If we are doing an "passive" resolver, meaning that waf was not invoked
        with configure. Then we load the resolved path to the file-system.
        Otherwise we raise an exception.

        :return: The path as a string.
        """

        config = self.__read_config()

        if self.dependency.sha1 != config['sha1']:
            raise DependencyError('Failed sha1 check', self.dependency)

        if config['is_symlink']:
            self.dependency.is_symlink = config['is_symlink']
            self.dependency.real_path = str(config['real_path'])

        path = str(config['path'])

        if not os.path.isdir(path):
            raise DependencyErrors('Not valid path {}'.format(path),
                self.dependency)

        return path

    def __read_config(self):
        """ Read the dependency config from file
        """

        config_path = os.path.join(
            self.bundle_config_path, self.dependency.name + '.resolve.json')

        if not os.path.isfile(config_path):
            raise DependencyError('No config - re-run configure',
                self.dependency)

        with open(config_path, 'r') as config_file:
            return json.load(config_file)
