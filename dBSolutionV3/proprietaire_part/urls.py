# urls.py de ton app (par ex. voiture/urls.py)
from django.urls import path
from . import views

app_name = "voiture"

urlpatterns = [
    path('edit/<int:voiture_id>/', views.voiture_edit, name='voiture_edit'),
]
