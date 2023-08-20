from django import forms
from django.forms import widgets

from ... import constants

from ..fields import ItemRelationParentField
from ..forms import TranslatableContentForm, ItemRelationForm


class TopicTranslatableContentForm(TranslatableContentForm):

    language = forms.CharField(widget=widgets.HiddenInput())
    title = forms.CharField()
    slug = forms.SlugField(disabled=True, required=False)
