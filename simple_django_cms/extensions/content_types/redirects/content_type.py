from ..content_type import BaseContentType

from .forms import RedirectItemDataForm
from .serializers import RedirectSerializer


class RedirectContentType(BaseContentType):

    display_name_plural = 'redirects'
    display_name_singular = 'redirect'
    has_tenant = False
    name = 'redirects'
    requires_project_admin = True
    serializer_class = RedirectSerializer
    item_data_form = RedirectItemDataForm
