from .base import BaseViewSet

from ....conf import settings

from ..permissions.access_mixins import (
    ProjectTenantAccessRequiredMixin,
    ProjectAdminAccessRequiredMixin,
)


class ItemsTogglePublishViewSet(
    ProjectTenantAccessRequiredMixin,
    BaseViewSet,
):

    def get(self, request, project_id, tenant_id, item_id):

        item = self.get_item(item_id)
        ct = self.get_content_type(item.content_type)

        return ct.admin_toggle_publish(
            self,
            item,
            settings.DEFAULT_LANGUAGE,
            settings.DEFAULT_LANGUAGE,
        )


class ProjectItemsTogglePublishViewSet(BaseViewSet):

    def get(self, request, project_id, item_id):

        item = self.get_item(item_id)
        ct = self.get_content_type(item.content_type)

        return ct.admin_toggle_publish(
            self,
            item,
            settings.DEFAULT_LANGUAGE,
            settings.DEFAULT_LANGUAGE,
        )
