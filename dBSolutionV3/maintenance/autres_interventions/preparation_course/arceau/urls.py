# maintenance/check_up/urls.py
from django.urls import path
from .views import ArceauSecuriteListView, pc_arceau_form_view, modifier_pc_arceau_view, pc_arceau_detail_view, \
    pc_arceau_detail_pdf_view, delete_pc_arceau_view

app_name = "pc_arceau"


urlpatterns = [

    path('pc_arceau/<uuid:exemplaire_id>/liste/', ArceauSecuriteListView.as_view(),name='pc_arceau_list'),

    path('pc_arceau/<uuid:exemplaire_id>/', pc_arceau_form_view, name='pc_arceau_form'),


    path('pc_arceau/<int:pc_arceau_id>/modifier/', modifier_pc_arceau_view, name='modifier_pc_arceau'),


    path('pc_arceau/<int:pc_arceau_id>/detail/', pc_arceau_detail_view, name='pc_arceau_detail'),

    path("<int:pk>/detail/", pc_arceau_detail_pdf_view, name="pc_arceau_detail_pdf"),

    path("pc_arceau/<int:pc_arceau_id>/delete/", delete_pc_arceau_view, name="delete_pc_arceau"),

]

