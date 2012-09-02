from zope.component import adapts, queryUtility
from zope.interface import Interface, implements
from zope.schema import Bool

from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from Products.CMFPlone.interfaces import IPloneSiteRoot
from plone.app.controlpanel.form import ControlPanelForm

from zope.formlib.form import FormFields

from collective.assets import CollectiveAssetsMessageFactory as _
from collective.assets.interfaces import IAssetsSchema, IAssetsConfig

class IAssetsSchema(Interface):
    """ """

    active = Bool(title=_('label_active', default=u'Active'), default=False,
        description=_('help_active',
                      default=(u'Check this to enable the web assets '
                                'integration.')))
 


class AssetsControlPanelAdapter(SchemaAdapterBase):
    adapts(IPloneSiteRoot)
    implements(IAssetsSchema)

    def getActive(self):
        util = queryUtility(IAssetsConfig)
        return getattr(util, 'active', '')

    def setActive(self, value):
        util = queryUtility(IAssetsConfig)
        if util is not None:
            util.active = value
        self.reset()

    active = property(getActive, setActive)


class AssetsControlPanel(ControlPanelForm):

    form_fields = FormFields(IAssetsSchema)

    label = _('label_assets_settings', default='Assets settings')
    description = _('help_assets_settings',
                     default='Settings to enable and configure web assets.')
    form_name = _('label_assets_settings', default='Assets settings')
