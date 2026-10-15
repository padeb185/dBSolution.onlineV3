# maintenance/check_up/urls.py
from django.urls import path
from .views import RenovationMachoiresListView, renovation_machoires_form_view, modifier_renovation_machoires_view, renovation_machoires_detail_view, \
    renovation_machoires_detail_pdf_view, delete_renovation_machoires_view

app_name = "renovation_machoires"


urlpatterns = [

    path('renovation_machoires/<uuid:exemplaire_id>/liste/', RenovationMachoiresListView.as_view(),name='renovation_machoires_list'),

    path('renovation_machoires/<uuid:exemplaire_id>/', renovation_machoires_form_view, name='renovation_machoires_form'),


    path('renovation_machoires/<int:renovation_machoires_id>/modifier/', modifier_renovation_machoires_view, name='modifier_renovation_machoires'),


    path('renovation_machoires/<int:renovation_machoires_id>/detail/', renovation_machoires_detail_view, name='renovation_machoires_detail'),

    path("<int:pk>/detail/", renovation_machoires_detail_pdf_view, name="renovation_machoires_detail_pdf"),

    path("renovation_machoires/<int:renovation_machoires_id>/delete/", delete_renovation_machoires_view, name="delete_renovation_machoires"),

]

