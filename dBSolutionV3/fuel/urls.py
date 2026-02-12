from django.urls import path
from . import views

app_name = "fuel"

urlpatterns = [
    path("fuel/", views.fuel_list, name="fuel_list"),
    path("fuel/add/", views.fuel_add, name="fuel_add"),
    path("fuel/edit/<int:pk>/", views.fuel_edit, name="fuel_edit"),
    path("fuel/delete/<int:pk>/", views.fuel_delete, name="fuel_delete"),
    path('ajax/get_car_info/', views.get_car_info, name='get_car_info'),


]
