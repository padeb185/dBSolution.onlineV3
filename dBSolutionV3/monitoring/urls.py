from django.urls import path

from . import views

app_name = "monitoring"

urlpatterns = [
    path("", views.tableau, name="tableau"),
    path("tenant/<int:pk>/", views.tenant, name="tenant"),
    path("api/", views.api, name="api"),
]
