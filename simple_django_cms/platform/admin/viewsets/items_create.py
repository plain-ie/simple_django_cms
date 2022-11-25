from django.contrib import messages

from .... import constants

from ....clients.internal.content_types import ContentTypeQuerySetClient
from ....clients.internal.projects import ProjectQuerySetClient
from ....clients.internal.tenants import TenantQuerySetClient
from ....conf import settings

from ..permissions.access_mixins import ProjectTenantAccessRequiredMixin

from .base import BaseViewSet


class ItemsCreateViewSet(
    ProjectTenantAccessRequiredMixin,
    BaseViewSet
):

    page_title = 'Item creation'
    template = settings.TEMPLATE_CREATE_ITEM

    def get(self, request, project_id, tenant_id, content_type):
        # Form
        return self._render(request, self.template, context=self.get_context())

    def post(self, request, project_id, content_type):

        content_type_client = ContentTypeQuerySetClient()
        _ct = content_type_client.get_content_type(content_type)

        #

        try:
            item = _ct.create(project_id, tenant_id, request.user, request.POST)
        except Exception:
            return self._render(request, self.template, context=self.get_context())

        #

        messages.success(
            request,
            'Item created successfully'
        )

        redirect_to = self._reverse(
            constants.URLNAME_ADMIN_RETRIEVE_ITEMS,
            kwargs={
                'project_id': project_id,
                'tenant_id': tenant_id,
                'item_id': item.id
            }
        )

        return self._redirect(redirect_to)

    def get_context(self):

        tenant_id = self.kwargs['tenant_id']
        project_id = self.kwargs['project_id']
        content_type = self.kwargs['content_type']
        language = settings.DEFAULT_LANGUAGE

        #

        project_client = ProjectQuerySetClient()
        tenant_client = TenantQuerySetClient()
        content_type_client = ContentTypeQuerySetClient()

        _project = project_client.get_project(project_id)
        _tenant = tenant_client.get_tenant(tenant_id)
        _ct = content_type_client.get_content_type(content_type)

        form = _ct.get_rendered_form(
            initial_data={
                'translatable_contents': [{
                    'language': settings.DEFAULT_LANGUAGE
                }]
            },
            language=language
        )

        #

        msg = f'Creating "{_ct.get_content_type(language)}" '
        msg += f'for project "{_project.name}" '
        msg += f'tenant "{_tenant.name}"'

        messages.info(self.request, msg)

        #

        context = super().get_context()
        context['page']['subtitle'] = _ct.get_content_type(language)
        context['form'] = form

        return context
