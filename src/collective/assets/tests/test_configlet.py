import os.path
import unittest2 as unittest

import zope.component
from Products.CMFCore.utils import getToolByName
  
from collective.assets.testing import\
    COLLECTIVE_ASSETS_INTEGRATION_TESTING

from collective.assets.interfaces import IAssetsSchema, IAssetsConfig


class TestConfiglet(unittest.TestCase):

    layer = COLLECTIVE_ASSETS_INTEGRATION_TESTING
    
    def setUp(self):
        self.portal = self.layer['portal']
        self.schema = IAssetsSchema(self.portal)
        self.util = zope.component.queryUtility(IAssetsConfig)
    
    def test_active_on(self):
        self.schema.setActive(True)
        self.assertTrue(self.util.active)
        self.assertTrue(self.schema.getActive())
        
    def test_active_off(self):
        self.schema.setActive(False)
        self.assertFalse(self.util.active)
        self.assertFalse(self.schema.getActive())
        
