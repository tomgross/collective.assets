import os.path
import unittest2 as unittest

import zope.component
from Products.CMFCore.utils import getToolByName
  
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import login
from plone.app.testing import setRoles

from collective.assets.testing import\
    COLLECTIVE_ASSETS_INTEGRATION_TESTING

from collective.assets.interfaces import IWebAssetsEnvironment, IAssetsConfig
from collective.assets.browser import check
from webassets import Environment
from webassets.bundle import Bundle

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
        self.assertTrue(isinstance(env, Environment))

class TestHelperMethods(unittest.TestCase):

    layer = COLLECTIVE_ASSETS_INTEGRATION_TESTING
    data_attrs = ('oid', 'filters', 'suffix')

    def setUp(self):
        self.portal = self.layer['portal']

    def test_check(self):
        bundle = Bundle()
        self.assertTrue(check(bundle, self.portal))

    def test_js_data(self):
        from collective.assets.browser import JS
        for attr in self.data_attrs:
            self.assertTrue(hasattr(JS, attr))

    def test_css_data(self):
        from collective.assets.browser import CSS
        for attr in self.data_attrs:
            self.assertTrue(hasattr(CSS, attr))

class TestViews(unittest.TestCase):

    layer = COLLECTIVE_ASSETS_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self._set_active(False)
        self._add_dummy_resources()

    def _set_active(self, active):
        util = zope.component.queryUtility(IAssetsConfig)
        util.active = active

    def _add_dummy_resources(self):
        datadir = os.path.join(os.path.dirname(__file__), 'data')
        for css in ['authenticated.css',
                    'printmedia.css',
                    'withexpression.css']:
            setRoles(self.portal, TEST_USER_ID, ['Manager'])
            login(self.portal, TEST_USER_NAME)
            self.portal.invokeFactory('File', id=css)
            setRoles(self.portal, TEST_USER_ID, ['Member'])
            with open(os.path.join(datadir, css)) as f:
                self.portal[css].setFile(f.read())

    def test_scripts_view(self):
        from collective.assets.browser import ScriptsView
        scriptsview = ScriptsView(self.portal, self.request)
        # Standard JS view of javascript_tool as fallback
        scripts = scriptsview.scripts()
        self.assertTrue(scripts[0]['src'].startswith('http://nohost/plone/portal_javascripts/'))
        self._set_active(True)
        scripts = scriptsview.scripts()
        # No bundles registered
        self.assertEqual(scripts, [])

    def test_styles_view(self):
        from collective.assets.browser import StylesView
        stylesview = StylesView(self.portal, self.request)
        styles = stylesview.styles()
        self.assertTrue(styles[0]['src'].startswith('http://nohost/plone/portal_css/'))
        self._set_active(True)
        styles = stylesview.styles()
        # No bundles registered
        self.assertEqual(styles, [])

    def test_generate(self):
        print [x.getId() for x in self.portal.portal_css.resources]
        pass
