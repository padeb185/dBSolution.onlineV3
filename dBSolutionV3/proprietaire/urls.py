from django.urls import path
from .views import proprietaire_dashboard_view, ProprietaireListView, ProprietaireVoitureListView

app_name = "proprietaire"

urlpatterns = [
    path('', proprietaire_dashboard_view, name='proprietaire_dashboard'),

    path('proprietaire', ProprietaireListView.as_view(), name='proprietaire_list'),

    path(
        "proprietaire_voiture/",
        ProprietaireVoitureListView.as_view(),
        name="proprietaire_voiture_list"
    )






]
