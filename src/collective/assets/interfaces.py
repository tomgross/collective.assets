from zope.interface import Interface
from zope.schema import Bool, List, Choice, TextLine

from collective.assets import CollectiveAssetsMessageFactory as _

class IWebAssetsEnvironment(Interface):
    """ Allow webassets environment to be an utility """


class IAssetsCPConfigSchema(Interface):
    """ """

    active = Bool(title=_('assets_active_label', default=u'Active'),
                  description=_('assets_active_help',
                      default=u'Check this to enable the Assets integration'),
                  default=False)

    debug = Bool(title=_('assets_debug_label', default=u'Debug Mode'),
                  description=_('assets_debug_help',
                      default=u'Check this to enable the Assets debug mode'),
                  default=False)

    cache = Bool(title=_('assets_cache_label', default=u'Caching'),
                  description=_('assets_cache_help',
                      default=u'Activate assets caching'),
                  default=True)

    url_expire = Bool(title=_('assets_urlexpire_label', default=u'URL expiring'),
                  description=_('assets_urlexpire_help',
                      default=u'Activate url expiring for assets'),
                  default=False)

    auto_build = Bool(title=_('assets_autobuild_label', default=u'Auto build'),
                  description=_('assets_autobuild_help',
                      default=u'Check filesystem for changes and build assets automatically'),
                  default=True)

    manifest = Choice(title=_('assets_manifest_label', default=u'Manifest'),
                  description=_('assets_manifest_help',
                      default=u''),
                  default='cache',
                  values=['file', 'cache']) # TODO use a vocabulary based on webassets.version.get_manifest

class IAssetsCPOverviewSchema(Interface):
    """ """

    css = List(title=_('assets_css_label', default=u'CSS Resources'),
                  description=_('assets_css_help',
                      default=u'CSS resources registered as webassets'),
                  default=[],
                  readonly=True,
                  value_type=TextLine())

    js = List(title=_('assets_js_label', default=u'JavaScript Resources'),
                  description=_('assets_js_help',
                      default=u'JavaScript resources registered as webassets'),
                  default=[],
                  readonly=True,
                  value_type=TextLine())
