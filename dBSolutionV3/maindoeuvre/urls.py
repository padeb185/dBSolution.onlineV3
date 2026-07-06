import maindoeuvre
from django.urls import path
from .views import MainDoeuvreListView, main_oeuvre_form_view, modifier_maindoeuvre_view, maindoeuvre_detail_pdf_view, \
    maindoeuvre_detail_view

urlpatterns = [
    path("", MainDoeuvreListView.as_view(), name="main_oeuvre_list"),

    path("ajouter/", main_oeuvre_form_view, name="main_oeuvre_form"),

    path(
        "<uuid:main_oeuvre_id>/detail/",
        maindoeuvre_detail_view,
        name="main_oeuvre_detail",
    ),

    path(
        "<uuid:main_oeuvre_id>/modifier/",
        modifier_maindoeuvre_view,
        name="modifier_maindoeuvre",
    ),

    path(
        "<uuid:main_oeuvre_id>/pdf/",
        maindoeuvre_detail_pdf_view,
        name="main_oeuvre_detail_pdf",
    ),
]