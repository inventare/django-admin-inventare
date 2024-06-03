from django import template
from django.forms.boundfield import BoundField
from django.utils.html import format_html

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
