from .base import BaseViewSet

from ....clients.internal.content_types import ContentTypeQuerySetClient
from ....clients.internal.items import ItemQuerySetClient
from ....clients.internal.projects import ProjectQuerySetClient
from ....clients.internal.tenants import TenantQuerySetClient
from ....conf import settings

from ..permissions.access_mixins import ProjectAccessRequiredMixin


class ItemsListViewSet(ProjectAccessRequiredMixin, BaseViewSet):

    page_limit = 10
    page_query_string = 'page'
    keyword_query_string = 'q'
    tenant_query_string = 'tenant'
    status_query_string = 'status'
    content_type_query_string = 'content_type'
    page_title = 'Browse items'
    paginate=True
    template = settings.TEMPLATE_PROJECT_ITEMS_LIST

    def get(self, request, project_id):
        return self._render(request, self.template, context=self.get_context())

    def get_context(self):

        user_id = self.request.user.id
        project_id = self.kwargs['project_id']

        page = int(self.request.GET.get(self.page_query_string, '1'))
        keyword = self.request.GET.get(self.keyword_query_string, None)
        tenant = self.request.GET.get(self.tenant_query_string, None)
        status = self.request.GET.get(self.status_query_string, None)
        content_type = self.request.GET.get(self.content_type_query_string, None)

        #

        item_client = ItemQuerySetClient()
        project_client = ProjectQuerySetClient()
        tenant_client = TenantQuerySetClient()
        content_type_client = ContentTypeQuerySetClient()

        #

        project = project_client.get_project(project_id)

        tenants = tenant_client.get_tenants(
            project_id,
            user_id,
            format='choices'
        )['results']

        content_types = content_type_client.get_content_types(
            project_id,
            user_id,
            format='choices'
        )['results']

        statuses = []

        if content_type is not None:
            # check if type is in tenants choices
            pass

        if tenant is not None:
            # check if tenant is in content_types choices
            pass

        if status is not None:
            # check if status is in statuses choices
            pass

        items = item_client.get_items(
            project_id,
            user_id,
            page=page,
            keyword=keyword,
            paginate=paginate,
            content_type=content_type,
            tenant=tenant,
            status=status,
            limit=self.page_limit
        )

        items['results'] = settings.CONTENT_TYPE_REGISTRY.serialize(
            items['results']
        )

        #
        context = super().get_context()
        context['page']['subtitle'] = project.name
        context['results'] = items
        context['choices'] = {
            'tenants': tenants,
            'content_types': content_types,
            'statuses': statuses
        }

        return context
