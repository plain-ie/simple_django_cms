from django.core.exceptions import PermissionDenied

from .base import BaseViewSet

from .... import constants
from ....clients.internal.content_types import ContentTypeQuerySetClient
from ....clients.internal.items import ItemQuerySetClient
from ....clients.internal.projects import ProjectQuerySetClient
from ....clients.internal.tenants import TenantQuerySetClient
from ....conf import settings

from ..permissions.access_mixins import ProjectAccessRequiredMixin


class ItemsListViewSet(ProjectAccessRequiredMixin, BaseViewSet):

    page_limit = settings.ITEMS_LIMIT
    page_query_string = 'page'
    keyword_query_string = 'q'
    tenant_query_string = 'tenant'
    status_query_string = 'status'
    content_type_query_string = 'content_type'
    page_title = 'Browse items'
    paginate = True
    template = settings.TEMPLATE_PROJECT_ITEMS_LIST

    def get(self, request, project_id):
        return self._render(request, self.template, context=self.get_context())

    def get_context(self):

        user_id = self.request.user.id
        project_id = self.kwargs['project_id']
        request_data = self.request.GET

        page = int(request_data.get(self.page_query_string, '1'))
        keyword = request_data.get(self.keyword_query_string, None)
        tenant = request_data.get(self.tenant_query_string, None)
        status = request_data.get(self.status_query_string, None)
        content_type = request_data.get(self.content_type_query_string, None)

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

        allowed_content_types = list(map(lambda x: x[0], content_types))

        # Check if content_type filter has content_type thats allowed for user
        if content_type not in [None, '', ' ']:
            if content_type not in allowed_content_types:
                raise PermissionDenied('Content type not allowed')

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
            paginate=self.paginate,
            content_type=content_type,
            content_types=allowed_content_types,
            tenant=tenant,
            status=status,
            limit=self.page_limit
        )

        items['results'] = settings.CONTENT_TYPE_REGISTRY.serialize(
            items['results'],
            language=settings.DEFAULT_LANGUAGE,
            default_language=settings.DEFAULT_LANGUAGE,
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
        context['management_links'] = [
            {
                'href': self._reverse(constants.URLNAME_ADMIN_LIST_PROJECTS),
                'text': 'Change project',
            },
            {
                'href': self._reverse(
                    constants.URLNAME_ADMIN_CREATE_ITEMS_SELECT_CONTENT_TYPE,
                    kwargs={
                        'project_id': project_id
                    }
                ),
                'text': 'Create new',
            }
        ]

        return context
