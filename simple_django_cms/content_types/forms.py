from django import forms
from django.forms import widgets
from django.forms.formsets import BaseFormSet as DjBaseFormSet
from django.forms.formsets import DEFAULT_MIN_NUM, DEFAULT_MAX_NUM
from django.forms.renderers import get_default_renderer
from django.utils.text import slugify

from .. import constants

from .fields import ItemRelationParentField


class BaseFormSet(DjBaseFormSet):

    def __init__(self, *args, **kwargs):
        formset_title = kwargs.get('formset_title', None)
        if formset_title is not None:
            self.formset_title = kwargs.pop('formset_title')
        super().__init__(*args, **kwargs)


class ItemForm(forms.Form):
    pass


class ItemDataForm(forms.Form):
    pass


class TranslatableContentForm(forms.Form):

    def clean_slug(self):
        return slugify(self.cleaned_data['title'])


class ItemRelationForm(forms.Form):

    STATUS = constants.RELATION_NAME_NOT_SET

    parent = ItemRelationParentField(
        content_types=[
            constants.CONTENT_TYPE_NAME_TOPICS
        ],
    )
    status = forms.CharField(widget=widgets.HiddenInput(), initial=STATUS)

    def clean_status(self):
        return self.STATUS


def formset_factory(
    form,
    formset=BaseFormSet,
    extra=1,
    can_order=False,
    can_delete=False,
    max_num=None,
    validate_max=False,
    min_num=None,
    validate_min=False,
    absolute_max=None,
    can_delete_extra=True,
    renderer=None,
    formset_title=None,
):

    if min_num is None:
        min_num = DEFAULT_MIN_NUM

    if max_num is None:
        max_num = DEFAULT_MAX_NUM

    if absolute_max is None:
        absolute_max = max_num + DEFAULT_MAX_NUM

    if max_num > absolute_max:
        raise ValueError('"absolute_max" must be greater or equal to "max_num".')

    attrs = {
        'form': form,
        'extra': extra,
        'can_order': can_order,
        'can_delete': can_delete,
        'can_delete_extra': can_delete_extra,
        'min_num': min_num,
        'max_num': max_num,
        'absolute_max': absolute_max,
        'validate_min': validate_min,
        'validate_max': validate_max,
        'renderer': renderer or get_default_renderer(),
        'formset_title': formset_title,
    }

    return type(form.__name__ + 'FormSet', (formset,), attrs)
