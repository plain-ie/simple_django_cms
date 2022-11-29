from django.contrib import messages
from django.forms.models import model_to_dict

from .... import constants

from ....clients.internal.content_types import ContentTypeQuerySetClient
from ....clients.internal.items import ItemQuerySetClient
from ....clients.internal.projects import ProjectQuerySetClient
from ....clients.internal.tenants import TenantQuerySetClient
from ....conf import settings

from ..permissions.access_mixins import ProjectTenantAccessRequiredMixin

from .base import BaseViewSet


class ItemsRetrieveViewSet(
    ProjectTenantAccessRequiredMixin,
    BaseViewSet
):

    page_title = ''
    template = settings.TEMPLATE_CREATE_RETRIEVE

    def get(self, request, project_id, tenant_id, item_id):
        return self._render(request, self.template, context=self.get_context())

    def post(self, request, project_id, tenant_id, item_id):
        # Update
        return self._render(request, self.template, context=self.get_context())

    def get_context(self):

        tenant_id = self.kwargs['tenant_id']
        project_id = self.kwargs['project_id']
        item_id = self.kwargs['item_id']
        language = settings.DEFAULT_LANGUAGE

        #

        project_client = ProjectQuerySetClient()
        tenant_client = TenantQuerySetClient()
        content_type_client = ContentTypeQuerySetClient()
        items_client = ItemQuerySetClient()

        item = items_client.get_item(item_id)

        _project = project_client.get_project(project_id)
        _tenant = tenant_client.get_tenant(tenant_id)
        _ct = content_type_client.get_content_type(item.content_type)


        data = model_to_dict(item)
        data['translatable_contents'] = []

        for translatable_content in item.translatable_contents.all():
            data['translatable_contents'].append(model_to_dict(translatable_content))

        for relation in item.parents.all():
            data['relations'].append(model_to_dict(relation))

        form = _ct.get_rendered_form(
            initial=data,
            language=language
        )

        #

        if item.published is False:
            messages.warning(self.request, 'This item is unpublished')

        #

        context = super().get_context()
        context['page']['title'] = _ct.get_content_type(language)
        context['page']['subtitle'] = _tenant.name + ' @ ' + _project.name
        context['form'] = form
        context['item'] = item

        return context
