from django.shortcuts import reverse
from django.template.loader import render_to_string
from django.utils.text import slugify

from .. import constants
from ..clients.internal.items import ItemQuerySetClient
from ..conf import settings
from ..models import Item, ItemRelation, TranslatableContent


class BaseContentType:

    browsable = False
    #
    name = 'base'
    display_name_plural = 'base'
    display_name_singular = 'base'
    #
    form_template = 'simple_django_cms/platform/admin/forms/content_type.html'
    #
    item_form = None
    item_data_form = None
    translatable_contents_form = None
    translatable_contents_data_form = None
    relations_form = None

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

    def get_translatable_contents_form(
        self,
        data=None,
        initial=[],
        language=settings.DEFAULT_LANGUAGE
    ):

        if self.translatable_contents_form is None:
            return None

        return self.translatable_contents_form(data, initial=initial)

    def get_relations_form(
        self,
        data=None,
        initial=[],
        language=settings.DEFAULT_LANGUAGE
    ):

        if self.relations_form is None:
            return None

        return self.relations_form(data, initial=initial)

    def get_item_form(
        self,
        data=None,
        initial={},
        language=settings.DEFAULT_LANGUAGE
    ):

        if self.item_form is None:
            return None

        return self.item_form(data, initial=initial)

    def get_item_data_form(
        self,
        data=None,
        initial={},
        language=settings.DEFAULT_LANGUAGE
    ):

        if self.item_data_form is None:
            return None

        return self.item_data_form(data, initial=initial)

    def get_rendered_form(
        self,
        data=None,
        initial={},
        language=settings.DEFAULT_LANGUAGE,
        validate=False,
        render_html=True,
    ):

        is_valid = True
        errors = {
            'translatable_contents_form': [],
            'translatable_contents_data_form': [],
            'relations_form': [],
            'item_form': [],
            'item_data_form': [],
        }

        translatable_contents_form = self.get_translatable_contents_form(
            data=data,
            initial=initial.get('translatable_contents', []),
            language=language
        )

        relations_form = self.get_relations_form(
            data=data,
            initial=initial.get('relations', []),
            language=language
        )

        item_form = self.get_item_form(
            data=data,
            initial=initial,
            language=language
        )

        item_data_form = self.get_item_data_form(
            data=data,
            initial=initial.get('data', {}),
            language=language
        )

        if validate is True:

            if translatable_contents_form is not None:
                for form in translatable_contents_form.forms:
                    if form.is_valid() is False:
                        is_valid = False
                        errors['translatable_contents_form'].append(form.errors)

            if relations_form is not None:
                for form in relations_form.forms:
                    if form.is_valid() is False:
                        is_valid = False
                        errors['relations_form'].append(form.errors)

            if item_form is not None:
                if item_form.is_valid() is False:
                    is_valid = False
                    errors['item_form'] = item_form.errors

            if item_data_form is not None:
                if item_data_form.is_valid() is False:
                    is_valid = False
                    errors['item_data_form'] = item_data_form.errors


        context = {
            'errors': errors,
            'is_valid': is_valid,
            'translatable_contents_form': translatable_contents_form,
            'relations_form': relations_form,
            'item_form': item_form,
            'item_data_form': item_data_form,
        }

        if render_html is False:
            return context

        html = render_to_string(
            self.form_template,
            context=context
        )

        return html

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

    # --

    def create_slug(self, translatable_content):
        return slugify(translatable_content['title'])

    # --

    def create(
        self,
        project_id=None,
        tenant_id=None,
        user_id=None,
        validated_data=None,
    ):

        item = validated_data['item']
        item['data'] = validated_data['item_data']

        translatable_contents = validated_data['translatable_contents']
        for translatable_content in translatable_contents:
            translatable_content['slug'] = self.create_slug(translatable_content)

        item = ItemQuerySetClient().create(
            project_id=project_id,
            tenant_id=tenant_id,
            user_id=user_id,
            item_data=item,
            translatable_contents_data=validated_data['translatable_contents'],
            relations_data=validated_data['relations']
        )

        return item

    def update(self, object, data, **kwargs):
        raise NotImplemented()

    def partial_update(self, object, data, **kwargs):
        raise NotImplemented()

    def delete(self, object, **kwargs):
        raise NotImplemented()
