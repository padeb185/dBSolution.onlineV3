from django.urls import path
from .views import (
    AssurancePoliceListView,
    ajouter_assurance_all,
    modifier_assurance_police,
    assurance_police_detail,
    dashboard_assurances, delete_assurance_police_view, document_pdf_view,
)

from . import views_sinistre

app_name = 'assurance_police'

urlpatterns = [
    path('', AssurancePoliceListView.as_view(), name='assurance_police_list'),
    path('formulaire/', ajouter_assurance_all, name='assurance_police_form'),
    path('dashboard/', dashboard_assurances, name='dashboard'),
    path(
        '<uuid:assurance_police_id>/modifier/',
        modifier_assurance_police,
        name='modifier_assurance_police'
    ),

    path(
        'detail/<uuid:assurance_police_id>/',
        assurance_police_detail,
        name='assurance_police_detail'
    ),

    path("<uuid:pk>/supprimer/", delete_assurance_police_view, name="delete_assurance_police"),
    path("<uuid:pk>/document.pdf", document_pdf_view, name="document_pdf"),

    # Sinistres
    path("sinistres/", views_sinistre.sinistre_liste, name="sinistre_liste"),
    path("sinistres/declarer/", views_sinistre.sinistre_ajouter, name="sinistre_ajouter"),
    path("sinistres/<uuid:sinistre_id>/modifier/", views_sinistre.sinistre_modifier, name="sinistre_modifier"),
    path("sinistres/<uuid:sinistre_id>/supprimer/", views_sinistre.sinistre_supprimer, name="sinistre_supprimer"),



]
