from django.urls import path
from .views import achat_mds_view, AchatMdsListView, achat_detail_view

app_name = "achat_mds"

urlpatterns = [


    path(
        "achat_mds/",
        AchatMdsListView.as_view(),
        name="achat_list",
    ),

    path(
        "<uuid:achat_mds_id>/",
        achat_detail_view,
        name="achat_detail",
    ),

    path(
        'achat_mds/',
        achat_mds_view,
        name='achat_form'),




]
