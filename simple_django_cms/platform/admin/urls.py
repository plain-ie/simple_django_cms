from django.urls import path

from ... import constants
from ...conf import settings

from .viewsets.auth_forgot_password import ForgotPasswordViewSet
from .viewsets.auth_register import RegisterViewSet
from .viewsets.auth_reset_password import ResetPasswordViewSet
from .viewsets.auth_signin import SignInViewSet
from .viewsets.auth_signout import SignOutViewSet

from .viewsets.items_create import ItemsCreateViewSet
from .viewsets.items_create_select_tenant import ItemsCreateSelectTenantViewSet
from .viewsets.items_create_select_content_type import ItemsCreateSelectContentTypeViewSet
from .viewsets.items_delete import ItemsDeleteViewSet
from .viewsets.items_list import ItemsListViewSet
from .viewsets.items_retrieve import ItemsRetrieveViewSet

from .viewsets.projects_list import ProjectsListViewSet


urlpatterns = [

    path(
        'projects/<str:project_id>/create-item/tenants/<str:tenant_id>/content-type/<str:content_type>/',
        ItemsCreateViewSet.as_view(),
        name=constants.URLNAME_ADMIN_CREATE_ITEMS
    ),
    path(
        'projects/<str:project_id>/create-item/tenants/<str:tenant_id>/',
        ItemsCreateSelectContentTypeViewSet.as_view(),
        name=constants.URLNAME_ADMIN_CREATE_ITEMS_SELECT_CONTENT_TYPE
    ),
    path(
        'projects/<str:project_id>/create-item/tenants/',
        ItemsCreateSelectTenantViewSet.as_view(),
        name=constants.URLNAME_ADMIN_CREATE_ITEMS_SELECT_TENANT
    ),
    path(
        'projects/<str:project_id>/tenants/<str:tenant_id>/items/<str:item_id>/delete/',
        ItemsDeleteViewSet.as_view(),
        name=constants.URLNAME_ADMIN_DELETE_ITEMS
    ),
    path(
        'projects/<str:project_id>/tenants/<str:tenant_id>/items/<str:item_id>/',
        ItemsRetrieveViewSet.as_view(),
        name=constants.URLNAME_ADMIN_RETRIEVE_ITEMS
    ),
    path(
        'projects/<str:project_id>/items/<str:item_id>/',
        ItemsRetrieveViewSet.as_view(),
        name=constants.URLNAME_ADMIN_RETRIEVE_ITEMS
    ),
    path(
        'projects/<str:project_id>/items/',
        ItemsListViewSet.as_view(),
        name=constants.URLNAME_ADMIN_LIST_ITEMS
    ),

    # --

    path(
        'projects/',
        ProjectsListViewSet.as_view(),
        name=constants.URLNAME_ADMIN_LIST_PROJECTS
    ),

    # --

    path(
        'auth/sign-out/',
        SignOutViewSet.as_view(),
        name=constants.URLNAME_AUTH_SIGNOUT
    ),
    path(
        'auth/reset-password/',
        ResetPasswordViewSet.as_view(),
        name=constants.URLNAME_AUTH_RESET_PASSWORD
    ),
    path(
        'auth/forgot-password/',
        ForgotPasswordViewSet.as_view(),
        name=constants.URLNAME_AUTH_FORGOT_PASSWORD
    ),
    path(
        'auth/register/',
        RegisterViewSet.as_view(),
        name=constants.URLNAME_AUTH_REGISTER
    ),
    path(
        '',
        SignInViewSet.as_view(),
        name=constants.URLNAME_AUTH_SIGNIN
    ),

]
