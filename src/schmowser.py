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
argp = argparse.ArgumentParser(description='schmowser: an app routing utility')

# TODO correct the default config path...
argp.add_argument('--config', default='.schmowserc',
                  help='configuration file (default: ~/.schmowserc)')

argp.add_argument('--debug', default=False, action='store_true',
                  help='enable debugging mode (default: False)')

argp.add_argument('params', nargs=argparse.REMAINDER)

args = argp.parse_args()
gconf = { }

#-------------------------------------------------------------------------------
# load user configuration options
with open(args.config) as config_file:
    gconf = yaml.load(config_file, Loader=yaml.CLoader)

# TODO error checking on config file structure

# load configuration options
options = gconf['Options']

# configure logging and setup debug options
if args.debug is True:
    logging.basicConfig(level=logging.DEBUG)

elif 'Logging' in gconf:
    logging.config.dictConfig(gconf['Logging'])

default_app = options['DefaultApp']
logging.debug('[conf] default app: %s', default_app)

logging.debug('[conf] config file loaded: %s', args.config)

################################################################################
# launch the given application
def launch(app, *argv):
    logging.info('Launching App: %s -- %s', app, ','.join(argv))

    # global applications
    apps = gconf['Applications']

    if app not in apps:
        logging.error('invalid app: %s', app)
        return False

    # load the correct app
    app_path = apps[app]
    logging.debug('-- application path: %s', app_path)

    # TODO add DryRun option to global config

    # launch the correct application for the parameter
    if args.debug is False:
        # XXX should we care if the open call fails?  e.g. a bad app path
        subprocess.call(['open', '-a', app_path, *argv])

    return True

################################################################################
# find the app for a given input parameter
def get_app(app, *argv):
    app = None

    # load global handlers
    handlers = gconf['Handlers']

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

    return app

################################################################################
## MAIN ENTRY

# process each of the parameters
for param in args.params:
    logging.debug('processing input parameter: %s', param)

    app = get_app(param)

    launch(app, param)
