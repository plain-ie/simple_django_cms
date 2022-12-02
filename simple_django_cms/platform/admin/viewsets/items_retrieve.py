from ....conf import settings

from ..permissions.access_mixins import ProjectTenantAccessRequiredMixin

from .base import BaseViewSet


class ItemsRetrieveViewSet(
    ProjectTenantAccessRequiredMixin,
    BaseViewSet
):

    def get(self, request, project_id, tenant_id, item_id):

        item = self.get_item(item_id)
        ct = self.get_content_type(item.content_type)

        return ct.admin_retrieve(
            self,
            item,
            settings.DEFAULT_LANGUAGE,
            settings.DEFAULT_LANGUAGE,
        )

    def post(self, request, project_id, tenant_id, item_id):

        item = self.get_item(item_id)
        ct = self.get_content_type(item.content_type)

        return ct.admin_update(
            self,
            item,
            settings.DEFAULT_LANGUAGE,
            settings.DEFAULT_LANGUAGE,
        )
