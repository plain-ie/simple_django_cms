from django import forms
from django.utils.text import slugify


class ItemForm(forms.Form):
    pass


class ItemDataForm(forms.Form):
    pass


class TranslatableContentForm(forms.Form):

    slug = forms.SlugField(disabled=True, required=False)

    def clean_slug(self):
        title = self.cleaned_data['title']
        return slugify(title)
