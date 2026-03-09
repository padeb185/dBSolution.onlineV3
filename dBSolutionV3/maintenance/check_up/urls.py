# maintenance/check_up/urls.py
from django.urls import path
from .views import  controle_total_view

app_name = "check_up"

urlpatterns = [

    path('controle-total/<uuid:exemplaire_id>/', controle_total_view, name='controle_total_view'),
]




