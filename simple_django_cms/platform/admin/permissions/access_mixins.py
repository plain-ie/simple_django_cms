from django.contrib.auth.mixins import AccessMixin

from ....clients.internal.users import UserQuerySetClient


class AuthenticatedUserRequiredMixin(AccessMixin):

    def dispatch(self, request, *args, **kwargs):

        if request.user.is_authenticated is False:
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)


class ProjectAccessRequiredMixin(AccessMixin):

    def dispatch(self, request, *args, **kwargs):

        if request.user.is_authenticated is False:
            return self.handle_no_permission()

        user_client = UserQuerySetClient()
        has_access = user_client.user_has_project_access(
            kwargs['project_id'],
            request.user.id
        )

        if has_access is True:
            return super().dispatch(request, *args, **kwargs)

        return self.handle_no_permission()
