# maintenance/check_up/urls.py
from django.urls import path
from .views import EspListView, esp_form_view, modifier_esp_view, esp_detail_view, \
    esp_detail_pdf_view, delete_esp_view

app_name = "esp"


urlpatterns = [

    path('esp/<uuid:exemplaire_id>/liste/', EspListView.as_view(),name='esp_list'),

    path('esp/<uuid:exemplaire_id>/', esp_form_view, name='esp_form'),


    path('esp/<int:esp_id>/modifier/', modifier_esp_view, name='modifier_esp'),


    path('esp/<int:esp_id>/detail/', esp_detail_view, name='esp_detail'),

    path("<int:pk>/detail/", esp_detail_pdf_view, name="esp_detail_pdf"),

    path("esp/<int:esp_id>/delete/", delete_esp_view, name="delete_esp"),

]

