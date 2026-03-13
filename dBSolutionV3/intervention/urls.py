from django.contrib.auth.decorators import login_required
from django.urls import path
from .views import InterventionListView, modifier_intervention, intervention_detail, InterventionCreateView

app_name = "intervention"


urlpatterns = [
    path(
        "intervention/",
        login_required(InterventionListView.as_view()),
        name="intervention_list",
    ),

    path(
        "intervention/creer/",
        InterventionCreateView.as_view(),
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
