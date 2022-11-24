from .base import BaseViewSet


class ItemsRetrieveViewSet(BaseViewSet):

    def get(self, request, project_id, tenant_id, item_id):
        return self._render(request, self.template, context=self.get_context())

    def post(self, request, project_id, tenant_id, item_id):
        # Update
        return self._render(request, self.template, context=self.get_context())
