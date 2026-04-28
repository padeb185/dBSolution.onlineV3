from django.urls import path
from .views import *

urlpatterns = [
    path("", MainDoeuvreListView.as_view(), name="main_oeuvre_list"),
    path("create/", MainDoeuvreCreateView.as_view(), name="main_oeuvre_create"),
    path("update/<uuid:pk>/", MainDoeuvreUpdateView.as_view(), name="main_oeuvre_update"),
    path("delete/<uuid:pk>/", MainDoeuvreDeleteView.as_view(), name="main_oeuvre_delete"),
]