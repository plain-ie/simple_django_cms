from django.forms import CharField, IntegerField

from .widgets import FileURLDisplayWidget, ItemRelationParentWidget


class FileURLDisplayField(CharField):

    widget = FileURLDisplayWidget

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.disabled = True
        self.required = False


class ItemRelationParentField(IntegerField):

    widget = ItemRelationParentWidget

    def __init__(self, **kwargs):
        self.content_types = kwargs.pop('content_types', [])
        self.cross_tenant = kwargs.pop('cross_tenant', False)
        self.multiple = kwargs.pop('multiple', False)
        super().__init__(**kwargs)

    def get_choices(self, keyword, page, limit):
        return []
