from django.urls import path
from .check_up.views import creer_checkup_complet
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
    path('<uuid:exemplaire_id>/checkup/', maintenance_tenant_view, name='maintenance_tenant_creer'),  # <-- création maintenance complète
    path(
        "<uuid:maintenance_id>/",
        maintenance_detail_view,
        name="maintenance_detail",
    ),


    path('creer/<uuid:exemplaire_id>/', creer_checkup_complet, name='creer_checkup'),


]
