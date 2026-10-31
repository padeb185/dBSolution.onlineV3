from django.urls import path

from . import views

app_name = "voiture_remorque"

urlpatterns = [
    path("", views.remorque_list, name="remorque_list"),
    path("ajouter/", views.remorque_form, name="remorque_ajouter"),
    path("<uuid:pk>/", views.remorque_detail, name="remorque_detail"),
    path("<uuid:pk>/modifier/", views.remorque_form, name="remorque_modifier"),
    path("<uuid:pk>/supprimer/", views.remorque_supprimer, name="remorque_supprimer"),
]
