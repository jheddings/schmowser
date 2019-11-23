import unittest
import logging
import os

import schmowser

# keep logging output to a minumim for testing
logging.basicConfig(level=logging.ERROR)

################################################################################
class AppInfoObjectTests(unittest.TestCase):

    #---------------------------------------------------------------------------
    def setUp(self):
        local_dir = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(local_dir, 'TestInfo.plist')
        self.test_info = schmowser.AppInfo.load(filename)

    #---------------------------------------------------------------------------
    def test_EmptyInfo(self):
        empty_info = schmowser.AppInfo()
        app_name = empty_info.get_name()
        self.assertIsNone(app_name)

    #---------------------------------------------------------------------------
    def test_LocalAppInfo(self):
        app_name = self.test_info.get_name()
        self.assertIsNotNone(app_name)
