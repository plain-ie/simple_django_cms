from ..content_type import BaseContentType


class NewsContentType(BaseContentType):

    browsable = True
    display_name_plural = 'news'
    display_name_singular = 'news'
    has_tenant = True
    name = 'news'
    requires_project_admin = False
