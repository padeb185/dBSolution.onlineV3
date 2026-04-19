from django.urls import path
from .views import achat_mds_view, AchatMdsListView, achat_detail_view, modifier_achat_view

app_name = "achat_mds"

urlpatterns = [


    path(
        "achat_mds/",
        AchatMdsListView.as_view(),
        name="achat_list",
    ),

    path("<uuid:achat_id>/", achat_detail_view, name="achat_detail"),

    path("achat/", achat_mds_view, name="achat_form"),

    path(
        'achat/<uuid:achat_id>/modifier/',
        modifier_achat_view,
        name='modifier_achat_mds'),



]
