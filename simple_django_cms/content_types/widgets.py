from django.forms.widgets import Input

from ..conf import settings

from .utils import get_translated_content


class FileURLDisplayWidget(Input):

    input_type = 'text'
    template_name = f'{settings.APP_NAME}/platform/admin/components/widgets/file_url_display.html'


class ItemRelationParentWidget(Input):

    input_type = 'text'
    template_name = f'{settings.APP_NAME}/platform/admin/components/widgets/relation_parent.html'

    def get_context(self, name, value, attrs):

        attrs = self.build_attrs(self.attrs, attrs)
        context = {
            'widget': {
                'name': name,
                'is_hidden': self.is_hidden,
                'required': self.is_required,
                'value': self.format_value(value),
                'attrs': self.build_attrs(self.attrs, attrs),
                'template_name': self.template_name,
            },
        }

        if value is not None:
            id = value.get('id', None)
            if id is not None:
                context['widget']['value'] = id
                attrs['placeholder'] = 'XFD'

        return context
