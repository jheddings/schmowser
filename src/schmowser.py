# schmowser - a.k.a browser-shmowser

import os

import logging
import logging.config

################################################################################
class Schmowser():

    #---------------------------------------------------------------------------
    def __init__(self, discover_apps=True):
        self.logger = logging.getLogger('schmowser')
        self.logger.debug('initializing')

        self.apps = { }
        self.handlers = { }

        self.default_app_name = None
        self.dry_run = False

        if discover_apps is True:
            self._discover_apps()

    #---------------------------------------------------------------------------
    def add_app(self, app_name, app_path):
        self.logger.debug('adding app: %s => %s', app_name, app_path)

        # XXX should this raise an exception instead?
        if app_name is None:
            self.logger.warning('invalid app name: %s', app_name)
            return False

        # XXX should this raise an exception instead?
        if not os.path.exists(app_path):
            self.logger.warning('invalid app path: %s', app_path)
            return False

        old_path = self.apps.pop(app_name, None)
        if old_path is not None:
            self.logger.debug('overriding previous app: %s', old_path)

        self.apps[app_name] = app_path

        return True

    #---------------------------------------------------------------------------
    def add_handler(self, expr, app_name):
        self.logger.debug('registering handler: %s = %s', expr, app_name)

        # XXX should this raise an exception instead?
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
    def open(self, param):
        self.logger.debug('processing input parameter: %s', param)

        app_name = self.get_app_name(param)

        return self._run_app(app_name, param)

    #---------------------------------------------------------------------------
    def _discover_apps(self):
        import glob

        # NOTE we only load the main Applications automatically...  apps stored
        # in sub folders (like Utilities) will need to be added by the user

        self.logger.debug('loading system apps')
        for app_dir in glob.glob('/Applications/*.app'):
            self._add_app_from_path(app_dir)

        self.logger.debug('loading user apps')
        user_dir = os.path.expanduser('~/Applications')
        for app_dir in glob.glob(user_dir + '/*.app'):
            self._add_app_from_path(app_dir)

        self._choose_default_app()

    #---------------------------------------------------------------------------
    def _add_app_from_path(self, app_dir):
        self.logger.debug('loading app: %s', app_dir)

        info_path = os.path.join(app_dir, 'Contents/Info.plist')

        if not os.path.exists(info_path):
            self.logger.warn('app info not found: %s', info_path)
            return None

        self.logger.debug('reading app info: %s', info_path)
        app_info = AppInfo.load(info_path)
        app_name = app_info.get_name()

        if app_name is not None:
            self.add_app(app_name, app_dir)

        return app_name

    #---------------------------------------------------------------------------
    def _choose_default_app(self):
        # XXX is there a better way to pick the default? something more dynamic?

        if 'Safari' in self.apps:
            self.default_app_name = 'Safari'
        elif 'Chrome' in self.apps:
            self.default_app_name = 'Chrome'
        elif 'Firefox' in self.apps:
            self.default_app_name = 'Firefox'
        elif 'Opera' in self.apps:
            self.default_app_name = 'Opera'
        else:
            self.default_app_name = None
            self.logger.warning('Could not initialize default app')

        self.logger.debug('initialized default app: %s', self.default_app_name)

    #---------------------------------------------------------------------------
    # run the given application with specified args
    def _run_app(self, app_name, *argv):
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
class AppInfo():

    #---------------------------------------------------------------------------
    def __init__(self, info=None):
        self.logger = logging.getLogger('appinfo')

        if info is None:
            self.logger.debug('initializing empty info')
            self.info = dict()
        else:
            self.logger.debug('initializing user info')
            self.info = info

    #---------------------------------------------------------------------------
    def get(self, key):
        self.logger.debug('searching for key: %s', key)

        val = self.info.get(key, None)

        return val

    #---------------------------------------------------------------------------
    def get_name(self):
        return self.get('CFBundleName')

    #---------------------------------------------------------------------------
    def get_version(self):
        return self.get('CFBundleVersion')

    #---------------------------------------------------------------------------
    def load(path):
        import plistlib

        with open(path, 'rb') as plist_file:
            info = plistlib.load(plist_file)

        return AppInfo(info=info)

################################################################################
def parse_args():
    import argparse

    argp = argparse.ArgumentParser(description='schmowser: an app routing utility')

    default_conf = os.path.expanduser('~/.schmowserc')
    argp.add_argument('--config', default=default_conf,
                      help='configuration file (default: ~/.schmowserc)')

    argp.add_argument('params', nargs=argparse.REMAINDER)

    return argp.parse_args()

################################################################################
def load_config(args):
    import yaml

    if not os.path.exists(args.config):
        logging.warning('config file does not exist: %s', args.config)
        return None

    with open(args.config, 'r') as config_file:
        conf = yaml.load(config_file, Loader=yaml.CLoader)

    # TODO error checking on config file structure

    if 'Logging' in conf:
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

    logging.debug('== initializing main application ==')

    app = Schmowser()

    if conf is not None:
        configure_app(app, conf)

    for param in args.params:
        app.open(param)

################################################################################
## MAIN ENTRY

if __name__ == '__main__':
    main()

