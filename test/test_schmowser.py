import unittest
import logging

import schmowser

# keep logging output to a minumim for testing
logging.basicConfig(level=logging.ERROR)

################################################################################
class SchmowserObjectTest(unittest.TestCase):

    #---------------------------------------------------------------------------
    def test_DefaultAppName(self):
        app = schmowser.Schmowser()
        self.assertIsNotNone(app.default_app_name)

    #---------------------------------------------------------------------------
    def test_BasicAppMatch(self):
        app = schmowser.Schmowser()
        app.add_app('Foo', '/usr/bin/true')
        app.add_handler('^http://.*foo.*$', 'Foo')

        good_name = app.get_app_name('http://www.foo.com/')
        self.assertEqual(good_name, 'Foo')

        bad_name = app.get_app_name('http://www.bar.com/')
        self.assertNotEqual(bad_name, 'Foo')

