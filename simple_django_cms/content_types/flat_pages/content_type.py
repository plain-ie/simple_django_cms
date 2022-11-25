from .forms import (
    FlatPageItemForm,
    FlatPageTranslatableContenFormSet,
)

from ..base import BaseContentType


class FlatPageContentType(BaseContentType):

    browsable = True
    display_name_plural = 'flat pages'
    display_name_singular = 'flat page'
    name = 'flat_pages'

    item_form = FlatPageItemForm
    translatable_contents_form = FlatPageTranslatableContenFormSet
    relations_form = None
