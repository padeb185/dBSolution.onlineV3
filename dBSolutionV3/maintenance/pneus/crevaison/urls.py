from django.urls import path

from .views import (
    CrevaisonListView,
    crevaison_check_view,
    crevaison_detail_view,
    crevaison_pdf_view,
    delete_crevaison_view,
    modifier_crevaison_view,
)

app_name = "crevaison"

urlpatterns = [
    path("<uuid:exemplaire_id>/liste/", CrevaisonListView.as_view(), name="crevaison_list"),
    path("<uuid:exemplaire_id>/", crevaison_check_view, name="crevaison_check"),
    path("<int:crevaison_id>/detail/", crevaison_detail_view, name="crevaison_detail"),
    path("<int:crevaison_id>/modifier/", modifier_crevaison_view, name="modifier_crevaison"),
    path("<int:crevaison_id>/pdf/", crevaison_pdf_view, name="crevaison_pdf"),
    path("<int:crevaison_id>/delete/", delete_crevaison_view, name="delete_crevaison"),
]
