from ..content_type import BaseContentType

from .serializers import RedirectSerilizer


class RedirectContentType(BaseContentType):

    display_name_plural = 'redirects'
    display_name_singular = 'redirect'
    name = 'redirects'

    serializer_class = RedirectSerilizer
