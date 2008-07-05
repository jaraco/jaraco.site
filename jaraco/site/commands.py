# -*- coding: utf-8 -*-
"""This module contains functions called from console script entry points."""

import os
import sys

from os.path import dirname, exists, join

import pkg_resources
pkg_resources.require("TurboGears")

import cherrypy
import turbogears

cherrypy.lowercase_api = True

class ConfigurationError(Exception):
    pass

def start():
    """Start the CherryPy application server."""

    web_dir = dirname(__file__)
    jaraco_dir = dirname(web_dir)
    setupdir = dirname(jaraco_dir)
    curdir = os.getcwd()

    # First look on the command line for a desired config file,
    # if it's not on the command line, then look for 'setup.py'
    # in the current directory. If there, load configuration
    # from a file called 'dev.cfg'. If it's not there, the project
    # is probably installed and we'll look first for a file called
    # 'prod.cfg' in the current directory and then for a default
    # config file called 'default.cfg' packaged in the egg.
    if len(sys.argv) > 1:
        configfile = sys.argv[1]
    elif exists(join(setupdir, "setup.py")):
        configfile = join(setupdir, "dev.cfg")
    elif exists(join(curdir, "prod.cfg")):
        configfile = join(curdir, "prod.cfg")
    else:
        try:
            configfile = pkg_resources.resource_filename(
              pkg_resources.Requirement.parse("jaraco.site"),
                "config/default.cfg")
        except pkg_resources.DistributionNotFound:
            raise ConfigurationError("Could not find default configuration.")

    turbogears.update_config(configfile=configfile,
        modulename="jaraco.site.config")

    from jaraco.site.controllers import Root

    turbogears.start_server(Root())
