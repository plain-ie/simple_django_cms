from django import template

from .. import constants
from ..conf import settings


register = template.Library()


@register.simple_tag
def setting(value):
    return getattr(settings, value, None)


@register.simple_tag
def define(value):
    return value


@register.simple_tag
def constant(name):
    return getattr(constants, name, None)


@register.filter(name='extend_field_css_classes')
def extend_field_css_classes(field, classes):
    cls = field.field.widget.attrs.get('class', '')
    field.field.widget.attrs['class'] = cls + ' ' + classes
    return field


@register.filter(name='override_disabled_state')
def override_disabled_state(field, disabled):
    field.field.widget.attrs['disabled'] = disabled
    return field


@register.filter(name='override_field_attr')
def override_field_attr(field, value):
    attr_name, attr_value = value.split('|')
    field.field.widget.attrs[attr_name] = attr_value
    return field
