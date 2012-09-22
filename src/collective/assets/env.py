from os.path import join

from zope.interface import implements
from zope.component import getUtility
from plone.resource.interfaces import IResourceDirectory

from webassets import Environment

from .interfaces import IWebAssetsEnvironment

class PloneEnvironment(Environment):

    implements(IWebAssetsEnvironment)

    def __init__(self):
        # get global resource path from plone.resource configuration
        plone_resource = getUtility(IResourceDirectory, name=u'')
        resource_path = join(plone_resource.directory, 'theme', 'rr')
        super(PloneEnvironment, self).__init__(resource_path, '/++theme++rr')

