# maintenance/check_up/urls.py
from django.urls import path
from .views import SilencieuxListView, silencieux_form_view, modifier_silencieux_view, silencieux_detail_view, \
    silencieux_detail_pdf_view, delete_silencieux_view

app_name = "silencieux"


urlpatterns = [

    path('silencieux/<uuid:exemplaire_id>/liste/', SilencieuxListView.as_view(),name='silencieux_list'),

    path('silencieux/<uuid:exemplaire_id>/', silencieux_form_view, name='silencieux_form'),


    path('silencieux/<int:silencieux_id>/modifier/', modifier_silencieux_view, name='modifier_silencieux'),


    path('silencieux/<int:silencieux_id>/detail/', silencieux_detail_view, name='silencieux_detail'),

    path("<int:pk>/detail/", silencieux_detail_pdf_view, name="silencieux_detail_pdf"),

    path("silencieux/<int:silencieux_id>/delete/", delete_silencieux_view, name="delete_silencieux"),

]

