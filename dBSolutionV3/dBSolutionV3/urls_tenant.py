from django.urls import path
from theme.views import dashboard

urlpatterns = [
    path("", dashboard, name="dashboard"),
]
