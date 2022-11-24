from django.shortcuts import redirect, render, reverse
from django.views import View


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

    def _render(self, request, template, context):
        return render(request, template, context=context)

    def _redirect(self, redirect_to):
        return redirect(redirect_to)

    def _reverse(self, name, kwargs={}):
        return reverse(name, kwargs=kwargs)
