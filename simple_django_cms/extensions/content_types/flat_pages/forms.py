from django import forms
from django.forms import widgets

from ..forms import TranslatableContentForm


class FlatPageTranslatableContentForm(TranslatableContentForm):

    language = forms.CharField(widget=widgets.HiddenInput())
    title = forms.CharField()
    slug = forms.SlugField(disabled=True)
    content = forms.CharField(widget=widgets.Textarea(), required=False)
