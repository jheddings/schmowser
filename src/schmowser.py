#!/usr/bin/env python2.7

import yaml
import argparse

import logging
import logging.config

import re
import subprocess
import shlex

#-------------------------------------------------------------------------------
# read command line options
argp = argparse.ArgumentParser(description='schmowser: a link routing utility')

# TODO correct the default config path...
argp.add_argument('-f', '--config', default='.schmowserc',
                  help='configuration file (default: ~/.schmowserc)')

argp.add_argument('params', nargs=argparse.REMAINDER)

args = argp.parse_args()
conf = { }

#-------------------------------------------------------------------------------
# load user configuration options
with open(args.config) as config_file:
    conf = yaml.load(config_file, Loader=yaml.CLoader)

# configure logging first - used by other config options
# TODO turn off output if no logging config
conf_logging = conf['Logging']
logging.config.dictConfig(conf_logging)

logging.debug('[conf] config file loaded: %s', args.config)

# load configuration options
options = conf['Options']

default_app = options['DefaultApp']
logging.debug('[conf] default app: %s', default_app)

# load applications
apps = conf['Applications']
handlers = conf['Handlers']

################################################################################
## MAIN ENTRY

# process each of the parameters
for param in args.params:
    logging.debug('processing input parameter: %s', param)

    app = None

    # look through each handler to find a match
    for handler in handlers:
        logging.debug('-- match: %s', handler)
        m = re.match(handler, param)

        if m is not None:
            app = handlers[handler]
            logging.debug('-- match FOUND: %s', app)

    # if nothing matched, use the default
    if app is None:
        app = default_app
        logging.debug('-- match NOT FOUND, using default: %s', app)

    # load the correct app
    app_path = apps[app]
    logging.debug('-- using app: %s', app_path)

    # launch the correct application for the parameter
    subprocess.call(['open', param, '-a', app_path])

