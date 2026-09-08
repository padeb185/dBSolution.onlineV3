# maintenance/check_up/urls.py
from django.urls import path
from .views import injection_form_view, modifier_injection_view, injection_detail_view, \
    injection_detail_pdf_view, InjectionListView, delete_injection_view

app_name = "injection"


class InjectionDistributionListView:
    pass


urlpatterns = [

    path('injection/<uuid:exemplaire_id>/liste/', InjectionListView.as_view(),name='injection_list'),

    path('injection/<uuid:exemplaire_id>/', injection_form_view, name='injection_form'),

    path('injection/<int:injection_id>/modifier/', modifier_injection_view, name='modifier_injection'),

    path('injection/<int:injection_id>/detail/', injection_detail_view, name='injection_detail'),

    path("<int:pk>/detail/", injection_detail_pdf_view, name="injection_detail_pdf"),

    path("injection/<int:injection_id>/delete/", delete_injection_view, name="delete_injection"),

]

