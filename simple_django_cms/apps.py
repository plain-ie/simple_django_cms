from django.apps import AppConfig


class SimpleDjangoCmsConfig(AppConfig):

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'simple_django_cms'

    def ready(self):

        from .conf import settings

        # ---------------------------------------------------------------------
        # Set content type registry
        # ---------------------------------------------------------------------

        from .extensions.content_types.registry import ContentTypeRegistry

        settings._CONTENT_TYPE_REGISTRY = ContentTypeRegistry()

        from .extensions.content_types.flat_pages.content_type import FlatPageContentType
        from .extensions.content_types.images.content_type import ImageContentType
        from .extensions.content_types.news.content_type import NewsContentType
        from .extensions.content_types.redirects.content_type import RedirectContentType
        from .extensions.content_types.topics.content_type import TopicContentType

        settings._CONTENT_TYPE_REGISTRY.register(FlatPageContentType())
        settings._CONTENT_TYPE_REGISTRY.register(ImageContentType())
        settings._CONTENT_TYPE_REGISTRY.register(NewsContentType())
        settings._CONTENT_TYPE_REGISTRY.register(RedirectContentType())
        settings._CONTENT_TYPE_REGISTRY.register(TopicContentType())

        # ---------------------------------------------------------------------
        # Set markdown widget registry
        # ---------------------------------------------------------------------

        from .extensions.markdown.registry import MarkdownWidgetRegistry

        settings._MARKDOWN_WIDGET_REGISTRY = MarkdownWidgetRegistry()

        from .extensions.markdown.widgets import HeadingH1
        from .extensions.markdown.widgets import HeadingH2
        from .extensions.markdown.widgets import HeadingH3
        from .extensions.markdown.widgets import HeadingH4
        from .extensions.markdown.widgets import HorizontalRule
        from .extensions.markdown.widgets import Image
        from .extensions.markdown.widgets import UnorderedListElement
        from .extensions.markdown.widgets import OrderedListElement
        from .extensions.markdown.widgets import Paragraph
        from .extensions.markdown.widgets import SimpleLink

        settings._MARKDOWN_WIDGET_REGISTRY.register(HeadingH1)
        settings._MARKDOWN_WIDGET_REGISTRY.register(HeadingH2)
        settings._MARKDOWN_WIDGET_REGISTRY.register(HeadingH3)
        settings._MARKDOWN_WIDGET_REGISTRY.register(HeadingH4)
        settings._MARKDOWN_WIDGET_REGISTRY.register(HorizontalRule)
        settings._MARKDOWN_WIDGET_REGISTRY.register(Image)
        settings._MARKDOWN_WIDGET_REGISTRY.register(UnorderedListElement)
        settings._MARKDOWN_WIDGET_REGISTRY.register(OrderedListElement)
        settings._MARKDOWN_WIDGET_REGISTRY.register(Paragraph)
        settings._MARKDOWN_WIDGET_REGISTRY.register(SimpleLink)

        # ---------------------------------------------------------------------
        # Set translations registry
        # ---------------------------------------------------------------------

        settings._TRANSLATION_REGISTRY = None
