from ...models import ProjectAdmin, TenantUser, User


class UserQuerySetClient:

    def get_user(self, user_id):
        return User.objects.get(id=user_id)

    def user_is_project_admin(self, project_id, user_id):
        return ProjectAdmin.objects.filter(
            user_id=user_id,
            project_id=project_id
        ).exists()

    def user_is_project_user(self, project_id, user_id):
        return TenantUser.objects.filter(
            user_id=user_id,
            tenant__projects__project_id=project_id
        ).prefetch_related(
            'tenant__projects'
        ).exists()

    def user_is_project_tenant_user(self, project_id, tenant_id, user_id):
        return ProjectAdmin.objects.filter(
            user_id=user_id,
            project_id=project_id
        ).exists()

    def user_has_project_access(
        self,
        project_id,
        user_id,
        fresh=False,
    ):

        user = self.get_user(user_id)

        project_admin_exists = self.user_is_project_admin(project_id, user_id)
        if project_admin_exists is True:
            return True

        tenant_user_exists = self.user_is_project_user(project_id, user_id)
        if tenant_user_exists is True:
            return True

        return False
