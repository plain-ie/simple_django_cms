from django.shortcuts import redirect, render, reverse
from django.views import View

from ....clients.internal.content_types import ContentTypeQuerySetClient
from ....clients.internal.items import ItemQuerySetClient


class BaseViewSet(View):

    page_title = ''

    def get_context(self):
        return {
            'page': {
                'title': self.page_title,
            },
            'view': {
                'kwargs': self.kwargs
            }
        }

    def get_item(self, item_id):
        return ItemQuerySetClient().get_item(item_id)

    def get_content_type(self, content_type):
        return ContentTypeQuerySetClient().get_content_type(content_type)

    def _render(self, request, template, context):
        return render(request, template, context=context)

    def _redirect(self, redirect_to):
        return redirect(redirect_to)

    def _reverse(self, name, kwargs={}):
        return reverse(name, kwargs=kwargs)
