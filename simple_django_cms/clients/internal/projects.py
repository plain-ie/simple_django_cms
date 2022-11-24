import math

from django.db.models import Q

from ...models import Project

from .users import UserQuerySetClient


class ProjectQuerySetClient:

    def get_project(self, project_id,):
        return Project.objects.get(id=project_id)

    def get_projects(
        self,
        user_id,
        keyword=None,
        name=None,
        page=1,
        limit=0,
        paginate=False,
    ):

        user_client = UserQuerySetClient()
        user = user_client.get_user(user_id)

        queryset = Project.objects.all().order_by('name')

        if name is not None:
            queryset = queryset.filter(name__icontains=name)

        condition = Q()
        condition.add(Q(tenants__tenant__users__user=user), Q.OR)
        condition.add(Q(users__user=user), Q.OR)

        queryset = queryset.filter(
            condition
        ).prefetch_related(
            'tenants',
            'users'
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
