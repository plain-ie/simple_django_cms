from django.contrib import messages

from .base import BaseViewSet

from ....clients.internal.content_types import ContentTypeQuerySetClient
from ....clients.internal.projects import ProjectQuerySetClient
from ....clients.internal.tenants import TenantQuerySetClient
from ....conf import settings


class ItemsCreateSelectContentTypeViewSet(BaseViewSet):

    page_limit = settings.ITEMS_LIMIT
    page_query_string = 'page'
    keyword_query_string = 'q'
    paginate = True
    page_title = 'Item creation'
    page_subtitle = 'Select content type'
    template = settings.TEMPLATE_CREATE_ITEM_SELECT_CONTENT_TYPE

    def get(self, request, project_id, tenant_id):
        return self._render(request, self.template, context=self.get_context())

    def get_context(self):

        user_id = self.request.user.id
        tenant_id = self.kwargs['tenant_id']
        project_id = self.kwargs['project_id']
        page = int(self.request.GET.get(self.page_query_string, '1'))
        keyword = self.request.GET.get(self.keyword_query_string, None)

        #

        content_type_client = ContentTypeQuerySetClient()
        project_client = ProjectQuerySetClient()
        tenant_client = TenantQuerySetClient()

        project = project_client.get_project(project_id)
        tenant = tenant_client.get_tenant(tenant_id)

        messages.success(
            self.request,
            f'Creating item for project "{project.name}" tenant "{tenant.name}"'
        )

        #

        content_types = content_type_client.get_content_types(
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
        context['results'] = content_types

        return context
