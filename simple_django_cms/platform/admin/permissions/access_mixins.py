from django.contrib.auth.mixins import AccessMixin

from ....clients.internal.users import UserQuerySetClient


class AuthenticatedUserRequiredMixin(AccessMixin):

    def dispatch(self, request, *args, **kwargs):

        if request.user.is_authenticated is False:
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)


class ProjectTenantAccessRequiredMixin(AccessMixin):

    def dispatch(self, request, *args, **kwargs):

        if request.user.is_authenticated is False:
            return self.handle_no_permission()

        has_access = UserQuerySetClient().user_has_tenant_access(
            kwargs['project_id'],
            kwargs['tenant_id'],
            request.user.id
        )

        if has_access is True:
            return super().dispatch(request, *args, **kwargs)

        return self.handle_no_permission()


class ProjectAccessRequiredMixin(AccessMixin):

    def dispatch(self, request, *args, **kwargs):

        if request.user.is_authenticated is False:
            return self.handle_no_permission()

        has_access = UserQuerySetClient().user_has_project_access(
            kwargs['project_id'],
            request.user.id
        )

        if has_access is True:
            return super().dispatch(request, *args, **kwargs)

        return self.handle_no_permission()


class ProjectAdminAccessRequiredMixin(AccessMixin):

    def dispatch(self, request, *args, **kwargs):

        if request.user.is_authenticated is False:
            return self.handle_no_permission()

        has_access = UserQuerySetClient().user_is_project_admin(
            kwargs['project_id'],
            request.user.id
        )

        if has_access is True:
            return super().dispatch(request, *args, **kwargs)

        return self.handle_no_permission()
