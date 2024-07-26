from django import template
from django.contrib.admin import site
from django.forms.boundfield import BoundField
from django.utils.html import format_html
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _

register = template.Library()

@register.simple_tag
def form_control(field: BoundField):
    
    help_text = field.help_text or ""
    classes = ['form-control']
    if field.errors:
        help_text = field.errors[0]
        classes.append('invalid')

    if help_text:
        help_text = format_html('<span class="helper-text">{}</span>', help_text)

    return format_html('<div class="{}">{}{}{}</div>', " ".join(classes), field.label_tag(), field, help_text)

@register.simple_tag
def is_route_on_admin_model(model: dict, request: HttpRequest):
    ModelClass = model.get('model')
    info = (ModelClass._meta.app_label, ModelClass._meta.model_name)
    base_path = "/admin/%s/%s/" % info

    if not request.path.startswith(base_path):
        return False
    path = request.path[len(base_path):]

    model_admin = site._registry.get(ModelClass)

    urls = model_admin.get_urls()
    for item in urls:
        if not item.resolve(path):
            continue
        return True
    
    return False

@register.simple_tag
def is_route_on_admin_app(app: dict, request: HttpRequest):
    for model in app.get('models'):
        if not is_route_on_admin_model(model, request):
            continue
        return True
    return False

@register.simple_tag
def is_on_admin_route(url: str, request: HttpRequest):
    return url == request.path

@register.simple_tag
def get_active_display(choices: dict):
    choices = list(filter(lambda item: item.get('selected'), choices))
    if not choices:
        return _('select')
    return choices[0].get('display')
