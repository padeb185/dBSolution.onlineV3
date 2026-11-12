from django.urls import include, path
from rest_framework.routers import SimpleRouter

from . import views

app_name = "api_particulier"

routeur = SimpleRouter()
routeur.register("vehicules", views.VehiculeViewSet, basename="vehicule")
routeur.register("kilometrages", views.ReleveViewSet, basename="kilometrage")
routeur.register("pleins", views.PleinViewSet, basename="plein")
routeur.register("recharges", views.RechargeViewSet, basename="recharge")
routeur.register("entretiens", views.EntretienViewSet, basename="entretien")
routeur.register("maintenances", views.MaintenanceViewSet, basename="maintenance")
routeur.register("pneus", views.PneusViewSet, basename="pneus")
routeur.register("documents", views.DocumentViewSet, basename="document")
routeur.register("rappels", views.RappelViewSet, basename="rappel")
routeur.register("depenses", views.DepenseViewSet, basename="depense")

urlpatterns = [
    path("auth/inscription/", views.InscriptionView.as_view(), name="inscription"),
    path("auth/connexion/", views.ConnexionView.as_view(), name="connexion"),
    path("auth/deconnexion/", views.DeconnexionView.as_view(), name="deconnexion"),
    path("moi/", views.MoiView.as_view(), name="moi"),
    path("moi/mot-de-passe/", views.MotDePasseView.as_view(), name="mot_de_passe"),
    path("moi/email/", views.EmailView.as_view(), name="email"),
    path("tableau-de-bord/", views.TableauDeBordView.as_view(), name="tableau_de_bord"),
    path("vin/", views.VinView.as_view(), name="vin"),
    path("simulateur/", views.SimulateurView.as_view(), name="simulateur"),
    path("catalogue/", views.CatalogueView.as_view(), name="catalogue"),
    path("abonnement/", views.AbonnementView.as_view(), name="abonnement"),
    path("abonnement/achat/", views.AchatView.as_view(), name="abonnement_achat"),
    path("appareils/", views.AppareilsView.as_view(), name="appareils"),
    path("abonnement/notifications/apple/", views.NotificationAppleView.as_view(), name="notification_apple"),
    path("abonnement/notifications/google/", views.NotificationGoogleView.as_view(), name="notification_google"),
    path("", include(routeur.urls)),
]
