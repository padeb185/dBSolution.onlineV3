from django.urls import path
from .views import (
    AssurancePoliceListView,
    ajouter_assurance_all,
    modifier_assurance_police,
    assurance_police_detail,
    dashboard_assurances,
)

app_name = 'assurance_police'

urlpatterns = [
    path('', AssurancePoliceListView.as_view(), name='assurance_police_list'),
    path('formulaire/', ajouter_assurance_all, name='assurance_police_form'),
    path('dashboard/', dashboard_assurances, name='dashboard'),
    path(
        '<uuid:assurance_police_id>/modifier/',
        modifier_assurance_police,
        name='modifier_assurance_police'
    ),

    path(
        'detail/<uuid:assurance_police_id>/',
        assurance_police_detail,
        name='assurance_police_detail'
    )

]
