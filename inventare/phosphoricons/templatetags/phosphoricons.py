from django import template
from django.conf import settings
from django.utils.html import format_html

register = template.Library()

def get_model_icon_name(app: str, model: str):
    info_upper = (app.upper(), model.upper())
    if hasattr(settings, 'ICON_%s_%s' % info_upper):
        return getattr(settings, 'ICON_%s_%s' % info_upper)
    
    info = (app, model)
    if not hasattr(settings, 'MODEL_ICONS'):
        return None
    model_name = '%s.%s' % info
    model_icons = getattr(settings, 'MODEL_ICONS')
    if not hasattr(model_icons, 'get'):
        return None
    return model_icons.get(model_name)

def get_app_icon_name(app: str):
    app_upper = app.upper()
    if hasattr(settings, 'ICON_%s' % app_upper):
        return getattr(settings, 'ICON_%s' % app_upper)
    
    if not hasattr(settings, 'APP_ICONS'):
        return None
    app_icons = getattr(settings, 'APP_ICONS')
    if not hasattr(app_icons, 'get'):
        return None
    return app_icons.get(app)

@register.simple_tag
def model_icon(app: str, model: str):
    icon = get_model_icon_name(app, model)
    return icon

@register.simple_tag
def app_icon(app: str):
    icon = get_app_icon_name(app)
    return icon

@register.simple_tag
def phosphor_bold(icon: str, *extra_classes: list[str]):
    return format_html('<i class="ph-bold ph-{} {}"></i>', icon, " ".join(extra_classes))

@register.simple_tag
def phosphor(icon: str, *extra_classes: list[str]):
    return format_html('<i class="ph ph-{} {}"></i>', icon, " ".join(extra_classes))

@register.simple_tag
def model_icon_tag(app: str, model: str):
    icon = model_icon(app, model)
    if not icon:
        return ''
    return phosphor(icon, 'sidebar-icon')

@register.simple_tag
def app_icon_tag(app: str):
    icon = app_icon(app)
    if not icon:
        return ''
    return phosphor(icon, 'sidebar-icon')
