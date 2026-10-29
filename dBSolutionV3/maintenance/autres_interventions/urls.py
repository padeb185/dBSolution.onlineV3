from django.urls import path
from .views import choisir_autre_maintenance, liste_autre_all, dashboard_boites_view, dashboard_electricite_view, dashboard_geometrie_view, dashboard_aide_conduite_view, dashboard_transmission_view
from ..check_up.views import controle_total_view
from ..views import  maintenance_detail_view, maintenance_tenant_view, maintenance_liste_view

app_name = "autres_interventions"

urlpatterns = [
    path('autres_interventions', liste_autre_all, name='liste_maintenance_all'),

    path('<uuid:exemplaire_id>/choisir_autre/', choisir_autre_maintenance, name='choisir_autre'),
    path('<uuid:exemplaire_id>/boites/', dashboard_boites_view, name='dashboard_boites'),
    path('<uuid:exemplaire_id>/electricite/', dashboard_electricite_view, name='dashboard_electricite'),
    path('<uuid:exemplaire_id>/geometrie/', dashboard_geometrie_view, name='dashboard_geometrie'),
    path('<uuid:exemplaire_id>/aide-conduite/', dashboard_aide_conduite_view, name='dashboard_aide_conduite'),
    path('<uuid:exemplaire_id>/transmission/', dashboard_transmission_view, name='dashboard_transmission'),

]