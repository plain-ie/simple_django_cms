from django import forms

from ...conf import settings


class RedirectItemDataForm(forms.Form):

    source = forms.URLField()
    redirect_to = forms.URLField()
