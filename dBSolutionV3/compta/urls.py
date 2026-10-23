from django.urls import path

from . import views

app_name = "compta"

urlpatterns = [
    path("", views.compta_tableau_de_bord, name="tableau_de_bord"),
    path("comptes/ouvrir/", views.compte_ouvrir, name="compte_ouvrir"),
    path("comptes/<uuid:pk>/", views.compte_journal, name="compte_journal"),
    path("comptes/<uuid:pk>/modifier/", views.compte_modifier, name="compte_modifier"),
    path("comptes/<uuid:pk>/supprimer/", views.compte_supprimer, name="compte_supprimer"),
    path("comptes/<uuid:pk>/mouvement/", views.mouvement_ajouter, name="mouvement_ajouter"),
    path("mouvements/<uuid:pk>/modifier/", views.mouvement_modifier, name="mouvement_modifier"),
    path("mouvements/<uuid:pk>/supprimer/", views.mouvement_supprimer, name="mouvement_supprimer"),
    path("virement/", views.virement_interne, name="virement_interne"),
]
