from django import template
from django.contrib.admin import site
from django.contrib.admin.helpers import AdminField
from django.forms.boundfield import BoundField
from django.utils.html import format_html
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _
from django.contrib.admin.views.main import PAGE_VAR
from django.utils.safestring import mark_safe

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
    if choices[0].get('inline_display'):
        return choices[0].get('inline_display')
    return choices[0].get('display')

@register.simple_tag
def paginator_number(cl, i):
    """
    Generate an individual page index link in a paginated list.
    """
    if i == cl.paginator.ELLIPSIS:
        return format_html("{} ", cl.paginator.ELLIPSIS)
    elif i == cl.page_num:
        return format_html('<span class="this-page">{}</span> ', i)
    else:
        pagination_template = '<a href="#" hx-post="./table/{}" hx-params="csrfmiddlewaretoken" hx-target="#changelist" hx-swap="outerHTML" hx-indicator="#changelist-indicator" {}>{}</a> '
        return format_html(
            pagination_template,
            cl.get_query_string({PAGE_VAR: i}),
            mark_safe(' class="end"' if i == cl.paginator.num_pages else ""),
            i,
        )
    
@register.simple_tag
def get_error_message(field: AdminField):
    if (not field.field):
        return None
    if not field.field.errors:
        return None
    errors = list(field.field.errors)
    return errors[0]
