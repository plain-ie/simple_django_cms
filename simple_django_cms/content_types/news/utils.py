from ..forms import formset_factory

from .forms import TopicRelationForm


def get_topics_relation_formset(
    data,
    files,
    initial,
    prefix,
    formset_title=None,
    extra=0,
    form=TopicRelationForm,
):

    factory = formset_factory(
        form,
        extra=extra,
    )

    return factory(
        data,
        files,
        initial=initial,
        prefix=prefix,
        formset_title=formset_title
    )
