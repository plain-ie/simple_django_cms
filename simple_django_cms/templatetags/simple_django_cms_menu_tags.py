from django import template
from django.shortcuts import reverse

from .. import constants
from ..conf import settings


register = template.Library()


@register.inclusion_tag(
    f'{settings.APP_NAME}/platform/admin/components/footer.html',
    takes_context=True
)
def footer(context):
    request = context['request']
    return {
        'request': request
    }


@register.inclusion_tag(
    f'{settings.APP_NAME}/platform/admin/components/mainmenu.html',
    takes_context=True
)
def main_menu(context):

    request = context['request']
    links = []

    if getattr(request.user, 'is_authenticated', False) is False:
        links.append({
            'text': 'Sign in',
            'href': reverse(constants.URLNAME_AUTH_SIGNIN)
        })

    else:
        links.append({
            'text': request.user.email,
            'children': [
                {
                    'text': 'Sign out',
                    'href': reverse(constants.URLNAME_AUTH_SIGNOUT)
                }
            ]
        })

    return {
        'brand_logo_url': None,
        'brand_url': '/',
        'brand_title': 'XXX',
        'links': links,
        'request': request,
    }
