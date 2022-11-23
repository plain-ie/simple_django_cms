from ..conf import settings
from ..loader import load


class ContentTypeRegistry:

    content_types = {}
    content_types_list = settings.CONTENT_TYPE_LIST

    def __init__(self):
        self.load()

    def load(self):
        for serializer_string in self.content_types_list:
            self.register(serializer_string)

    def find(self, content_type):
        return self.content_types.get(content_type, None)

    def register(self, serializer_string):
        module = load(serializer_string)
        self.content_types[module.name] = module

    def get_content_types(
            self,
            content_types=None,
            browsable=None,
            format='list'
            ):

        format_choices = [
            'list',
            'choices'
        ]

        if isinstance(content_types, list) is False and content_types is not None:
            content_types = [content_types, ]

        if format not in format_choices:
            raise ValueError('Format is not supported')

        _content_types = []

        for key in self.content_types.keys():

            add = True
            serializer = self.content_types[key]

            if browsable is False and serializer.browsable is True:
                add = False

            if content_types is not None:
                if len(content_types) != 0:
                    if serializer._content_type not in content_types:
                        add = False

            if add is True:
                _content_types.append(serializer)

        if format == 'choices':
            choices = []
            for x in _content_types:
                choices.append([
                    x._content_type,
                    x._display_name_plural
                ])
            return choices

        return _content_types

    def get_urlpatterns(self):
        return []

    def serialize(self, objects, many=False):
        return next(iter([]), None)
