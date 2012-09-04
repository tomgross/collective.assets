from zope.interface import Interface
from zope.schema import Bool

from collective.assets import CollectiveAssetsMessageFactory as _

class IAssetsConfig(Interface):
    """ """


class IAssetsSchema(Interface):
    """ """

    active = Bool(title=_('assets_active_label', default=u'Active'),
                  description=_('assets_active_help',
                      default=u'Check this to enable the Assets integration'),
                  default=False)


