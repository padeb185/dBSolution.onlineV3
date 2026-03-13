from django.urls import path
from outillage.views import OutillageListView
from .views import modifier_outillage, outillage_detail, ajouter_outillage_all




app_name = "outillage"


urlpatterns = [
    path("", OutillageListView.as_view(), name="outillage_list"),

    path(
        "outillage/creer/",
        ajouter_outillage_all,
        name="outillage_form",
    ),

    path(
        "<int:outillage_id>/",
        outillage_detail,
        name="outillage_detail",
    ),

    path(
        'outillage/<int:outillage_id>/modifier/',
        modifier_outillage,
        name='modifier_outillage'
    ),


]