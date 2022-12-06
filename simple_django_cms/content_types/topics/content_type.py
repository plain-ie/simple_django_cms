from ..content_type import BaseContentType

from .forms import TopicTranslatableContentForm
from .serializers import TopicSerializer


class TopicContentType(BaseContentType):

    browsable = True
    display_name_plural = 'topics'
    display_name_singular = 'topic'
    has_tenant = False
    name = 'topics'
    serializer_class = TopicSerializer
    translatable_contents_form = TopicTranslatableContentForm
    requires_project_admin = True
