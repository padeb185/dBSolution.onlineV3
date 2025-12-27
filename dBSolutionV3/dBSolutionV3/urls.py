from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
]

urlpatterns += i18n_patterns(
    path("", include("dBSolutionV3.urls_public")),   # domaine public
    path("", include("dBSolutionV3.urls_tenant")),   # tenant (via middleware)
    path("admin/", admin.site.urls),
)
