from django.urls import path
from . import entretien
from .entretien.views import creer_entretien
from .views import maintenance_detail_view
from .views import (
    liste_maintenance_all,
    choisir_type_maintenance,
    maintenance_tenant_view,
)


app_name = "maintenance"

urlpatterns = [
    path('', liste_maintenance_all, name='liste_maintenance_all'),

    path('<uuid:exemplaire_id>/choisir_type/', choisir_type_maintenance, name='choisir_type'),

    path('<uuid:exemplaire_id>/entretien/', creer_entretien, name='creer_entretien'),  # <-- création maintenance complète
    path(
        "<uuid:maintenance_id>/",
        maintenance_detail_view,
        name="maintenance_detail",
    ),

    path("maintenance/<uuid:exemplaire_id>/", maintenance_tenant_view, name="maintenance_tenant"),




]
