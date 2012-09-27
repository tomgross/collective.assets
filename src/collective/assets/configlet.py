import zope.component
from zope.component.hooks import getSite
from zope.interface import Interface, implements
from zope.schema import Bool
from persistent import Persistent

from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from Products.CMFPlone.interfaces import IPloneSiteRoot
from plone.app.controlpanel.form import ControlPanelForm

from plone.fieldsets.fieldsets import FormFieldsets
from zope.formlib.form import action

from collective.assets import CollectiveAssetsMessageFactory as _
from .interfaces import IAssetsSchema, IAssetsConfig, IAssetsOverview, IWebAssetsEnvironment


class AssetsConfig(Persistent):

    implements(IAssetsConfig)

    def __init__(self):
        self.active = False


class AssetsControlPanelAdapter(SchemaAdapterBase):
    zope.component.adapts(IPloneSiteRoot)
    implements(IAssetsSchema)

    def getActive(self):
        util = zope.component.queryUtility(IAssetsConfig)
        return getattr(util, 'active', '')

    def setActive(self, value):
        util = zope.component.queryUtility(IAssetsConfig)
        if util is not None:
            util.active = value

    active = property(getActive, setActive)


class AssetsOverviewAdapter(SchemaAdapterBase):
    zope.component.adapts(IPloneSiteRoot)
    implements(IAssetsOverview)

    @property
    def css(self):
        env = zope.component.getUtility(IWebAssetsEnvironment)
        styles = []        
        for name, bundle in env._named_bundles.iteritems():
            if not name.startswith('css-'):
                continue
            styles.append('%s [%s]' % (bundle.urls()[0],
                                       bundle.extra_data.get('media', None)))
        styles.sort()
        return '\r\n'.join(styles)

    @property
    def js(self):
        env = zope.component.getUtility(IWebAssetsEnvironment)
        scripts = []        
        for name, bundle in env._named_bundles.iteritems():
            if not name.startswith('js-'):
                continue
            scripts.append('%s' % (bundle.urls()[0]))
        scripts.sort()
        return '\r\n'.join(scripts)


assetsschema = FormFieldsets(IAssetsSchema)
assetsschema.id = 'assetsconfig'
assetsschema.label = _(u'label_assetsconfig', default=u'Configuration')

assetsoverview = FormFieldsets(IAssetsOverview)
assetsoverview.id = 'assetsoverview'
assetsoverview.label = _(u'label_assetsoverview', default=u'Overview')


class AssetsControlPanel(ControlPanelForm):

    form_fields = FormFieldsets(assetsschema, assetsoverview)

    label = _('label_assets_settings', default='Assets settings')
    description = _('help_assets_settings',
                     default='Settings to enable and configure web assets.')
    form_name = _('label_assets_settings', default='Assets settings')

    @action(_(u'label_generate', default=u'Generate Assets'),
            name=u'generate')
    def handle_generate_action(self, action, data):
        generateview = zope.component.queryMultiAdapter(
                (self.context, self.request), name="generate-assets")
        return generateview()
