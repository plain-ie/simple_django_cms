import math

from ...models import Item

from .users import UserQuerySetClient


class ItemQuerySetClient:

    def get_items(
        self,
        project_id,
        user_id,
        keyword=None,
        tenant=None,
        content_type=None,
        status=None,
        deleted=False,
        page=1,
        limit=10,
        paginate=False,
    ):

        user_client = UserQuerySetClient()
        user = user_client.get_user(user_id)

        queryset = Item.objects.filter(
            project_id=project_id,
            deleted=deleted,
        ).prefetch_related(
            'translatable_contents',
            'parents__parent',
        ).order_by(
            '-created_at'
        )

        if user_client.user_is_project_admin(project_id, user_id) is False:
            queryset = queryset.filter(
                tenant__projects__project_id=project_id,
                tenant__users__user=user
            )

        if content_type is not None:
            queryset = queryset.filter(
                content_type=content_type
            )

        if tenant is not None:
            queryset = queryset.filter(
                tenant_id=tenant
            )

        if keyword is not None:
            queryset = queryset.filter(
                translatable_contents__title__icontains=keyword
            )

        queryset = queryset.distinct()

        total = queryset.count()

        if paginate is True:

            skip_from = ((page - 1) * limit)
            skip_to = skip_from + limit

            queryset = queryset[skip_from:skip_to]

        try:
            pages = math.ceil(total / limit)
        except ZeroDivisionError:
            pages = 1

        if pages == 0:
            pages = 1

        return {
            'results': queryset,
            'page': page,
            'pages': pages,
            'total': total
        }
