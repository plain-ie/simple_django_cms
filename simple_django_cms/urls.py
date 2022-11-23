from django.urls import include, path

from .conf import settings


urlpatterns = []


if settings.ENABLE_ADMIN_SITE is True:

    from .platform.admin.urls import urlpatterns as admin_urlpatterns

    urlpatterns += [
        path('cms/', include(admin_urlpatterns)),
    ]


if settings.ENABLE_API is True:
    urlpatterns += []


if settings.ENABLE_SITE is True:
    urlpatterns += []
