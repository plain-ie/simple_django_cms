from django import forms
from django.forms import widgets

from ..fields import FileURLDisplayField
from ..forms import TranslatableContentForm


class ImageTranslatableContentForm(TranslatableContentForm):

    language = forms.CharField(widget=widgets.HiddenInput())
    title = forms.CharField()
    description = forms.CharField(widget=widgets.Textarea(), required=False)
    file_url = FileURLDisplayField()
    file = forms.FileField(required=False)
