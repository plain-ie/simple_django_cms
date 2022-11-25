from django.db.models import Q

from ...models import ProjectAdmin, TenantUser, User


class UserQuerySetClient:

    def get_user(self, user_id):
        return User.objects.get(id=user_id)

    # --

    def user_is_project_admin(self, project_id, user_id):
        return ProjectAdmin.objects.filter(
            user_id=user_id,
            project_id=project_id
        ).exists()

    # --

    def user_has_project_access(
        self,
        project_id,
        user_id,
    ):

        condition = Q()

        condition.add(
            Q(
                id=user_id,
                tenants__tenant__projects__project_id=project_id,
                tenants__user_id=user_id,
            ),
            Q.OR
        )

        condition.add(
            Q(
                id=user_id,
                projects__user_id=user_id,
                projects__project_id=project_id,
            ),
            Q.OR
        )

        return User.objects.filter(condition).exists()

    # --

    def user_has_tenant_access(
        self,
        project_id,
        tenant_id,
        user_id
    ):

        condition = Q()

        condition.add(
            Q(
                id=user_id,
                tenants__tenant__projects__project_id=project_id,
                tenants__user_id=user_id,
                tenants__tenant_id=tenant_id,
            ),
            Q.OR
        )

        condition.add(
            Q(
                id=user_id,
                projects__user_id=user_id,
                projects__project_id=project_id,
            ),
            Q.OR
        )

        return User.objects.filter(condition).exists()
