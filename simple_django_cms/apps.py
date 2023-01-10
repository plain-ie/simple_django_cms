from django.apps import AppConfig


class SimpleDjangoCmsConfig(AppConfig):

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'simple_django_cms'

    def ready(self):

        import os

        from django.conf import settings as dj_settings

        from .conf import settings

        # ---------------------------------------------------------------------
        # Set file handling backend
        # ---------------------------------------------------------------------

        from .file_handling.local import LocalFileStorageBackend

        settings._FILE_HANDLING_BACKEND = LocalFileStorageBackend()


        # ---------------------------------------------------------------------
        # Set content type registry
        # ---------------------------------------------------------------------

        from .content_types.registry import ContentTypeRegistry

        settings._CONTENT_TYPE_REGISTRY = ContentTypeRegistry()

        from .content_types.flat_pages.content_type import FlatPageContentType
        from .content_types.images.content_type import ImageContentType
        from .content_types.news.content_type import NewsContentType
        from .content_types.redirects.content_type import RedirectContentType
        from .content_types.topics.content_type import TopicContentType

        settings.CONTENT_TYPE_REGISTRY.register(FlatPageContentType())
        settings.CONTENT_TYPE_REGISTRY.register(ImageContentType())
        settings.CONTENT_TYPE_REGISTRY.register(NewsContentType())
        settings.CONTENT_TYPE_REGISTRY.register(RedirectContentType())
        settings.CONTENT_TYPE_REGISTRY.register(TopicContentType())


        # ---------------------------------------------------------------------
        # Set markdown widget registry
        # ---------------------------------------------------------------------

        from .markdown.registry import MarkdownWidgetRegistry

        settings._MARKDOWN_WIDGET_REGISTRY = MarkdownWidgetRegistry()

        from .markdown.widgets import HeadingH1
        from .markdown.widgets import HeadingH2
        from .markdown.widgets import HeadingH3
        from .markdown.widgets import HeadingH4
        from .markdown.widgets import HorizontalRule
        from .markdown.widgets import Image
        from .markdown.widgets import UnorderedListElement
        from .markdown.widgets import OrderedListElement
        from .markdown.widgets import Paragraph
        from .markdown.widgets import SimpleLink

        settings.MARKDOWN_WIDGET_REGISTRY.register(HeadingH1)
        settings.MARKDOWN_WIDGET_REGISTRY.register(HeadingH2)
        settings.MARKDOWN_WIDGET_REGISTRY.register(HeadingH3)
        settings.MARKDOWN_WIDGET_REGISTRY.register(HeadingH4)
        settings.MARKDOWN_WIDGET_REGISTRY.register(HorizontalRule)
        settings.MARKDOWN_WIDGET_REGISTRY.register(Image)
        settings.MARKDOWN_WIDGET_REGISTRY.register(UnorderedListElement)
        settings.MARKDOWN_WIDGET_REGISTRY.register(OrderedListElement)
        settings.MARKDOWN_WIDGET_REGISTRY.register(Paragraph)
        settings.MARKDOWN_WIDGET_REGISTRY.register(SimpleLink)


        # ---------------------------------------------------------------------
        # Set translations registry
        # ---------------------------------------------------------------------

        from .translate.registry import TransaltionRegistry

        settings._TRANSLATION_REGISTRY = TransaltionRegistry()


        # ---------------------------------------------------------------------
        # Get nltk, set it up
        # ---------------------------------------------------------------------

        import nltk
        nltk.download('punkt', download_dir='nltk')
        nltk.data.path.append(os.path.join(dj_settings.BASE_DIR, 'nltk'))
