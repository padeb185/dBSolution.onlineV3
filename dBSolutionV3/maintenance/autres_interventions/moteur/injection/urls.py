# maintenance/check_up/urls.py
from django.urls import path
from .views import injection_form_view, modifier_injection_view, injection_detail_view, rapport_injection_view, \
    injection_detail_pdf_view, InjectionListView, InjectionRapportDetailView

app_name = "injection"


class InjectionDistributionListView:
    pass


urlpatterns = [

    path('injection/<uuid:exemplaire_id>/liste/', InjectionListView.as_view(),name='injection_list'),

    path('injection/<uuid:exemplaire_id>/', injection_form_view, name='injection_form'),


    path('injection/<int:injection_id>/modifier/', modifier_injection_view, name='modifier_injection'),


    path('injection/<int:injection_id>/detail/', injection_detail_view, name='injection_detail'),

    path("injection/<int:pk>/", rapport_injection_view, name="rapport_injection"),

    path("injectionPDF/<int:pk>/", InjectionRapportDetailView.as_view(), name="rapport_pdf_injection"),

    path("<int:pk>/detail/", injection_detail_pdf_view, name="injection_detail_pdf"),

]

