# fournisseur_stats/urls.py

from django.urls import path
from .views import stats_fournisseur_view

app_name = "stats_fournisseurs"

urlpatterns = [
    path(
        "statistiques/",
        stats_fournisseur_view,
        name="statistiques"
    ),
]