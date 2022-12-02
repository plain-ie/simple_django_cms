from django.contrib import messages
from django.shortcuts import render, redirect

from ..conf import settings

from .serializers import ItemSerializer


class BaseContentType:

    browsable = False
    display_name_plural = 'base'
    display_name_singular = 'base'
    has_tenant = False
    name = 'base'
    requires_project_admin = False
    serializer_class = ItemSerializer
    template_admin_create = settings.TEMPLATE_CREATE_ITEM
    template_admin_retrieve = settings.TEMPLATE_RETRIEVE_ITEM

    # --

    def get_urlpatterns(self):
        return []

    def matches(self, object):
        return object.content_type == self.name

    # --

    def serialize(self, object, language, default_language):
        serializer = self.serializer_class.from_orm(object)
        display_data = serializer.get_display_data(language, default_language)
        data = display_data.dict()
        data['serializer'] = serializer
        return data

    # --

    def admin_create(
        self,
        view,
        language,
        default_language,
    ):

        serialized_data = self.serialize(object, language, default_language)

        context = {
            'forms': {
                'item': None,
                'item_data': None,
                'translatable_contents': None,
                'relations': None
            },
            'item': object,
            'management_links': [
                {'href': '#', 'text': 'Browse all items'},
                {'href': '#', 'text': 'Create new'},
                {'href': '#', 'text': 'Publish'},
            ],
            'page': {
                'title': 'Item creation',
                'subtitle': serialized_data['content_type'],
            },
            'view': view,
        }

        messages.info(
            view.request,
            'Creating item for project "x" tenant "y"'
        )

        return render(
            request,
            self.template_admin_create,
            context=context
        )

    def admin_retrieve(
        self,
        view,
        object,
        language,
        default_language,
    ):

        serialized_data = self.serialize(object, language, default_language)

        # initial = serialized_data['serializer'].dict()

        context = {
            'forms': {
                'item': None,
                'item_data': None,
                'translatable_contents': None,
                'relations': None
            },
            'item': object,
            'management_links': [
                {'href': '#', 'text': 'Browse all items'},
                {'href': '#', 'text': 'Create new'},
                {'href': '#', 'text': 'Publish'},
            ],
            'page': {
                'title': serialized_data['title'],
                'subtitle': serialized_data['content_type'],
            },
            'view': view,
        }

        if serialized_data['published'] is True:
            messages.success(
                view.request,
                'This item is published'
            )
        else:
            messages.warning(
                view.request,
                'This item is unpublished'
            )

        return render(
            view.request,
            self.template_admin_retrieve,
            context=context
        )

    def admin_update(
        self,
        view,
        object,
        language,
        default_language,
    ):

        return self.admin_retrieve(view, object, language, default_language)

    def admin_delete(
        self,
        view,
        object,
        language,
        default_language,
    ):

        return redirect('#')
