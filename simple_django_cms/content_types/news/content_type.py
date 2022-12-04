from ..content_type import BaseContentType

from .forms import NewsItemForm, NewsTranslatableContentForm


class NewsContentType(BaseContentType):

    browsable = True
    display_name_plural = 'news'
    display_name_singular = 'news'
    has_tenant = True
    name = 'news'
    requires_project_admin = False

    item_form = NewsItemForm
    translatable_contents_form = NewsTranslatableContentForm
