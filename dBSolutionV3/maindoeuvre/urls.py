from django.urls import path
from .views import MainDoeuvreListView, main_oeuvre_form_view

urlpatterns = [
    path("", MainDoeuvreListView.as_view(), name="main_oeuvre_list"),

    path('maindoeuvre/', main_oeuvre_form_view, name='main_oeuvre_form'),

]
