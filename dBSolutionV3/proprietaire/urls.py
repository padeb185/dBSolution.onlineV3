from django.urls import path
from .views import proprietaire_dashboard_view, ProprietaireListView, ProprietaireVoitureListView, check_prenom, \
    proprietaire_form_view, proprietaire_detail_view, proprietaire_voiture_form_view, \
    proprietaire_voiture_detail_view, total_part_voiture, modifier_proprietaire_voiture_view

app_name = "proprietaire"

urlpatterns = [
    path('', proprietaire_dashboard_view, name='proprietaire_dashboard'),

    path('list/', ProprietaireListView.as_view(), name='proprietaire_list'),

    path("creer/",proprietaire_form_view, name="proprietaire_form",),

    path('api/check_prenom/', check_prenom, name='check_prenom'),

    path("<int:proprietaire_voiture_id>/", proprietaire_detail_view, name="proprietaire_detail"),

    path('<int:proprietaire_voiture_id>/modifier/',modifier_proprietaire_voiture_view,name='modifier_proprietaire_voiture'),







    path('proprietaire', ProprietaireVoitureListView.as_view(), name='proprietaire_voiture_list'),

    path('proprietaire/creer/', proprietaire_voiture_form_view, name='proprietaire_voiture_form'),

    path("proprietaire/<int:proprietaire_voiture_id>/",proprietaire_voiture_detail_view,name="proprietaire_voiture_detail"),

    path("api/voiture/<int:voiture_id>/total-part/", total_part_voiture ,name="total_part_voiture"),
]
