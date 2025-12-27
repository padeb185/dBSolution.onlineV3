from django.urls import path, include
from theme.views import dashboard


urlpatterns = [
    path("dashboard/", dashboard, name="dashboard"),
    path("auth/", include("authentification.urls")),

]

