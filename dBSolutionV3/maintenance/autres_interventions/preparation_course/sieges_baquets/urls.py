# maintenance/check_up/urls.py
from django.urls import path
from .views import SiegesBaquetsListView, pc_sieges_form_view, modifier_pc_sieges_view, pc_sieges_detail_view, \
    pc_sieges_detail_pdf_view, delete_pc_sieges_view

app_name = "pc_sieges"


urlpatterns = [

    path('pc_sieges/<uuid:exemplaire_id>/liste/', SiegesBaquetsListView.as_view(),name='pc_sieges_list'),

    path('pc_sieges/<uuid:exemplaire_id>/', pc_sieges_form_view, name='pc_sieges_form'),


    path('pc_sieges/<int:pc_sieges_id>/modifier/', modifier_pc_sieges_view, name='modifier_pc_sieges'),


    path('pc_sieges/<int:pc_sieges_id>/detail/', pc_sieges_detail_view, name='pc_sieges_detail'),

    path("<int:pk>/detail/", pc_sieges_detail_pdf_view, name="pc_sieges_detail_pdf"),

    path("pc_sieges/<int:pc_sieges_id>/delete/", delete_pc_sieges_view, name="delete_pc_sieges"),

]

