from django.contrib import messages

from ....clients.internal.projects import ProjectQuerySetClient
from ....clients.internal.tenants import TenantQuerySetClient
from ....conf import settings

from ..permissions.access_mixins import ProjectAccessRequiredMixin

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

    def get(self, request, project_id):
        return self._render(request, self.template, context=self.get_context())

    def get_context(self):

        user_id = self.request.user.id
        # tenant_id = self.kwargs['tenant_id']
        project_id = self.kwargs['project_id']
        page = int(self.request.GET.get(self.page_query_string, '1'))
        keyword = self.request.GET.get(self.keyword_query_string, None)

        #

        project_client = ProjectQuerySetClient()
        tenant_client = TenantQuerySetClient()

        project = project_client.get_project(project_id)

        messages.info(
            self.request,
            f'Creating item for project "{project.name}"'
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

        return context
