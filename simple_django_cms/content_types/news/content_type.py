from ... import constants

from ..content_type import BaseContentType

from .forms import (
    NewsItemForm,
    NewsTranslatableContentForm,
)
from .utils import get_topics_relation_formset


class NewsContentType(BaseContentType):

    browsable = True
    display_name_plural = 'news'
    display_name_singular = 'news'
    has_tenant = True
    name = 'news'
    requires_project_admin = False

    item_form = NewsItemForm
    translatable_contents_form = NewsTranslatableContentForm

    def get_relation_formsets(
        self,
        data,
        files,
        serialized_data,
        language,
        default_language,
    ):

        formsets = []

        initial = serialized_data.get('parents', [])

        initial_topics = list(
            filter(
                lambda x: x['status'] == constants.RELATION_NAME_TOPICS,
                initial
            )
        )

        formsets.append(
            get_topics_relation_formset(
                data,
                files,
                initial=initial_topics,
                prefix='topics-relation-form',
                formset_title='Topics'
            )
        )

        return formsets
