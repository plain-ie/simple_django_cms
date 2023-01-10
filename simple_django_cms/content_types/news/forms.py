from django import forms
from django.forms import widgets

from ... import constants

from ..fields import ItemRelationParentField
from ..forms import ItemForm, TranslatableContentForm, ItemRelationForm

from ..topics.content_type import TopicContentType


class NewsItemForm(ItemForm):

    published_at = forms.DateTimeField(required=False)


class NewsTranslatableContentForm(TranslatableContentForm):

    language = forms.CharField(widget=widgets.HiddenInput())
    title = forms.CharField()
    slug = forms.SlugField(disabled=True, required=False)
    content = forms.CharField(widget=widgets.Textarea(), required=False)
