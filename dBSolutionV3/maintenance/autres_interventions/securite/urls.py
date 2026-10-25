# maintenance/check_up/urls.py
from django.urls import path
from .views import SecuriteListView, securite_form_view, modifier_securite_view, securite_detail_view, \
    securite_detail_pdf_view, delete_securite_view

app_name = "securite"


urlpatterns = [

    path('securite/<uuid:exemplaire_id>/liste/', SecuriteListView.as_view(),name='securite_list'),

    path('securite/<uuid:exemplaire_id>/', securite_form_view, name='securite_form'),


    path('securite/<int:securite_id>/modifier/', modifier_securite_view, name='modifier_securite'),


    path('securite/<int:securite_id>/detail/', securite_detail_view, name='securite_detail'),

    path("<int:pk>/detail/", securite_detail_pdf_view, name="securite_detail_pdf"),

    path("securite/<int:securite_id>/delete/", delete_securite_view, name="delete_securite"),

]

