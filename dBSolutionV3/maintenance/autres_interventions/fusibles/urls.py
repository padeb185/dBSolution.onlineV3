# maintenance/check_up/urls.py
from django.urls import path
from .views import FusiblesListView, fusibles_form_view, modifier_fusibles_view, fusibles_detail_view, \
    fusibles_detail_pdf_view, delete_fusibles_view

app_name = "fusibles"


urlpatterns = [

    path('fusibles/<uuid:exemplaire_id>/liste/', FusiblesListView.as_view(),name='fusibles_list'),

    path('fusibles/<uuid:exemplaire_id>/', fusibles_form_view, name='fusibles_form'),


    path('fusibles/<int:fusibles_id>/modifier/', modifier_fusibles_view, name='modifier_fusibles'),


    path('fusibles/<int:fusibles_id>/detail/', fusibles_detail_view, name='fusibles_detail'),

    path("<int:pk>/detail/", fusibles_detail_pdf_view, name="fusibles_detail_pdf"),

    path("fusibles/<int:fusibles_id>/delete/", delete_fusibles_view, name="delete_fusibles"),

]

