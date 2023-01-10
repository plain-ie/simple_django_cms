from ..content_type import BaseContentType

from .forms import ImageTranslatableContentForm
from .serializers import ImageSerializer


class ImageContentType(BaseContentType):

    display_name_plural = 'images'
    display_name_singular = 'image'
    has_tenant = True
    name = 'images'
    requires_project_admin = False

    serializer_class = ImageSerializer
    translatable_contents_form = ImageTranslatableContentForm
