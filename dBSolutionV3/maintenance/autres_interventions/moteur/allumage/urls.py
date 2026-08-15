# maintenance/check_up/urls.py
from django.urls import path
from .views import AllumageListView, allumage_check_view, modifier_allumage_view, allumage_detail_view, \
    allumage_detail_pdf_view

app_name = "allumage"


urlpatterns = [

    path('allumage/<uuid:exemplaire_id>/liste/', AllumageListView.as_view(),name='allumage_list'),

    path('allumage/<uuid:exemplaire_id>/', allumage_check_view, name='allumage_check'),


    path('allumage/<int:allumage_id>/modifier/', modifier_allumage_view, name='modifier_allumage'),


    path('allumage/<int:allumage_id>/detail/', allumage_detail_view, name='allumage_detail'),

    path("<int:pk>/detail/", allumage_detail_pdf_view, name="allumage_detail_pdf"),

]

