from django.urls import include, path
from rest_framework.routers import SimpleRouter

from . import views

app_name = "api_particulier"

routeur = SimpleRouter()
routeur.register("vehicules", views.VehiculeViewSet, basename="vehicule")
routeur.register("kilometrages", views.ReleveViewSet, basename="kilometrage")
routeur.register("pleins", views.PleinViewSet, basename="plein")
routeur.register("entretiens", views.EntretienViewSet, basename="entretien")
routeur.register("documents", views.DocumentViewSet, basename="document")
routeur.register("rappels", views.RappelViewSet, basename="rappel")
routeur.register("depenses", views.DepenseViewSet, basename="depense")

urlpatterns = [
    path("auth/inscription/", views.InscriptionView.as_view(), name="inscription"),
    path("auth/connexion/", views.ConnexionView.as_view(), name="connexion"),
    path("auth/deconnexion/", views.DeconnexionView.as_view(), name="deconnexion"),
    path("moi/", views.MoiView.as_view(), name="moi"),
    path("tableau-de-bord/", views.TableauDeBordView.as_view(), name="tableau_de_bord"),
    path("vin/", views.VinView.as_view(), name="vin"),
    path("", include(routeur.urls)),
]
