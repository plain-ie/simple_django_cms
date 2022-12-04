from django.contrib import messages

from .... import constants
from ....clients.internal.content_types import ContentTypeQuerySetClient
from ....clients.internal.projects import ProjectQuerySetClient
from ....conf import settings

from ..permissions.access_mixins import ProjectAccessRequiredMixin
from ..utils import get_management_link_project_items

from .base import BaseViewSet


class ItemsCreateSelectContentTypeViewSet(
    ProjectAccessRequiredMixin,
    BaseViewSet
):

    page_limit = settings.ITEMS_LIMIT
    page_query_string = 'page'
    keyword_query_string = 'q'
    paginate = True
    page_title = 'Item creation'
    page_subtitle = 'Select content type'
    template = settings.TEMPLATE_CREATE_ITEM_SELECT_CONTENT_TYPE

    def get(self, request, project_id):
        return self._render(request, self.template, context=self.get_context())

    def get_context(self):

        user_id = self.request.user.id
        project_id = self.kwargs['project_id']
        page = int(self.request.GET.get(self.page_query_string, '1'))
        keyword = self.request.GET.get(self.keyword_query_string, None)

        language = settings.DEFAULT_LANGUAGE
        default_language = settings.DEFAULT_LANGUAGE

        #

        content_type_client = ContentTypeQuerySetClient()
        project_client = ProjectQuerySetClient()

        project = project_client.get_project(project_id)

        messages.info(
            self.request,
            f'Creating item for project "{project.name}"'
        )

        #

        content_types = content_type_client.get_content_types(
            project_id,
            user_id,
            page=page,
            keyword=keyword,
            limit=self.page_limit,
            paginate=self.paginate,
            format='list'
        )

        content_types_data = []

        for content_type in content_types['results']:

            href = '#'
            text = content_type.get_display_name_plural(
                language, default_language)

            if content_type.has_tenant is False:
                href = self._reverse(
                    constants.URLNAME_ADMIN_CREATE_PROJECT_ITEMS,
                    kwargs={
                        'project_id': project_id,
                        'content_type': content_type.name
                    }
                )
            else:
                href = self._reverse(
                    constants.URLNAME_ADMIN_CREATE_ITEMS_SELECT_TENANT,
                    kwargs={
                        'project_id': project_id,
                        'content_type': content_type.name
                    }
                )

            content_types_data.append({
                'href': href,
                'text': text,
            })

        content_types['results'] = content_types_data

        #
        context = super().get_context()
        context['page']['subtitle'] = self.page_subtitle
        context['results'] = content_types
        context['management_links'] = [
            get_management_link_project_items(
                project_id, language, default_language),
        ]

        return context
