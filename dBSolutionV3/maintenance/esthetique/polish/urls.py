# maintenance/check_up/urls.py
from django.urls import path
from .views import PolishListView, polish_form_view, modifier_polish_view, polish_detail_view, \
    polish_detail_pdf_view, delete_polish_view

app_name = "polish"


urlpatterns = [

    path('polish/<uuid:exemplaire_id>/liste/', PolishListView.as_view(),name='polish_list'),

    path('polish/<uuid:exemplaire_id>/', polish_form_view, name='polish_form'),


    path('polish/<int:polish_id>/modifier/', modifier_polish_view, name='modifier_polish'),


    path('polish/<int:polish_id>/detail/', polish_detail_view, name='polish_detail'),

    path("<int:pk>/detail/", polish_detail_pdf_view, name="polish_detail_pdf"),

    path("polish/<int:polish_id>/delete/", delete_polish_view, name="delete_polish"),

]

