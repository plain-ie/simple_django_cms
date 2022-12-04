from ..content_type import BaseContentType


class TopicContentType(BaseContentType):

    browsable = True
    display_name_plural = 'topics'
    display_name_singular = 'topic'
    has_tenant = False
    name = 'topics'
    requires_project_admin = True
