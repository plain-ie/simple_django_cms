from .... import constants
from ....conf import settings

from .base import BaseViewSet


class RegisterViewSet(BaseViewSet):

    page_title = 'Register'
    template = settings.TEMPLATE_REGISTER

    def get(self, request):
        return self._render(request, self.template, context=self.get_context())

    def post(self, request):
        return self._redirect()

    def get_context(self):
        context = super().get_context()
        context['form'] = {
            'action': self._reverse(constants.URLNAME_AUTH_REGISTER),
            'button_text': 'Sign in',
            'method': 'POST',
            'links': [
                {
                    'href': self._reverse(constants.URLNAME_AUTH_SIGNIN),
                    'text': 'Sign in'
                },
                {
                    'href': self._reverse(constants.URLNAME_AUTH_FORGOT_PASSWORD),
                    'text': 'Forgot password'
                }
            ]
        }
        return context
