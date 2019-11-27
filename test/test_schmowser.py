import unittest
import logging

import schmowser

# keep logging output to a minumim for testing
logging.basicConfig(level=logging.CRITICAL)

################################################################################
class SchmowserObjectTest(unittest.TestCase):

    #---------------------------------------------------------------------------
    def test_EmptyAppsDefaultName(self):
        app = schmowser.Schmowser(discover_apps=False)
        app_name = app.get_app_name('http://www.foo.com/')
        self.assertIsNone(app_name)

    #---------------------------------------------------------------------------
    def test_DiscoverAppsDefaultName(self):
        app = schmowser.Schmowser()
        app_name = app.get_app_name('http://www.foo.com/')
        self.assertIsNotNone(app_name)

    #---------------------------------------------------------------------------
    def test_BasicAppMatch(self):
        app = schmowser.Schmowser(discover_apps=False)
        app.add_app('Foo', '/usr/bin/true')
        app.add_handler('^http://.*foo.*$', 'Foo')

        good_name = app.get_app_name('http://www.foo.com/')
        self.assertEqual(good_name, 'Foo')

        bad_name = app.get_app_name('http://www.bar.com/')
        self.assertNotEqual(bad_name, 'Foo')

    #---------------------------------------------------------------------------
    def test_OverrideAppPath(self):
        app = schmowser.Schmowser(discover_apps=False)

        ret = app.add_app('MyApp', '/Applications/Safari.app')
        self.assertTrue(ret)

        ret = app.add_app('MyApp', '/Applications/Safari.app')
        self.assertTrue(ret)

    #---------------------------------------------------------------------------
    def test_BadAppPath(self):
        app = schmowser.Schmowser(discover_apps=False)
        ret = app.add_app('Foo', '/tmp/bad_file_name.app')
        self.assertFalse(ret)

    #---------------------------------------------------------------------------
    def test_BadAppName(self):
        app = schmowser.Schmowser(discover_apps=False)

        # make sure we can add Safari properly...
        ret = app.add_app('Safari', '/Applications/Safari.app')
        self.assertTrue(ret)

        # now try to use a bad appname
        ret = app.add_app(None, '/Applications/Safari.app')
        self.assertFalse(ret)

    #---------------------------------------------------------------------------
    def test_NoSuchAppForHandler(self):
        app = schmowser.Schmowser(discover_apps=False)
        ret = app.add_handler('*', 'NoSuchApp')
        self.assertFalse(ret)

