from django.contrib.auth import authenticate, login

from .... import constants
from ....conf import settings

from .base import BaseViewSet


class SignInViewSet(BaseViewSet):

    page_title = 'Sign in'
    template = settings.TEMPLATE_SIGNIN

    def get(self, request):

        if getattr(request.user, 'is_authenticated', False) is True:
            return self._redirect(constants.URLNAME_ADMIN_LIST_PROJECTS)

        return self._render(request, self.template, context=self.get_context())

    def post(self, request):

        try:
            email = request.POST['email']
        except KeyError:
            return self._redirect(constants.URLNAME_AUTH_SIGNIN)

        try:
            password = request.POST['password']
        except KeyError:
            return self._redirect(constants.URLNAME_AUTH_SIGNIN)

        user = authenticate(request, email=email, password=password)

        if user is None:
            return self._redirect(constants.URLNAME_AUTH_SIGNIN)

        login(request, user)

        return self._redirect(constants.URLNAME_ADMIN_LIST_PROJECTS)

    def get_context(self):
        context = super().get_context()
        context['form'] = {
            'action': self._reverse(constants.URLNAME_AUTH_SIGNIN),
            'button_text': 'Sign in',
            'method': 'POST',
            'links': [
                {
                    'href': self._reverse(constants.URLNAME_AUTH_FORGOT_PASSWORD),
                    'text': 'Forgot password'
                },
                {
                    'href': self._reverse(constants.URLNAME_AUTH_REGISTER),
                    'text': 'Register'
                }
            ]
        }
        return context
