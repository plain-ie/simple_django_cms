import math

from ...conf import settings


class ContentTypeQuerySetClient:

    def get_content_type(self, content_type):
        return settings.CONTENT_TYPE_REGISTRY.find(content_type)

    def get_content_types(
        self,
        project_id,
        user_id,
        keyword=None,
        page=1,
        limit=0,
        paginate=False,
        format='choices'
    ):

        queryset = settings.CONTENT_TYPE_REGISTRY.get_content_types(
            format='choices'
        )

        total = len(queryset)

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
            'total': total,
            'page': page,
            'pages': pages,
        }
