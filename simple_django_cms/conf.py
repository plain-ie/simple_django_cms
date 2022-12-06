from django.conf import settings as dj_settings

from .apps import SimpleDjangoCmsConfig
from .loader import load


class Settings:

    _CONTENT_TYPE_REGISTRY = None
    _MARKDOWN_WIDGET_REGISTRY = None
    _TRANSLATION_REGISTRY = None
    _FILE_HANDLING_BACKEND = None

    APP_NAME = SimpleDjangoCmsConfig.name

    def __init__(self):
        self.FILE_HANDLING_BACKEND  # Initiate backend with app start

    # --

    @property
    def PROJECT_TITLE(self):
        return getattr(
            dj_settings,
            'PROJECT_TITLE',
            'Simple Django CMS'
        )

    # --

    @property
    def DEFAULT_LANGUAGE(self):
        return getattr(
            dj_settings,
            'DEFAULT_LANGUAGE',
            'en'
        )

    @property
    def LANGUAGES(self):
        return getattr(
            dj_settings,
            'LANGUAGES',
            []
        )

    # --

    @property
    def ENABLE_ADMIN_SITE(self):
        return getattr(
            dj_settings,
            'ENABLE_ADMIN_SITE',
            True
        )

    @property
    def ENABLE_API(self):
        return getattr(
            dj_settings,
            'ENABLE_API',
            True
        )

    @property
    def ENABLE_SITE(self):
        return getattr(
            dj_settings,
            'ENABLE_SITE',
            True
        )

    # --

    @property
    def CONTENT_TYPE_LIST(self):
        root = f'{self.APP_NAME}.content_types'
        return getattr(
            dj_settings,
            'CONTENT_TYPE_LIST',
            [
                f'{root}.flat_pages.content_type.FlatPageContentType',
                f'{root}.images.content_type.ImageContentType',
                f'{root}.news.content_type.NewsContentType',
                f'{root}.redirects.content_type.RedirectContentType',
                f'{root}.topics.content_type.TopicContentType',
            ]
        )

    @property
    def CONTENT_TYPE_REGISTRY(self):
        if self._CONTENT_TYPE_REGISTRY is not None:
            return self._CONTENT_TYPE_REGISTRY
        self._CONTENT_TYPE_REGISTRY = load(self.CONTENT_TYPE_REGISTRY_CLASS)()
        return self._CONTENT_TYPE_REGISTRY

    @property
    def CONTENT_TYPE_REGISTRY_CLASS(self):
        return getattr(
            dj_settings,
            'CONTENT_TYPE_REGISTRY_CLASS',
            f'{self.APP_NAME}.content_types.registry.ContentTypeRegistry'
        )

    # --

    @property
    def FILE_HANDLING_BACKEND_CLASS(self):
        return getattr(
            dj_settings,
            'FILE_HANDLING_BACKEND_CLASS',
            f'{self.APP_NAME}.file_handling.local.LocalFileStorageBackend'
        )

    @property
    def FILE_HANDLING_BACKEND(self):
        if self._FILE_HANDLING_BACKEND is not None:
            return self._FILE_HANDLING_BACKEND
        self._FILE_HANDLING_BACKEND = load(self.FILE_HANDLING_BACKEND_CLASS)()
        return self._FILE_HANDLING_BACKEND

    # --

    @property
    def MARKDOWN_WIDGETS_LIST(self):
        root = f'{self.APP_NAME}.markdown.widgets'
        return getattr(
            dj_settings,
            'MARKDOWN_WIDGETS_LIST',
            [
                f'{root}.HeadingH1',
                f'{root}.HeadingH2',
                f'{root}.HeadingH3',
                f'{root}.HeadingH4',
                f'{root}.HorizontalRule',
                f'{root}.Image',
                f'{root}.UnorderedListElement',
                f'{root}.OrderedListElement',
                f'{root}.Paragraph',
            ]
        )

    @property
    def MARKDOWN_WIDGETS_LIST_EXTENSION(self):
        return getattr(
            dj_settings,
            'MARKDOWN_WIDGETS_LIST_EXTENSION',
            [],
        )

    @property
    def MARKDOWN_WIDGET_REGISTRY(self):
        if self._MARKDOWN_WIDGET_REGISTRY is not None:
            return self._MARKDOWN_WIDGET_REGISTRY
        self._MARKDOWN_WIDGET_REGISTRY = load(
            self.MARKDOWN_WIDGET_REGISTRY_CLASS)()
        return self._MARKDOWN_WIDGET_REGISTRY

    @property
    def MARKDOWN_WIDGET_REGISTRY_CLASS(self):
        return getattr(
            dj_settings,
            'MARKDOWN_WIDGET_REGISTRY_CLASS'
            f'{self.APP_NAME}.markdown.registry.MarkdownWidgetRegistry',
        )

    # --

    @property
    def TRANSLATION_REGISTRY_CLASS(self):
        return getattr(
            dj_settings,
            'TRANSLATION_REGISTRY_CLASS',
            f'{self.APP_NAME}.translate.registry.TransaltionRegistry'
        )

    @property
    def TRANSLATION_REGISTRY(self):
        if self._TRANSLATION_REGISTRY is not None:
            return self._TRANSLATION_REGISTRY
        self._TRANSLATION_REGISTRY = load(self.TRANSLATION_REGISTRY_CLASS)()
        return self._TRANSLATION_REGISTRY

    # --

    @property
    def TEMPLATE_FORGOT_PASSWORD(self):
        return getattr(
            dj_settings,
            'TEMPLATE_FORGOT_PASSWORD',
            f'{self.APP_NAME}/platform/admin/pages/forgot_password.html'
        )

    @property
    def TEMPLATE_PROJECTS_LIST(self):
        return getattr(
            dj_settings,
            'TEMPLATE_PROJECTS_LIST',
            f'{self.APP_NAME}/platform/admin/pages/projects_list.html'
        )

    @property
    def TEMPLATE_PROJECT_ITEMS_LIST(self):
        return getattr(
            dj_settings,
            'TEMPLATE_PROJECTS_LIST',
            f'{self.APP_NAME}/platform/admin/pages/item_list.html'
        )

    @property
    def TEMPLATE_REGISTER(self):
        return getattr(
            dj_settings,
            'TEMPLATE_REGISTER',
            f'{self.APP_NAME}/platform/admin/pages/register.html'
        )

    @property
    def TEMPLATE_RESET_PASSWORD(self):
        return getattr(
            dj_settings,
            'TEMPLATE_RESET_PASSWORD',
            f'{self.APP_NAME}/platform/admin/pages/reset_password.html'
        )

    @property
    def TEMPLATE_SIGNIN(self):
        return getattr(
            dj_settings,
            'TEMPLATE_SIGNIN',
            f'{self.APP_NAME}/platform/admin/pages/signin.html'
        )

    @property
    def TEMPLATE_CREATE_ITEM(self):
        return getattr(
            dj_settings,
            'TEMPLATE_CREATE_ITEM',
            f'{self.APP_NAME}/platform/admin/pages/item_create.html'
        )

    @property
    def TEMPLATE_RETRIEVE_ITEM(self):
        return getattr(
            dj_settings,
            'RETRIEVE_ITEM',
            f'{self.APP_NAME}/platform/admin/pages/item_retrieve.html'
        )

    @property
    def TEMPLATE_CREATE_ITEM_SELECT_TENANT(self):
        return getattr(
            dj_settings,
            'TEMPLATE_CREATE_ITEM_SELECT_TENANT',
            f'{self.APP_NAME}/platform/admin/pages/item_create_select_tenant.html'
        )

    @property
    def TEMPLATE_CREATE_ITEM_SELECT_CONTENT_TYPE(self):
        return getattr(
            dj_settings,
            'TEMPLATE_CREATE_ITEM_SELECT_CONTENT_TYPE',
            f'{self.APP_NAME}/platform/admin/pages/item_create_select_content_type.html'
        )

    # --

    @property
    def ITEMS_LIMIT(self):
        return getattr(
            dj_settings,
            'ITEMS_LIMIT',
            10
        )

    @property
    def TENANTS_LIMIT(self):
        return getattr(
            dj_settings,
            'TENANTS_LIMIT',
            10000
        )

    @property
    def PROJECTS_LIMIT(self):
        return getattr(
            dj_settings,
            'PROJECTS_LIMIT',
            10000
        )


settings = Settings()
