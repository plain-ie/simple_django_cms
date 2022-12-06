from django import forms
from django.forms import widgets

from ..forms import ItemForm, TranslatableContentForm


class TopicTranslatableContentForm(TranslatableContentForm):

    language = forms.CharField(widget=widgets.HiddenInput())
    title = forms.CharField()
    slug = forms.SlugField(disabled=True, required=False)
