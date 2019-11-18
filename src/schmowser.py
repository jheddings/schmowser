# schmowser - a.k.a browser-shmowser

import os

import logging
import logging.config

################################################################################
class Schmowser():

    #---------------------------------------------------------------------------
    def __init__(self):
        self.logger = logging.getLogger('schmowser')

        self.apps = { }
        self.handlers = { }

        self.default_app_name = None
        self.dry_run = False

    #---------------------------------------------------------------------------
    def add_app(self, app_name, app_path):
        self.logger.debug('adding app: %s = %s', app_name, app_path)

        if not os.path.exists(app_path):
            self.logger.warning('invalid app path: %s', app_path)
            return False

        old_path = self.apps.pop(app_name, None)
        if old_path is not None:
            self.logger.debug('overriding previous app: %s', old_path)

        self.apps[app_name] = app_path

    #---------------------------------------------------------------------------
    def add_handler(self, expr, app_name):
        self.logger.debug('adding handler: %s = %s', expr, app_name)

        if app_name not in self.apps:
            self.logger.error('invalid app name: %s', app_name)
            return False

        old_name = self.handlers.pop(expr, None)
        if old_name is not None:
            self.logger.debug('overriding previous handler: %s', old_name)

        self.handlers[expr] = app_name

    #---------------------------------------------------------------------------
    # find the app for a given input parameter
    def get_app_name(self, param):
        import re

        self.logger.debug('retrieving app for: %s', param)

        app_name = None

        # look through each handler to find a match
        for expr,name in self.handlers.items():
            self.logger.debug('-- checking: %s', expr)
            m = re.match(expr, param)

            # XXX should we stop on a match or let the last one win?
            if m is not None:
                app_name = name
                self.logger.debug('-- match FOUND: %s', app_name)
                break

        # if nothing matched, use the default
        if app_name is None:
            app_name = self.default_app_name
            self.logger.debug('-- match NOT FOUND, using default: %s', app_name)

        return app_name

    #---------------------------------------------------------------------------
    # load the path to a given app
    def get_app_path(self, app_name):
        self.logger.debug('get path to app: %s', app_name)
        app_path = self.apps.get(app_name, None)

        if app_path is None:
            self.logger.error('no path for app: %s', app_name)
        else:
            self.logger.debug('application path: %s', app_path)

        return app_path

    #---------------------------------------------------------------------------
    def route(self, param):
        self.logger.debug('processing input parameter: %s', param)

        app_name = self.get_app_name(param)

        self._launch(app_name, param)

    ################################################################################
    # launch the given application
    def _launch(self, app_name, *argv):
        import subprocess

        self.logger.info('Launching App: %s -- %s', app_name, ','.join(argv))

        app_path = self.get_app_path(app_name)
        if app_path is None:
            self.logger.error('invalid app: %s', app_name)
            return False

        # TODO use shlex.quote on path and argv

        # launch the correct application for the parameter
        if self.dry_run is False:
            # XXX should we care if the open call fails?  e.g. a bad app path
            self.logger.debug('starting application process')
            subprocess.call(['open', '-a', app_path, *argv])

        return True

################################################################################
def parse_args():
    import argparse

    argp = argparse.ArgumentParser(description='schmowser: an app routing utility')

    # TODO correct the default config path...
    argp.add_argument('--config', default='.schmowserc',
                      help='configuration file (default: ~/.schmowserc)')

    argp.add_argument('--debug', default=False, action='store_true',
                      help='enable debugging mode (default: False)')

    argp.add_argument('params', nargs=argparse.REMAINDER)

    return argp.parse_args()

################################################################################
def load_config(args):
    import yaml

    with open(args.config) as config_file:
        conf = yaml.load(config_file, Loader=yaml.CLoader)

    # TODO error checking on config file structure

    # configure logging and setup debug options
    if args.debug is True:
        logging.basicConfig(level=logging.DEBUG)

    elif 'Logging' in conf:
        logging.config.dictConfig(conf['Logging'])

    logging.debug('config file loaded: %s', args.config)

    return conf

################################################################################
def configure_app(app, conf):
    logging.debug('loading user configuration')

    for app_name,app_path in conf['Applications'].items():
        app.add_app(app_name, app_path)

    for path_expr,app_name in conf['Handlers'].items():
        app.add_handler(path_expr, app_name)

    options = conf['Options']

    app.default_app_name = options.get('DefaultApp', None)
    logging.debug('[conf] default app: %s', app.default_app_name)

    app.dry_run = options.get('DryRun', False)
    logging.debug('[conf] dry run: %s', app.dry_run)

################################################################################
def main():
    args = parse_args()
    conf = load_config(args)

    app = Schmowser()
    configure_app(app, conf)

    for param in args.params:
        app.route(param)

################################################################################
## MAIN ENTRY

if __name__ == '__main__':
    main()

