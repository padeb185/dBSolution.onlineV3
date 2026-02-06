from django.urls import path
from .views import InterventionListView, modifier_intervention, ajouter_intervention_all, intervention_detail

app_name = "intervention"


urlpatterns = [
    path(
        "intervention/",
         InterventionListView,
         name="intervention_list"
         ),

path(
        "intervention/creer/",
        ajouter_intervention_all,
        name="intervention_create",
    ),

    path(
        "<int:intervention_id>/",
        intervention_detail,
        name="intervention_detail",
    ),
    path(
        "intervention/<int:intervention_id>/modifier/",
        modifier_intervention,
        name="modifier_intervention",
    ),

]
