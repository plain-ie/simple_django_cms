from django import forms
from django.forms import widgets

from ..forms import ItemForm, TranslatableContentForm


class NewsItemForm(ItemForm):

    published_at = forms.DateTimeField(required=False)


class NewsTranslatableContentForm(TranslatableContentForm):

    language = forms.CharField(widget=widgets.HiddenInput())
    title = forms.CharField()
    slug = forms.SlugField(disabled=True, required=False)
    content = forms.CharField(widget=widgets.Textarea(), required=False)
