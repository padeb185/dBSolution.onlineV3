# maintenance/check_up/urls.py
from django.urls import path
from .views import PotDenoxListView, pot_denox_form_view, modifier_pot_denox_view, pot_denox_detail_view, \
    pot_denox_detail_pdf_view, delete_pot_denox_view

app_name = "pot_denox"


urlpatterns = [

    path('pot_denox/<uuid:exemplaire_id>/liste/', PotDenoxListView.as_view(),name='pot_denox_list'),

    path('pot_denox/<uuid:exemplaire_id>/', pot_denox_form_view, name='pot_denox_form'),


    path('pot_denox/<int:pot_denox_id>/modifier/', modifier_pot_denox_view, name='modifier_pot_denox'),


    path('pot_denox/<int:pot_denox_id>/detail/', pot_denox_detail_view, name='pot_denox_detail'),

    path("<int:pk>/detail/", pot_denox_detail_pdf_view, name="pot_denox_detail_pdf"),

    path("pot_denox/<int:pot_denox_id>/delete/", delete_pot_denox_view, name="delete_pot_denox"),

]

