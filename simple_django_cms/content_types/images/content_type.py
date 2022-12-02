from ..content_type import BaseContentType


class ImageContentType(BaseContentType):

    display_name_plural = 'images'
    display_name_singular = 'image'
    has_tenant = True
    name = 'images'
    requires_project_admin = False
