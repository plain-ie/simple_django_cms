from .base import BaseViewSet


class ItemsCreateSelectContentTypeViewSet(BaseViewSet):

    def get(self, request, project_id, tenant_id):
        return self._render(request, self.template, context=self.get_context())
