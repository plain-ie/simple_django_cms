from django.contrib import messages
from django.core.exceptions import PermissionDenied

from .... import constants
from ....clients.internal.content_types import ContentTypeQuerySetClient
from ....clients.internal.projects import ProjectQuerySetClient
from ....clients.internal.tenants import TenantQuerySetClient
from ....conf import settings

from ..permissions.access_mixins import ProjectAccessRequiredMixin
from ..utils import get_management_link_project_items

from .base import BaseViewSet


class ItemsCreateSelectTenantViewSet(
    ProjectAccessRequiredMixin,
    BaseViewSet
):

    page_limit = settings.TENANTS_LIMIT
    page_query_string = 'page'
    keyword_query_string = 'q'
    paginate = True
    page_title = 'Item creation'
    page_subtitle = 'Select tenant'
    template = settings.TEMPLATE_CREATE_ITEM_SELECT_TENANT

    def get(self, request, project_id, content_type):
        return self._render(request, self.template, context=self.get_context())

    def get_context(self):

        user_id = self.request.user.id
        content_type = self.kwargs['content_type']
        project_id = self.kwargs['project_id']
        page = int(self.request.GET.get(self.page_query_string, '1'))
        keyword = self.request.GET.get(self.keyword_query_string, None)

        language = settings.DEFAULT_LANGUAGE
        default_language = settings.DEFAULT_LANGUAGE

        #

        content_type_client = ContentTypeQuerySetClient()
        project_client = ProjectQuerySetClient()
        tenant_client = TenantQuerySetClient()

        project = project_client.get_project(project_id)

        ct = ContentTypeQuerySetClient().get_content_type(content_type)

        if ct.has_tenant is False:
            raise PermissionDenied()

        messages.info(
            self.request,
            f'Creating "{ct.name}" content type for project "{project.name}"'
        )

        #

        tenants = tenant_client.get_tenants(
            project_id,
            user_id,
            page=page,
            keyword=keyword,
            limit=self.page_limit,
            paginate=self.paginate,
            format='choices'
        )

        #
        context = super().get_context()
        context['page']['subtitle'] = self.page_subtitle
        context['results'] = tenants
        context['management_links'] = [
            get_management_link_project_items(
                project_id, language, default_language),
            {
                'href': self._reverse(
                    constants.URLNAME_ADMIN_CREATE_ITEMS_SELECT_CONTENT_TYPE,
                    kwargs={
                        'project_id': project_id
                    }
                ),
                'text': 'Change content type'
            }
        ]

        return context
