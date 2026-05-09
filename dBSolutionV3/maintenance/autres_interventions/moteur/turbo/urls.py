# maintenance/check_up/urls.py
from django.urls import path
from .views import TurboListView, turbo_check_view, modifier_turbo_view, turbo_detail_view, turbo_detail_pdf_view

app_name = "turbo"

urlpatterns = [

    path('turbo/<uuid:exemplaire_id>/liste/', TurboListView.as_view(),name='turbo_list'),

    path('turbo/<uuid:exemplaire_id>/', turbo_check_view, name='turbo_check'),


    path('turbo/<int:turbo_id>/modifier/', modifier_turbo_view, name='modifier_turbo'),


    path('turbo/<int:turbo_id>/detail/', turbo_detail_view, name='turbo_detail'),

    path("<int:pk>/detail/", turbo_detail_pdf_view, name="turbo_detail_pdf"),

]


