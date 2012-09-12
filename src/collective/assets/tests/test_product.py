import unittest2 as unittest

import zope.component
from Products.CMFCore.utils import getToolByName

from collective.assets.testing import\
    COLLECTIVE_ASSETS_INTEGRATION_TESTING

from collective.assets.interfaces import IWebAssetsEnvironment

class TestProduct(unittest.TestCase):

    layer = COLLECTIVE_ASSETS_INTEGRATION_TESTING
    
    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.qi_tool = getToolByName(self.portal, 'portal_quickinstaller')
    
    def test_product_is_installed(self):
        """ Validate that our products GS profile has been run and the product 
            installed
        """
        pid = 'collective.assets'
        installed = [p['id'] for p in self.qi_tool.listInstalledProducts()]
        self.assertTrue(pid in installed,
                        'package appears not to have been installed')

    def test_environment(self):
        env = zope.component.getUtility(IWebAssetsEnvironment)
        print env()
