from .base import BaseViewSet


class ItemsCreateViewSet(BaseViewSet):

    def get(self, request, project_id, content_type):
        # Form
        return self._render(request, self.template, context=self.get_context())

    def post(self, request, project_id, content_type):
        # Create
        return self._redirect()
