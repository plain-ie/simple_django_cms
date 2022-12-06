from django.forms.widgets import Input

from ..conf import settings


class FileURLDisplayWidget(Input):

    input_type = 'text'
    template_name = f'{settings.APP_NAME}/platform/admin/components/fields/file_url_display.html'
