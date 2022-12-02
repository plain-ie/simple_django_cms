from ..content_type import BaseContentType


class FlatPageContentType(BaseContentType):

    browsable = True
    display_name_plural = 'flat pages'
    display_name_singular = 'flat page'
    has_tenant = True
    name = 'flat_pages'
    requires_project_admin = False
