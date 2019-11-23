import unittest
import logging

import schmowser

# keep logging output to a minumim for testing
logging.basicConfig(level=logging.ERROR)

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

