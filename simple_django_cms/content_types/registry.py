from django.core.exceptions import ObjectDoesNotExist


class ContentTypeRegistry:

    content_types = {}
    urlpatterns = []

    def find(self, content_type):
        content_type = self.content_types.get(content_type, None)
        if content_type is None:
            raise ObjectDoesNotExist(f'"{content_type}" does not exist')
        return content_type

    def register(self, extension):

        self.content_types[extension.name] = extension

        urlpatterns = extension.get_urlpatterns()
        if len(urlpatterns) != 0:
            urlpatterns.append(urlpatterns)

    def get_content_types(
        self,
        browsable=None,
        keyword=None,
        requires_project_admin=None,
        format='list'
    ):

        _keyword = None

        if keyword is not None:
            _keyword = str(keyword)
            _keyword = _keyword.strip()

        _content_types = []

        for key in self.content_types.keys():

            add = True
            ct = self.content_types[key]

            if browsable is not None:
                if ct.browsable != browsable:
                    add = False

            if add is True:
                if requires_project_admin is not None:
                    if ct.requires_project_admin != requires_project_admin:
                        add = False

            if add is True:
                if _keyword is not None:
                    if ct.name.startswith(_keyword) is False:
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
