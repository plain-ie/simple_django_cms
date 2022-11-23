from django import template

from .. import constants


register = template.Library()


@register.simple_tag
def define(value):
    return value


@register.simple_tag
def constant(name):
    return getattr(constants, name, None)
