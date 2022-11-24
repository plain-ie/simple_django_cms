import math

from ...models import Tenant

from .users import UserQuerySetClient


class TenantQuerySetClient:

    def get_tenant(self, tenant_id):
        return Tenant.objects.get(id=tenant_id)

    def get_tenants(
        self,
        project_id,
        user_id,
        keyword=None,
        page=1,
        limit=10,
        paginate=False,
        fresh=False,
        format='queryset',
    ):

        queryset = Tenant.objects.filter(
            projects__project_id=project_id
        ).order_by(
            'name'
        ).prefetch_related(
            'projects'
        )

        user_client = UserQuerySetClient()

        user = user_client.get_user(user_id)

        if user_client.user_is_project_admin(project_id, user_id) is False:
            queryset = queryset.filter(
                projects__project_id=project_id,
                users__user=user
            )

        if keyword is not None:
            queryset = queryset.filter(
                name__icontains=keyword
            )

        queryset = queryset.distinct()

        total = queryset.count()

        try:
            pages = math.ceil(total / limit)
        except ZeroDivisionError:
            pages = 1

        if pages == 0:
            pages = 1

        if format == 'choices':
            queryset = list(queryset.values_list('id', 'name'))

        if paginate is True:

            skip_from = ((page - 1) * limit)
            skip_to = skip_from + limit

            queryset = queryset[skip_from:skip_to]

        return {
            'results': queryset,
            'page': page,
            'pages': pages,
            'total': total
        }
