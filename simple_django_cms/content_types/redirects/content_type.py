from ..base import BaseContentType

from .forms import RedirectItemDataForm


class RedirectContentType(BaseContentType):

    display_name_plural = 'redirects'
    display_name_singular = 'redirect'
    name = 'redirects'

    item_data_form = RedirectItemDataForm
