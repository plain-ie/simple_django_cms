from django.contrib.auth import logout

from .... import constants

from .base import BaseViewSet


class SignOutViewSet(BaseViewSet):

    def get(self, request):

        if getattr(request.user, 'is_authenticated', False) is False:
            return self._redirect(constants.URLNAME_AUTH_SIGNIN)

        logout(request)

        return self._redirect(constants.URLNAME_AUTH_SIGNIN)
