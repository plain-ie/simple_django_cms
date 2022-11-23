from django.contrib.auth.mixins import AccessMixin


class AuthenticatedUserRequiredMixin(AccessMixin):

    def dispatch(self, request, *args, **kwargs):

        if getattr(request.user, 'is_authenticated', False) is False:
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)


class SuperUserOrProjectAdminOrTenantUserRequiredMixin(AccessMixin):

    def dispatch(self, request, *args, **kwargs):

        if getattr(request.user, 'is_authenticated', False) is False:
            return self.handle_no_permission()

        if request.user.is_superuser is True:
            return super().dispatch(request, *args, **kwargs)

        project_id = kwargs.get('project_id', '-1')
        tenant_id = kwargs.get('tenant_id', '-1')

        if request.user.is_project_admin(project_id) is True:
            return super().dispatch(request, *args, **kwargs)

        if request.user.is_project_tenant_user(project_id, tenant_id) is True:
            return super().dispatch(request, *args, **kwargs)

        return self.handle_no_permission()


class SuperUserRequiredMixin(AccessMixin):

    def dispatch(self, request, *args, **kwargs):

        if getattr(request.user, 'is_authenticated', False) is False:
            return self.handle_no_permission()

        if request.user.is_superuser is True:
            return super().dispatch(request, *args, **kwargs)

        return self.handle_no_permission()
