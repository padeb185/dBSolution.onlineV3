from django.urls import path

from . import views

app_name = "notifications"

urlpatterns = [
    path("", views.liste, name="liste"),
    path("<uuid:pk>/ouvrir/", views.ouvrir, name="ouvrir"),
    path("<uuid:pk>/marquer/", views.marquer, name="marquer"),
    path("tout-lire/", views.tout_lire, name="tout_lire"),
    path("parametres/", views.parametres, name="parametres"),
    path("preferences/", views.preferences, name="preferences"),
]
