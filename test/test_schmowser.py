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

