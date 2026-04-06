from django.urls import path
from .views import liste_pneus, ajouter_pneus_simple, pneus_detail_view, modifier_pneus_view

app_name = 'voiture_pneus'

urlpatterns = [

    path('', liste_pneus, name='list'),

    path('ajouter/', ajouter_pneus_simple, name='ajouter_pneus_simple'),

    # DETAIL
    path("<uuid:pneu_id>/", pneus_detail_view, name="detail"),

    # MODIFIER ✅ (URL différente)
    path("<uuid:pneu_id>/modifier/", modifier_pneus_view, name="modifier_pneus"),

    # LIER
    path("<uuid:pneu_id>/lier_pneus/<uuid:boite_id>/", pneus_detail_view, name='lier_pneus'),

]