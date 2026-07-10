from django.urls import path
from .views import dashboard_echappement_view

app_name = "echappement"


urlpatterns = [
    path(
        "echappement/<uuid:exemplaire_id>/dashboard/",
        dashboard_echappement_view,
        name="dashboard_echappement",
    ),


]
