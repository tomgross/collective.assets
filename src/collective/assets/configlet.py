import zope.component
from zope.component.hooks import getSite
from zope.interface import Interface, implements
from zope.schema import Bool
from persistent import Persistent

from Products.CMFPlone.interfaces import IPloneSiteRoot
from plone.app.controlpanel.form import ControlPanelForm
from plone.app.form.validators import null_validator

from plone.fieldsets.fieldsets import FormFieldsets
from zope.formlib.form import action

from collective.assets import CollectiveAssetsMessageFactory as _
from .interfaces import IAssetsCPConfigSchema, IAssetsCPOverviewSchema, IWebAssetsEnvironment


class AssetsCPConfigAdapter(object):
    zope.component.adapts(IPloneSiteRoot)
    implements(IAssetsCPConfigSchema)

    def __init__(self, context):
        self.context = context

    def __getattr__(self, name):
        env = zope.component.getUtility(IWebAssetsEnvironment)
        if name in env.config:
            return env.config[name]
        return super(AssetsCPConfigAdapter, self).__getattr__(name)

    def __setattr__(self, name, value):
        env = zope.component.getUtility(IWebAssetsEnvironment)
        if name in env.config:
            env.config[name] = value
        else:
            object.__setattr__(self, name, value)

class AssetsCPOverviewAdapter(object):
    zope.component.adapts(IPloneSiteRoot)
    implements(IAssetsCPOverviewSchema)

    def __init__(self, context):
        self.context = context
        self.env = zope.component.getUtility(IWebAssetsEnvironment)

    @property
    def css(self):
        styles = []        
        for name, bundle in self.env._named_bundles.iteritems():
            if not name.startswith('css-'):
                continue
            styles.append('%s [%s]' % (bundle.urls()[0],
                                       bundle.extra_data.get('media', None)))
        return sorted(styles)

    @property
    def js(self):
        scripts = []        
        for name, bundle in self.env._named_bundles.iteritems():
            if not name.startswith('js-'):
                continue
            scripts.append('%s' % (bundle.urls()[0]))
        return sorted(scripts)


assetsschema = FormFieldsets(IAssetsCPConfigSchema)
assetsschema.id = 'assetsconfig'
assetsschema.label = _(u'label_assetsconfig', default=u'Configuration')

assetsoverview = FormFieldsets(IAssetsCPOverviewSchema)
assetsoverview.id = 'assetsoverview'
assetsoverview.label = _(u'label_assetsoverview', default=u'Overview')


class AssetsControlPanel(ControlPanelForm):

    form_fields = FormFieldsets(assetsschema, assetsoverview)

    label = _('label_assets_settings', default='Assets settings')
    description = _('help_assets_settings',
                    default='Settings to enable and configure web assets.')
    form_name = _('label_assets_settings', default='Assets settings')

    actions = ControlPanelForm.actions.copy()

    @action(_(u'label_generate', default=u'Generate Assets'),
            name=u'generate')
    def handle_generate_action(self, action, data):
        generateview = zope.component.queryMultiAdapter(
                (self.context, self.request), name="generate-assets")
        generateview()
