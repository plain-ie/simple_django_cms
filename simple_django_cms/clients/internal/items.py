import math

from ...models import Item

from .users import UserQuerySetClient


class ItemQuerySetClient:

    def get_item(self, item_id):
        return Item.objects.get(id=item_id)

    def get_items(
        self,
        project_id,
        user_id,
        keyword=None,
        tenant=None,
        content_type=None,
        content_types=None,
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
            # deleted=deleted,
        ).prefetch_related(
            # 'translatable_contents',
            'parents__parent',
        ).order_by(
            '-created_at'
        )

        if content_types is not None:
            queryset = queryset.filter(
                content_type__in=content_types,
            )

        if user_client.user_is_project_admin(project_id, user_id) is False:
            queryset = queryset.filter(
                tenant__projects__project_id=project_id,
                tenant__users__user=user
            )

        if content_type not in [None, '', ' ']:
            queryset = queryset.filter(
                content_type=content_type
            )

        if tenant not in [None, '', ' ']:
            queryset = queryset.filter(
                tenant_id=tenant
            )

        if keyword not in [None, '', ' ']:
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

    def create(
        self,
        item_data,
        relations_data=[],
    ):

        item = Item.objects.create(**item_data)

        return item

    def update(
        self,
        item_id,
        item_data,
        relations_data=[],
    ):

        items = Item.objects.filter(id=item_id).update(**item_data)

        return self.get_item(item_id)
