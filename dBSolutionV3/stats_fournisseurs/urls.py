# fournisseur_stats/urls.py

from django.urls import path
from .views import stats_fournisseur_view, stats_fournisseur_pdf_view

app_name = "stats_fournisseurs"

urlpatterns = [
    path(
        "statistiques/",
        stats_fournisseur_view,
        name="statistiques"
    ),
    path(
        "statistiques/pdf/",
        stats_fournisseur_pdf_view,
        name="statistiques_pdf"
    ),
]
