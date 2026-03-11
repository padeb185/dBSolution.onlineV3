from django.urls import path
from outillage.views import OutillageListView


app_name = "outillage"


urlpatterns = [
    path("", OutillageListView.as_view(), name="outillage_list"),
    #path("add/", PieceCreateView.as_view(), name="add"),
    #path("<uuid:pk>/", PieceDetailView.as_view(), name="detail"),
    #path("<uuid:pk>/edit/", PieceUpdateView.as_view(), name="edit"),
    #path("<uuid:pk>/delete/", PieceDeleteView.as_view(), name="delete"),
    #path("api/check_fabricants", check_fabricants, name="check_fabricants"),
]