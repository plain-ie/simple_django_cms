from ..content_type import BaseContentType

from .forms import FlatPageTranslatableContentForm


class FlatPageContentType(BaseContentType):

    browsable = True
    display_name_plural = 'flat pages'
    display_name_singular = 'flat page'
    has_tenant = False
    name = 'flat_pages'
    requires_project_admin = True

    translatable_contents_form = FlatPageTranslatableContentForm
