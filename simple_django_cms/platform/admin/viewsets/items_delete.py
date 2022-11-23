from .base import BaseViewSet


class ItemsDeleteViewSet(BaseViewSet):

    def post(self, request, project_id, item_id):
        return self._redirect()
