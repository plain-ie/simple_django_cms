from ..conf import settings
from ..loader import load


class ContentTypeRegistry:

    content_types = {}
    content_types_list = settings.CONTENT_TYPE_LIST
    urlpatterns = []

    def __init__(self):
        self.load()

    def load(self):
        for serializer_string in self.content_types_list:
            self.register(serializer_string)

    def find(self, content_type):
        return self.content_types.get(content_type, None)

    def register(self, serializer_string):

        module = load(serializer_string)
        module = module()

        self.content_types[module.name] = module

        urlpatterns = module.get_urlpatterns()
        if len(urlpatterns) != 0:
            urlpatterns.append(urlpatterns)

    def get_content_types(
        self,
        browsable=None,
        requires_project_admin=None,
        format='list'
    ):

        _content_types = []

        for key in self.content_types.keys():

            add = True
            ct = self.content_types[key]

            if browsable is not None:
                if ct.browsable != browsable:
                    add = False

            if requires_project_admin is not None:
                if ct.requires_project_admin != requires_project_admin:
                    add = False

            if add is True:
                _content_types.append(ct)

        if format == 'choices':

            choices = []

            for x in _content_types:
                choices.append([
                    x.name,
                    x.display_name_plural
                ])

            # Order by choice[1]?

            return choices

        # Order by display_name_plural?

        return _content_types

    def serialize(
        self,
        objects,
        language,
        default_language,
    ):

        data = []

        for object in objects:
            for key in self.content_types.keys():
                content_type = self.content_types[key]
                if content_type.matches(object) is True:
                    data.append(
                        content_type.serialize(
                            object,
                            language,
                            default_language
                        )
                    )

        return data
