from django.urls import path
from .views import modifier_assurance, assurance_detail, ajouter_assurance_all, AssuranceListView


app_name = "carrosserie"



urlpatterns = [
    path(
        "assurance/",
        AssuranceListView.as_view(),
        name="assurance_list",
    ),
    path(
        "assurance/creer/",
        ajouter_assurance_all,
        name="carrosserie_create",
    ),

    path(
        "<uuid:assurance_id>/",
        assurance_detail,
        name="assurance_detail",
    ),

    path(
        'assurance/<uuid:assurance_id>/modifier/',
        modifier_assurance,
        name='modifier_assurance'),


]
