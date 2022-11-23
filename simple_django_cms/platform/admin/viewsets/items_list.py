from .base import BaseViewSet


class ItemsListViewSet(BaseViewSet):

    def get(self, request):
        return self._render(request, self.template, context=self.get_context())
