from tempfile import mkdtemp
import transaction
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting
from plone.app.testing import applyProfile

from zope.configuration import xmlconfig

from plone.resource.interfaces import IResourceDirectory
from plone.resource.directory import FilesystemResourceDirectory
from zope.component import getGlobalSiteManager

class CollectiveAssets(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        # Load ZCML for this package
        import collective.assets
        resources_dir = mkdtemp()
        directory = FilesystemResourceDirectory(resources_dir, u'')
        gsm = getGlobalSiteManager()
        gsm.registerUtility(directory,
                            IResourceDirectory,
                            name=u'')
        xmlconfig.file('configure.zcml',
                       collective.assets,
                       context=configurationContext)


    def setUpPloneSite(self, portal):
        applyProfile(portal, 'plone.resource:default')
        applyProfile(portal, 'collective.assets:testing')
        applyProfile(portal, 'collective.assets:default')

COLLECTIVE_ASSETS_FIXTURE = CollectiveAssets()
COLLECTIVE_ASSETS_INTEGRATION_TESTING = \
    IntegrationTesting(bases=(COLLECTIVE_ASSETS_FIXTURE, ),
                       name="CollectiveAssets:Integration")
