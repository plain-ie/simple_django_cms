import math

from .... import constants
from ....clients.internal.projects import ProjectQuerySetClient
from ....conf import settings

from ..permissions.access_mixins import AuthenticatedUserRequiredMixin

from .base import BaseViewSet


class ProjectsListViewSet(AuthenticatedUserRequiredMixin, BaseViewSet):

    page_limit = settings.PROJECTS_LIMIT
    page_query_string = 'page'
    page_title = 'Projects'
    paginate = True
    template = settings.TEMPLATE_PROJECTS_LIST

    def get(self, request):

        # context = self.get_context()
        #
        # if context['results']['total'] == 1:
        #     first = context['results']['results'][0]
        #     return self._redirect(first.get_admin_items_url())

        return self._render(request, self.template, context=self.get_context())

    def get_context(self):

        #
        user_id = self.request.user.id
        page = int(self.request.GET.get(self.page_query_string, '1'))
        keyword = self.request.GET.get('keyword', None)

        #
        results = ProjectQuerySetClient().get_projects(
            user_id,
            page=page,
            limit=self.page_limit,
            paginate=self.paginate,
            name=keyword
        )

        #
        context = super().get_context()
        context['results'] = results

        #
        return context
