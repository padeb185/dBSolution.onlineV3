from django.urls import path
from . import views
from tenant.views import moteur_view
from .views import MoteurListView

app_name = "voiture_moteur"

urlpatterns = [
    # Ajouter un moteur à un exemplaire
    path("ajouter/<uuid:exemplaire_id>/", views.ajouter_moteur, name="ajouter_moteur"),


    path("", MoteurListView.as_view(), name="list"),

    # Détail d'un moteur
    path('<uuid:moteur_id>/', views.moteur_detail_view, name='detail'),
]
