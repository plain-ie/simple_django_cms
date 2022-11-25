from django import forms
from django.forms import widgets
from django.forms import formset_factory

from ...conf import settings


class FlatPageItemForm(forms.Form):

    published_at = forms.DateTimeField(required=False)


class FlatPageTranslatableContentForm(forms.Form):

    language = forms.CharField(widget=widgets.HiddenInput())
    title = forms.CharField()
    content = forms.CharField(widget=widgets.Textarea(), required=False)


class FlatPageRelationForm(forms.Form):
    pass


FlatPageTranslatableContenFormSet = formset_factory(
    FlatPageTranslatableContentForm,
    extra=0,
)


FlatPageRelationFormSet = formset_factory(
    FlatPageRelationForm,
    extra=0,
)
