import math

from .... import constants
from ....conf import settings
from ....models import Project

from ..permissions.access_mixins import AuthenticatedUserRequiredMixin

from .base import BaseViewSet


class ProjectsListViewSet(AuthenticatedUserRequiredMixin, BaseViewSet):

    page_limit = 10
    page_query_string = 'page'
    page_title = 'Projects'
    template = settings.TEMPLATE_PROJECTS_LIST

    def get(self, request):

        # Super user can see page if only 1 project exists
        # Everyone else is redirected to project page

        context = self.get_context()

        if context['pagination']['total'] == 1:
            if request.user.is_superuser is False:
                self._redirect(
                    self._reverse(
                        constants.URLNAME_ADMIN_LIST_ITEMS,
                        kwargs={
                            'project_id': context['pagination']['results'][0].id
                        }
                    )
                )

        return self._render(request, self.template, context=context)

    def get_context(self):

        context = super().get_context()

        page = int(self.request.GET.get(self.page_query_string, '1'))

        projects = self.request.user.available_projects()

        total = projects.count()

        skip_from = ((page - 1) * self.page_limit)
        skip_to = skip_from + self.page_limit

        context['pagination'] = {
            'results': projects[skip_from:skip_to],
            'pages': math.ceil(total / self.page_limit),
            'page': page,
            'total': total,
        }

        return context
