from django.forms import CharField

from .widgets import FileURLDisplayWidget


class FileURLDisplayField(CharField):

    widget = FileURLDisplayWidget

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.disabled = True
        self.required = False
