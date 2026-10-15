# maintenance/check_up/urls.py
from django.urls import path
from .views import LubrificationListView, lubrification_form_view, modifier_lubrification_view, lubrification_detail_view, \
    lubrification_detail_pdf_view, delete_lubrification_view

app_name = "lubrification"


urlpatterns = [

    path('lubrification/<uuid:exemplaire_id>/liste/', LubrificationListView.as_view(),name='lubrification_list'),

    path('lubrification/<uuid:exemplaire_id>/', lubrification_form_view, name='lubrification_form'),


    path('lubrification/<int:lubrification_id>/modifier/', modifier_lubrification_view, name='modifier_lubrification'),


    path('lubrification/<int:lubrification_id>/detail/', lubrification_detail_view, name='lubrification_detail'),

    path("<int:pk>/detail/", lubrification_detail_pdf_view, name="lubrification_detail_pdf"),

    path("lubrification/<int:lubrification_id>/delete/", delete_lubrification_view, name="delete_lubrification"),

]

