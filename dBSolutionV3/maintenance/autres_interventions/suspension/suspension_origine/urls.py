# maintenance/check_up/urls.py
from django.urls import path
from .views import SuspensionOrigineListView, suspension_origine_form_view, modifier_suspension_origine_view, suspension_origine_detail_view, \
    suspension_origine_detail_pdf_view, delete_suspension_origine_view

app_name = "suspension_origine"


urlpatterns = [

    path('suspension_origine/<uuid:exemplaire_id>/liste/', SuspensionOrigineListView.as_view(),name='suspension_origine_list'),

    path('suspension_origine/<uuid:exemplaire_id>/', suspension_origine_form_view, name='suspension_origine_form'),


    path('suspension_origine/<int:suspension_origine_id>/modifier/', modifier_suspension_origine_view, name='modifier_suspension_origine'),


    path('suspension_origine/<int:suspension_origine_id>/detail/', suspension_origine_detail_view, name='suspension_origine_detail'),

    path("<int:pk>/detail/", suspension_origine_detail_pdf_view, name="suspension_origine_detail_pdf"),

    path("suspension_origine/<int:suspension_origine_id>/delete/", delete_suspension_origine_view, name="delete_suspension_origine"),

]

