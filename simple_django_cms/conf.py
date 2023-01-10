from django.conf import settings as dj_settings

from .apps import SimpleDjangoCmsConfig
from .loader import load


class Settings:

    _CONTENT_TYPE_REGISTRY = None
    _MARKDOWN_WIDGET_REGISTRY = None
    _TRANSLATION_REGISTRY = None
    _FILE_HANDLING_BACKEND = None

    APP_NAME = SimpleDjangoCmsConfig.name

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
    def CONTENT_TYPE_REGISTRY(self):
        return self._CONTENT_TYPE_REGISTRY

    # --

    @property
    def FILE_HANDLING_BACKEND(self):
        return self._FILE_HANDLING_BACKEND

    # --

    @property
    def MARKDOWN_WIDGET_REGISTRY(self):
        return self._MARKDOWN_WIDGET_REGISTRY

    # --

    @property
    def TRANSLATION_REGISTRY(self):
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
