from django.urls import path
from .views import choisir_autre_maintenance, liste_autre_all
from ..check_up.views import controle_total_view
from ..views import  maintenance_detail_view, maintenance_tenant_view, maintenance_liste_view

app_name = "autres_interventions"

urlpatterns = [
    path('autres_interventions', liste_autre_all, name='liste_maintenance_all'),

    path('<uuid:exemplaire_id>/choisir_autre/', choisir_autre_maintenance, name='choisir_autre'),

]