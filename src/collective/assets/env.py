from persistent.dict import PersistentDict
from os.path import join

from zope.interface import implements
from zope.component import getUtility
from zope.component.hooks import getSite
from zope.annotation.interfaces import IAnnotations
from plone.resource.interfaces import IResourceDirectory

from webassets.env import DictConfigStorage, Environment, ConfigStorage

from .interfaces import IWebAssetsEnvironment

ASSETS_SETTING_KEY = 'collective.assets.env'

class PersistentDictConfigStorage(DictConfigStorage):

    def __init__(self, *a, **kw):
        self._dict = PersistentDict() 
        ConfigStorage.__init__(self, *a, **kw)

    def getDict(self):
        site = getSite()
        if site is not None:
            ann = IAnnotations(site)
            if ASSETS_SETTING_KEY not in ann:
                ann[ASSETS_SETTING_KEY] = self._dict
            return ann[ASSETS_SETTING_KEY]
        return self._dict

    def __getitem__(self, key):
        key = key.lower()
        value = self._get_deprecated(key)
        if not value is None:
            return value
        self._dict = self.getDict()
        return self._dict.__getitem__(key)

    def __setitem__(self, key, value):
        key = key.lower()
        if not self._set_deprecated(key, value):
            self._dict = self.getDict()
            self._dict.__setitem__(key, value)
            self._dict._p_changed = True

class PloneEnvironment(Environment):

    implements(IWebAssetsEnvironment)

    config_storage_class = PersistentDictConfigStorage

    def __init__(self):
        # get global resource path from plone.resource configuration
        plone_resource = getUtility(IResourceDirectory, name=u'')
        resource_path = join(plone_resource.directory, 'theme', 'rr')
        super(PloneEnvironment, self).__init__(resource_path, '/++theme++rr')
        self.config.setdefault('active', False)

    def clear(self):
        self._named_bundles = {}
        self._anon_bundles = []

