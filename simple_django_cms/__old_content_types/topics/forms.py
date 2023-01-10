from django import forms
from django.forms import widgets

from ... import constants

from ..fields import ItemRelationParentField
from ..forms import TranslatableContentForm, ItemRelationForm


class TopicTranslatableContentForm(TranslatableContentForm):

    language = forms.CharField(widget=widgets.HiddenInput())
    title = forms.CharField()
    slug = forms.SlugField(disabled=True, required=False)


class TopicRelationForm(ItemRelationForm):

    parent = ItemRelationParentField(
        content_types=[
            constants.CONTENT_TYPE_NAME_TOPICS
        ],
    )
    status = forms.CharField(
        widget=widgets.HiddenInput(),
        disabled=True,
        initial=constants.RELATION_NAME_TOPICS
    )
