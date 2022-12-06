import datetime

from django.forms import formset_factory
from django.shortcuts import render, redirect, reverse

from .. import constants
from ..conf import settings
from ..clients.internal.files import FileClient
from ..clients.internal.items import ItemQuerySetClient
from ..clients.internal.projects import ProjectQuerySetClient
from ..clients.internal.tenants import TenantQuerySetClient
from ..platform.admin.utils import (
    create_message,
    get_item_admin_url,
    get_management_link_create_item_previous,
    get_management_link_delete_item,
    get_management_link_new_item,
    get_management_link_project_items,
    get_management_link_toggle_publish_item,
    get_project_items_url,
)

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

    item_form = None
    item_data_form = None
    translatable_contents_form = None

    # --
    # Forms

    def get_item_form(
        self,
        data,
        files,
        serialized_data,
    ):

        if self.item_form is None:
            return None

        return self.item_form(
            data,
            files,
            initial=serialized_data
        )

    def get_item_data_form(
        self,
        data,
        files,
        serialized_data,
    ):

        if self.item_data_form is None:
            return None

        return self.item_data_form(
            data,
            files,
            initial=serialized_data['data']
        )

    def get_translatable_contents_form_formset(
        self,
        data,
        files,
        serialized_data,
    ):

        if self.translatable_contents_form is None:
            return None

        formset = formset_factory(
            self.translatable_contents_form,
            extra=0,
        )

        initial = serialized_data.get('data', {})
        initial = initial.get('translatable_contents', [])

        return formset(
            data,
            files,
            initial=initial,
            prefix='translatable-contents-form'
        )

    # --

    def get_display_name_plural(self, language, default_language):
        return self.display_name_plural

    def get_display_name_singular(self, language, default_language):
        return self.display_name_singular

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
        data['content_type'] = self.get_display_name_singular(
            language,
            default_language
        )

        return data

    # --
    # Retrieve & create & update

    def admin_retrieve_create_update(
        self,
        view,
        object,
        language,
        default_language,
    ):

        # --

        errors = []
        initial = None
        request_method = view.request.method
        request_data = None
        request_files = None
        in_memory_file_class = 'InMemoryUploadedFile'
        temp_uploaded_file_class = 'TemporaryUploadedFile'
        upload_file_classes = [
            in_memory_file_class,
            temp_uploaded_file_class
        ]

        if request_method == 'POST':
            request_data = view.request.POST
            request_files = view.request.FILES

        project_id = view.kwargs['project_id']
        tenant_id = view.kwargs.get('tenant_id', None)
        content_type = str(self.name)

        # --

        projects_client = ProjectQuerySetClient()
        tenants_client = TenantQuerySetClient()
        files_client = FileClient()

        # --
        # Context data

        browse_items_link = get_management_link_project_items(
            project_id,
            language,
            default_language
        )
        previous_link = get_management_link_create_item_previous(
            project_id,
            content_type,
            language,
            default_language
        )

        if object is None:

            serialized_data = {
                'title': 'Item creation',
                'content_type': self.get_display_name_singular(
                    language,
                    default_language
                ),
            }

            management_links = [
                browse_items_link,
                previous_link,
            ]

            initial = {
                'content_type': self.name,
                'data': {
                    'translatable_contents': [
                        {
                            'language': default_language,
                        }
                    ]
                }
            }

            button_text = 'Create'

        else:

            tenant_id = object.tenant_id

            new_item_link = get_management_link_new_item(
                project_id,
                tenant_id,
                self.name,
                language,
                default_language
            )

            delete_item_link = get_management_link_delete_item(
                project_id,
                tenant_id,
                object.id,
                language,
                default_language
            )

            toggle_publish_item_link = get_management_link_toggle_publish_item(
                project_id,
                tenant_id,
                object.id,
                object.published,
                language,
                default_language
            )

            serialized_data = self.serialize(
                object,
                language,
                default_language
            )

            initial = serialized_data['serializer'].dict()

            management_links = [
                browse_items_link,
                new_item_link,
                toggle_publish_item_link,
                delete_item_link,
            ]

            button_text = 'Update'


        # --
        # Forms

        item_form = self.get_item_form(
            request_data,
            request_files,
            initial
        )
        item_data_form = self.get_item_data_form(
            request_data,
            request_files,
            initial
        )
        translatable_contents_formset = self.get_translatable_contents_form_formset(
            request_data,
            request_files,
            initial
        )

        # --
        # Validate forms if request is POST

        if request_method == 'POST':

            if item_form is not None:
                if item_form.is_valid() is False:
                    errors += item_form.errors

            if item_data_form is not None:
                if item_data_form.is_valid() is False:
                    errors += item_data_form.errors

            if translatable_contents_formset is not None:
                for content_form in translatable_contents_formset:
                    if content_form.is_valid() is False:
                        errors += content_form.errors

            if len(errors) == 0:

                item_data = {}
                relations_data = []
                files_to_upload = {}
                files_to_remove = []

                if item_form is not None:
                    item_data = dict(item_form.cleaned_data)

                item_data['project_id'] = project_id
                item_data['content_type'] = content_type
                item_data['tenant_id'] = tenant_id
                item_data['data'] = {}

                if item_data_form is not None:
                    item_data['data'] = dict(item_data_form.cleaned_data)

                    # --
                    # Capture files to handle

                    for key in item_data['data'].keys():

                        value = item_data['data'][key]

                        _url = item_data['data'].get(f'{key}_url', None)
                        if _url is None:
                            _url = ''

                        if type(value).__name__ in upload_file_classes:

                            new_file_name = files_client.get_file_path(
                                project_id,
                                tenant_id,
                                value.name
                            )

                            #
                            # Check if file can be replaced:
                            # - If file extension is the same, file can be
                            # overwritten with new file
                            # - Remove file that is not being overwritten
                            #

                            if files_client.extensions_match(
                                new_file_name,
                                _url
                            ) is True:
                                new_file_name = _url
                            else:
                                files_to_remove.append(_url)

                            files_to_upload[new_file_name] = value
                            item_data['data'][key] = new_file_name

                if translatable_contents_formset is not None:
                    item_data['data']['translatable_contents'] = translatable_contents_formset.cleaned_data

                    # --
                    # Capture files to handle

                    for content in item_data['data']['translatable_contents']:
                        for key in content.keys():

                            value = content[key]

                            _url = content.get(f'{key}_url', None)
                            if _url is None:
                                _url = ''

                            if type(value).__name__ in upload_file_classes:

                                new_file_name = files_client.get_file_path(
                                    project_id,
                                    tenant_id,
                                    value.name
                                )

                                #
                                # Check if file can be replaced:
                                # - If file extension is the same, file can be
                                # overwritten with new file
                                # - Remove file that is not being overwritten
                                #

                                if files_client.extensions_match(
                                    new_file_name,
                                    _url
                                ) is True:
                                    new_file_name = _url
                                else:
                                    files_to_remove.append(_url)

                                files_to_upload[new_file_name] = value
                                content[f'{key}_url'] = new_file_name
                                content[key] = new_file_name

                # --
                # Handle item

                if object is None:

                    item = ItemQuerySetClient().create(
                        item_data,
                        relations_data
                    )

                    create_message(
                        'success',
                        view.request,
                        'Item created successfully'
                    )

                else:

                    item = ItemQuerySetClient().update(
                        object.id,
                        item_data,
                        relations_data
                    )

                    create_message(
                        'success',
                        view.request,
                        'Item updated successfully'
                    )

                # --
                # Handle files

                for key in files_to_upload.keys():
                    files_client.upload(key, files_to_upload[key])

                for path in files_to_remove:
                    files_client.remove(path)

                # --

                return redirect(
                    get_item_admin_url(
                        item.project_id,
                        item.tenant_id,
                        item.content_type,
                        item.id
                    )
                )

        # --
        # Context

        context = {
            'button_text': button_text,
            'errors': [],
            'forms': {
                'item': item_form,
                'item_data': item_data_form,
            },
            'formsets': {
                'translatable_contents': translatable_contents_formset,
                'relations': []
            },
            'item': object,
            'management_links': management_links,
            'page': {
                'title': serialized_data['title'],
                'subtitle': serialized_data['content_type'],
            },
            'view': view,
        }

        # --
        # Messages

        project = projects_client.get_project(project_id)
        tenant = None

        if tenant_id is not None:
            tenant = tenants_client.get_tenant(tenant_id)

        if object is not None:

            if serialized_data['published'] is False:
                create_message(
                    'warning',
                    view.request,
                    'This item is unpublished'
                )

        else:

            msg = f'Creating item "{content_type}" '
            msg += f'for project "{project.name}"'

            if tenant is not None:
                msg += f' tenant "{tenant.name}"'

            create_message('info', view.request, msg)

        # --

        return render(
            view.request,
            self.template_admin_retrieve,
            context=context
        )

    # --
    # Delete

    def admin_delete(
        self,
        view,
        object,
        language,
        default_language,
    ):

        # --

        project_id = view.kwargs['project_id']

        # --

        serialized_data = self.serialize(object, language, default_language)

        # --

        object.delete()

        # --

        msg = f'Content type "{serialized_data["content_type"]}" item '
        msg += f'"{serialized_data["title"]}" was deleted!'

        create_message('success', view.request, msg)

        # --

        return redirect(get_project_items_url(project_id))

    # --
    # Toggle published

    def admin_toggle_publish(
        self,
        view,
        object,
        language,
        default_language,
    ):

        published = object.published
        published_at = object.published_at

        new_published_state = not published

        object.published = new_published_state

        if new_published_state == True and published_at is None:
            object.published_at = datetime.datetime.now(datetime.timezone.utc)

        object.save()

        # --

        msg = f'Item published state was changed'

        create_message('success', view.request, msg)

        # --

        return redirect(
            get_item_admin_url(
                object.project_id,
                object.tenant_id,
                object.content_type,
                object.id
            )
        )
