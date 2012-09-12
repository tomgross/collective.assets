from os.path import join
from zope.interface import Interface, directlyProvides
import zope.component

from webassets import Environment
from plone.resource.interfaces import IResourceDirectory

from .interfaces import IWebAssetsEnvironment


def get_webassets_environment():
    # get global resource path from plone.resource configuration
    plone_resource = zope.component.queryUtility(IResourceDirectory, name=u'')
    resource_path = join(plone_resource.directory, 'theme', 'rr')

    # define asset environment
    return Environment(resource_path, '/++theme++rr')

directlyProvides(get_webassets_environment, IWebAssetsEnvironment)
