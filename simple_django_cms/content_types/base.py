from django.forms.models import model_to_dict
from django.shortcuts import reverse

from .. import constants
from ..conf import settings
from ..models import Item, ItemRelation, TranslatableContent


class BaseContentType:

    browsable = False
    name = 'base'
    display_name_plural = 'base'
    display_name_singular = 'base'

    # --

    def matches(self, object):
        return object.content_type == self.name

    # --

    def get_edit_url(self, object):        
        return reverse(
            constants.URLNAME_ADMIN_RETRIEVE_ITEMS,
            kwargs={
                'project_id': str(object.project_id),
                'tenant_id': str(object.tenant_id),
                'item_id': str(object.id)
            }
        )

    def get_site_url(self, object, translatable_content):
        return '#'

    # --

    def get_title(
        self,
        object,
        translatable_content
    ):

        return translatable_content.title

    def get_content_type(
        self,
        language=settings.DEFAULT_LANGUAGE
    ):

        return self.display_name_singular

    # --

    def get_display_content(
        self,
        translatable_contents,
        requested_language,
        default_language=settings.DEFAULT_LANGUAGE
    ):

        requested_content = None
        default_content = None

        for translatable_content in translatable_contents:
            if translatable_content.language == requested_language:
                requested_content = translatable_content
            if translatable_content.language == default_language:
                default_content = translatable_content

        if requested_language == default_language:
            return default_content

        if requested_content is not None:
            return requested_content

        return default_content

    # --

    def get_rendered_form(
        self,
        data=None,
        inital_data=None,
        language=settings.DEFAULT_LANGUAGE
    ):

        return 'HELLO WORLD'

    # --

    def serialize(
        self,
        object,
        language=settings.DEFAULT_LANGUAGE,
    ):

        translatable_content = self.display_content(
            object.translatable_contents.all(),
            language,
            default_language=settings.DEFAULT_LANGUAGE
        )

        data['display_data'] = {
            'title': self.get_site_url(translatable_content),
            'edit_url': self.get_edit_url(object),
            'url': self.get_site_url(object, translatable_content),
            'content_type': self.get_content_type(language),
            'tenant': object.tenant.name,
            'created_at': object.created_at
        }

        return data
