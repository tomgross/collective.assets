from zope.interface import Interface
from zope.schema import Bool, Text

from collective.assets import CollectiveAssetsMessageFactory as _

class IWebAssetsEnvironment(Interface):
    """ Allow webassets environment to be an utility """

class IAssetsConfig(Interface):
    """ """

class IAssetsSchema(Interface):
    """ """

    active = Bool(title=_('assets_active_label', default=u'Active'),
                  description=_('assets_active_help',
                      default=u'Check this to enable the Assets integration'),
                  default=False)


class IAssetsOverview(Interface):

    css = Text(title=_('assets_css_label', default=u'CSS Resources'),
                  description=_('assets_css_help',
                      default=u'CSS resources registered as webassets'),
                  default=u'',
                  readonly=True)

    js = Text(title=_('assets_js_label', default=u'JavaScript Resources'),
                  description=_('assets_js_help',
                      default=u'JavaScript resources registered as webassets'),
                  default=u'',
                  readonly=True)
