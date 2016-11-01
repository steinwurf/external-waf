#!/usr/bin/env python
# encoding: utf-8

"""
WurfOptions overrides waf's default OptionsContext if it is imported in the
top-level wscript of a project like this:

    import waflib.extras.wurf_options

This step can be done automatically by building a custom waf binary and
using the --prelude statement (see more here http://bit.ly/1Te4mRz).

The tool overrides the 'parse_args' function to allow the definition of
options in dependencies. The passed options are parsed twice. The first time
all options are allowed as it is not possible to validate options that are not
yet defined. The second parsing will happen after the dependencies are fully
resolved, and therefore all options are known.

The dependencies are resolved with the "resolve" context, which is created
and executed in parse_args. This is a simplified version of the configuration
context, and it follows the standard control flow. First, it will call the
"resolve" function in the top-level wscript of the project. In that function,
we load "wurf_common_tools" which in turn loads "wurf_dependency_bundle",
"wurf_dependency_resolve" and "wurf_git". These tools are used to download
the dependencies.

The project's top-level dependencies are defined in the wscript's "resolve"
function like this (after loading "wurf_common_tools"):

def resolve(ctx):
    import waflib.extras.wurf_dependency_resolve as resolve

    ctx.load('wurf_common_tools')

    ctx.add_dependency(resolve.ResolveVersion(
        name='waf-tools',
        git_repository='github.com/steinwurf/waf-tools.git',
        major=2))

When a dependency is added, wurf_dependency_bundle tries to resolve the
project. This only happens if this is an active resolve step, i.e. if
"configure" is given in the waf commands. In a passive resolve step, the
tool only enumerates the  previously resolved dependencies to fetch the
options from these.

After downloading/resolving a dependency, we also recurse into the wscript
of that dependency where the "resolve" function adds the dependencies of
that project. These dependencies are resolved immediately in a recursive way.
A dependency can also define options in the "resolve" function by accessing
the original option parser using "ctx.opt":

def resolve(ctx):
    opts = ctx.opt.add_option_group('Makespec options')
    opts.add_option('--cxx_mkspec', default=None, dest='cxx_mkspec',
                    help="C++ make specification")
"""


import os
import sys
import copy

from waflib import Context
from waflib import Options

import wurf_resolve_context

class WurfOptionsContext(Options.OptionsContext):

    def execute(self):

        # Create and execute the resolve context
        ctx = Context.create_context('resolve', opt=self)
        ctx.cmd = 'resolve'

        try:
            ctx.execute()
        finally:
            ctx.finalize()

        # Call options in all dependencies
        wurf_resolve_context.recurse_dependencies(self)

        # Now invoke execute to recurse in to the option(...) function of
        # the wscript (if it is defined)
        #
        # This will also call parse_args(...) so we need to have recursed
        # the dependencies options(...) functions first.
        print("BLABAL 1")

        # Using the %default placeholder:
        #    http://stackoverflow.com/a/1254491/1717320
        self.add_option('--bundle-path', default='bundle_dependencies',
            dest='bundle_path',
            help='The folder where the bundled dependencies are downloaded.'
                 '[default: %default]')

        # Fetch the arguments not parsed in the resolve step
        self.waf_options = ctx.waf_options
        
        super(WurfOptionsContext, self).execute()



    def parse_args(self, _args=None):
        """ Override the parse_args(..) from the OptionsContext.

        Here we inject the arguments which were not consumed in the resolve step
        """
        super(WurfOptionsContext, self).parse_args(self.waf_options)

    def add_option(self, *k, **kw):

        print(k)
        super(WurfOptionsContext, self).add_option(*k, **kw)
