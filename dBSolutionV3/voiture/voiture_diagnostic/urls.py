from django.urls import path

from . import views

app_name = "voiture_diagnostic"

urlpatterns = [
    path("", views.diagnostic_liste, name="diagnostic_liste"),
    path("ajouter/", views.diagnostic_ajouter, name="diagnostic_ajouter"),
    path("<uuid:diagnostic_id>/", views.diagnostic_detail, name="diagnostic_detail"),
    path("<uuid:diagnostic_id>/pdf/", views.diagnostic_pdf, name="diagnostic_pdf"),
    path("<uuid:diagnostic_id>/modifier/", views.diagnostic_modifier, name="diagnostic_modifier"),
    path("<uuid:diagnostic_id>/supprimer/", views.diagnostic_supprimer, name="diagnostic_supprimer"),
]
