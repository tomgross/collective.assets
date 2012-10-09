import os.path
import unittest2 as unittest

import zope.component
from Products.CMFCore.utils import getToolByName
  
from collective.assets.testing import\
    COLLECTIVE_ASSETS_INTEGRATION_TESTING


class TestConfiglet(unittest.TestCase):

    layer = COLLECTIVE_ASSETS_INTEGRATION_TESTING
    
    def setUp(self):
        self.portal = self.layer['portal']
    
    def test_active_on(self):
        assert True
        
