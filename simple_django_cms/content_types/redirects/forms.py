from django import forms

from ..forms import ItemDataForm


class RedirectItemDataForm(ItemDataForm):

    source = forms.URLField()
    redirect_to = forms.URLField()
