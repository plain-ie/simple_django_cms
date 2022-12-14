from .base import BaseViewSet

from ....conf import settings

from ..permissions.access_mixins import (
    ProjectTenantAccessRequiredMixin,
    ProjectAdminAccessRequiredMixin,
)


class ItemsDeleteViewSet(
    ProjectTenantAccessRequiredMixin,
    BaseViewSet,
):

    def get(self, request, project_id, tenant_id, item_id):

        item = self.get_item(item_id)
        ct = self.get_content_type(item.content_type)

        return ct.admin_delete(
            self,
            item,
            settings.DEFAULT_LANGUAGE,
            settings.DEFAULT_LANGUAGE,
        )


class ProjectItemsDeleteViewSet(
    ProjectAdminAccessRequiredMixin,
    BaseViewSet,
):

    def get(self, request, project_id, item_id):

        item = self.get_item(item_id)
        ct = self.get_content_type(item.content_type)

        return ct.admin_delete(
            self,
            item,
            settings.DEFAULT_LANGUAGE,
            settings.DEFAULT_LANGUAGE,
        )
