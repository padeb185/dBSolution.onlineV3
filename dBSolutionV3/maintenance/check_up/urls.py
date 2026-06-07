# maintenance/check_up/urls.py
from django.urls import path
from .views import controle_total_view, CheckupListView, checkup_detail_view, modifier_checkup_view, checkup_pdf_view

app_name = "check_up"

urlpatterns = [

    path('check_up/<uuid:exemplaire_id>/liste/', CheckupListView.as_view(),name='checkup_list'),

    path('controle-total/<uuid:exemplaire_id>/', controle_total_view, name='controle_total_view'),


    path('<int:checkup_id>/modifier/', modifier_checkup_view, name='modifier_checkup'),


    path('<int:checkup_id>/detail/', checkup_detail_view, name='checkup_detail'),

    path("<int:checkup_id>/pdf/", checkup_pdf_view, name="checkup_detail_pdf"),
]




