from django import template

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

    return {
        'brand_logo_url': None,
        'brand_url': '/',
        'brand_title': 'XXX',
        'links': links,
        'request': request,
    }
