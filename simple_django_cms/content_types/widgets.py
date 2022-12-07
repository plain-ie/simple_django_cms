from django.forms.widgets import Input

from ..conf import settings


class FileURLDisplayWidget(Input):

    input_type = 'text'
    template_name = f'{settings.APP_NAME}/platform/admin/components/widgets/file_url_display.html'


class ItemRelationParentWidget(Input):

    input_type = 'text'
    template_name = f'{settings.APP_NAME}/platform/admin/components/widgets/relation_parent.html'
