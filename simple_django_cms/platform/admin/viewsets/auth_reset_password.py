from .... import constants
from ....conf import settings

from .base import BaseViewSet


class ResetPasswordViewSet(BaseViewSet):

    page_title = 'Reset password'
    template = settings.TEMPLATE_RESET_PASSWORD

    def get(self, request):
        return self._render(request, self.template, context=self.get_context())

    def post(self, request):
        return self._redirect()

    def get_context(self):
        context = super().get_context()
        context['form'] = {
            'action': self._reverse(constants.URLNAME_AUTH_RESET_PASSWORD),
            'button_text': 'Reset password',
            'method': 'POST',
            'links': [
                {
                    'href': self._reverse(constants.URLNAME_AUTH_SIGNIN),
                    'text': 'Sign in'
                },
                {
                    'href': self._reverse(constants.URLNAME_AUTH_REGISTER),
                    'text': 'Register'
                }
            ]
        }
        return context
