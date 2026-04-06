from django.contrib.auth.decorators import login_required
from django.urls import path
from .views import InterventionListView, intervention_create_view, intervention_detail_view, modifier_intervention_view

app_name = "intervention"


urlpatterns = [
    path(
        "intervention/",
        login_required(InterventionListView.as_view()),
        name="intervention_list",
    ),

    path(
        "intervention/creer/",
        intervention_create_view,
        name="intervention_create",
    ),

    path(
        "<int:intervention_id>/",
        intervention_detail_view,
        name="intervention_detail",
    ),
    path(
        "intervention/<int:intervention_id>/modifier/",
        modifier_intervention_view,
        name="modifier_intervention",
    ),

]
