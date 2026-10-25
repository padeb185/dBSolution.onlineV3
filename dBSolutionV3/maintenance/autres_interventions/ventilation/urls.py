# maintenance/check_up/urls.py
from django.urls import path
from .views import VentilationListView, ventilation_form_view, modifier_ventilation_view, ventilation_detail_view, \
    ventilation_detail_pdf_view, delete_ventilation_view

app_name = "ventilation"


urlpatterns = [

    path('ventilation/<uuid:exemplaire_id>/liste/', VentilationListView.as_view(),name='ventilation_list'),

    path('ventilation/<uuid:exemplaire_id>/', ventilation_form_view, name='ventilation_form'),


    path('ventilation/<int:ventilation_id>/modifier/', modifier_ventilation_view, name='modifier_ventilation'),


    path('ventilation/<int:ventilation_id>/detail/', ventilation_detail_view, name='ventilation_detail'),

    path("<int:pk>/detail/", ventilation_detail_pdf_view, name="ventilation_detail_pdf"),

    path("ventilation/<int:ventilation_id>/delete/", delete_ventilation_view, name="delete_ventilation"),

]

