from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting
from plone.app.testing import applyProfile

from zope.configuration import xmlconfig

class CollectiveAssets(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        # Load ZCML for dependend packages
        import plone.resource
        xmlconfig.file('configure.zcml',
                       plone.resource,
                       context=configurationContext)

        # Load ZCML for this package
        import collective.assets
        xmlconfig.file('configure.zcml',
                       collective.assets,
                       context=configurationContext)


    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.assets:default')

COLLECTIVE_ASSETS_FIXTURE = CollectiveAssets()
COLLECTIVE_ASSETS_INTEGRATION_TESTING = \
    IntegrationTesting(bases=(COLLECTIVE_ASSETS_FIXTURE, ),
                       name="CollectiveAssets:Integration")
