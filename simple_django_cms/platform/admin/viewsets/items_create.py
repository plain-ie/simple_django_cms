from django.contrib import messages
from django.core.exceptions import PermissionDenied

from .... import constants

from ....clients.internal.content_types import ContentTypeQuerySetClient
from ....conf import settings

from ..permissions.access_mixins import (
    ProjectTenantAccessRequiredMixin,
    ProjectAdminAccessRequiredMixin,
)

from .base import BaseViewSet


class ItemsCreateViewSet(
    ProjectTenantAccessRequiredMixin,
    BaseViewSet
):

    def get(self, request, project_id, tenant_id, content_type):

        ct = self.get_content_type(content_type)

        language = settings.DEFAULT_LANGUAGE
        default_language = settings.DEFAULT_LANGUAGE

        if ct.has_tenant is False:
            raise PermissionDenied()

        return ct.admin_retrieve_create_update(
            self,
            None,
            language,
            default_language,
        )

    def post(self, request, project_id, tenant_id, content_type):

        ct = self.get_content_type(content_type)

        language = settings.DEFAULT_LANGUAGE
        default_language = settings.DEFAULT_LANGUAGE

        if ct.has_tenant is False:
            raise PermissionDenied()

        return ct.admin_retrieve_create_update(
            self,
            None,
            language,
            default_language,
        )



class ProjectItemsCreateViewSet(
    ProjectAdminAccessRequiredMixin,
    BaseViewSet
):

    def get(self, request, project_id, content_type):

        ct = self.get_content_type(content_type)

        language = settings.DEFAULT_LANGUAGE
        default_language = settings.DEFAULT_LANGUAGE

        if ct.has_tenant is True:
            raise PermissionDenied('Requires tenant_id')

        return ct.admin_retrieve_create_update(
            self,
            None,
            language,
            default_language,
        )

    def post(self, request, project_id, content_type):

        ct = self.get_content_type(content_type)

        language = settings.DEFAULT_LANGUAGE
        default_language = settings.DEFAULT_LANGUAGE

        if ct.has_tenant is True:
            raise PermissionDenied('Requires tenant_id')

        return ct.admin_retrieve_create_update(
            self,
            None,
            language,
            default_language,
        )
