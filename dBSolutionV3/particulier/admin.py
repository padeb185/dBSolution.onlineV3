"""Admin Django du tenant des particuliers : /tenant/<schéma particuliers>/<langue>/admin/"""
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .comptes import activer
from .models import AbonnementParticulier, CompteParticulier, Financement, Depense, Document, Entretien, MaintenanceParticulier, Plein, TrainPneus, VenteParticulier, ProfilFiscal, Rappel, ReleveKilometrique, Vehicule


def lien_fichier(modele, champ):
    """Lien vers le fichier privé (vue réservée à l'administration, jamais /media/)."""
    def lien(self, obj):
        if not getattr(obj, champ):
            return "—"
        url = reverse("particulier_admin:fichier", args=[modele, obj.pk, champ])
        return format_html('<a href="{}" target="_blank">{}</a>', url, _("Ouvrir"))
    lien.short_description = champ
    return lien


class AccesAdminParticuliers:
    """Accès : direction du tenant des particuliers (ou super admin), sans permissions Django à attribuer."""

    def _autorise(self, request):
        from .admin_web import schema_particuliers
        u = request.user
        if u.is_superuser:
            return True
        return (u.is_active and u.is_staff and getattr(u, "role", None) == "direction"
                and getattr(getattr(request, "tenant", None), "schema_name", None) == schema_particuliers())

    def has_module_permission(self, request):
        return self._autorise(request)

    def has_view_permission(self, request, obj=None):
        return self._autorise(request)

    def has_change_permission(self, request, obj=None):
        return self._autorise(request)

    def has_delete_permission(self, request, obj=None):
        return self._autorise(request)

    def has_add_permission(self, request):
        return self._autorise(request)


class LectureFichiersMixin:
    """Les champs fichier ne sont pas modifiables ici (ils s'affichent par la vue protégée)."""
    champs_fichier = ()

    def get_exclude(self, request, obj=None):
        return list(super().get_exclude(request, obj) or []) + list(self.champs_fichier)


@admin.register(CompteParticulier)
class CompteParticulierAdmin(AccesAdminParticuliers, admin.ModelAdmin):
    list_display = ("email", "prenom", "nom", "is_active", "created_at", "last_login", "nb_vehicules")
    list_filter = ("is_active",)
    search_fields = ("email", "nom", "prenom")
    ordering = ("-created_at",)
    fields = ("email", "prenom", "nom", "telephone", "is_active", "created_at", "last_login")
    readonly_fields = ("email", "created_at", "last_login")
    actions = ["desactiver", "reactiver"]

    def get_queryset(self, request):
        return super().get_queryset(request).filter(role="particulier")

    def has_add_permission(self, request):
        return False   # les comptes se créent dans l'application

    @admin.display(description=_("Véhicules"))
    def nb_vehicules(self, obj):
        return Vehicule.objects.filter(proprietaire=obj).count()

    @admin.action(description=_("Désactiver (déconnecte l'application)"))
    def desactiver(self, request, queryset):
        for u in queryset:
            activer(u, False)

    @admin.action(description=_("Réactiver"))
    def reactiver(self, request, queryset):
        for u in queryset:
            activer(u, True)

    def delete_model(self, request, obj):
        from .comptes import supprimer_compte
        supprimer_compte(obj)

    def delete_queryset(self, request, queryset):
        from .comptes import supprimer_compte
        for u in queryset:
            supprimer_compte(u)


class DonneeVehiculeAdmin(AccesAdminParticuliers, LectureFichiersMixin, admin.ModelAdmin):
    list_select_related = ("vehicule", "vehicule__proprietaire")
    search_fields = ("vehicule__marque", "vehicule__modele", "vehicule__immatriculation", "vehicule__proprietaire__email")
    autocomplete_fields = ("vehicule",)

    @admin.display(description=_("Propriétaire"), ordering="vehicule__proprietaire__email")
    def proprietaire(self, obj):
        return obj.vehicule.proprietaire.email


@admin.register(Vehicule)
class VehiculeAdmin(AccesAdminParticuliers, LectureFichiersMixin, admin.ModelAdmin):
    champs_fichier = ("photo",)
    list_display = ("marque", "modele", "immatriculation", "vin", "energie", "proprietaire", "archive", "created_at")
    list_filter = ("energie", "archive")
    search_fields = ("marque", "modele", "immatriculation", "vin", "proprietaire__email")
    list_select_related = ("proprietaire",)
    raw_id_fields = ("proprietaire",)
    readonly_fields = ("photo_lien",)
    photo_lien = lien_fichier("vehicule", "photo")


@admin.register(Plein)
class PleinAdmin(DonneeVehiculeAdmin):
    champs_fichier = ("ticket",)
    list_display = ("date", "vehicule", "proprietaire", "carburant", "kilometrage", "quantite", "montant", "plein_complet",
                    "ticket_lien")
    list_filter = ("carburant", "plein_complet")
    date_hierarchy = "date"
    readonly_fields = ("ticket_lien",)
    ticket_lien = lien_fichier("plein", "ticket")


@admin.register(Entretien)
class EntretienAdmin(DonneeVehiculeAdmin):
    champs_fichier = ("facture",)
    list_display = ("date", "type", "vehicule", "proprietaire", "kilometrage", "montant", "facture_lien")
    list_filter = ("type",)
    date_hierarchy = "date"
    readonly_fields = ("facture_lien",)
    facture_lien = lien_fichier("entretien", "facture")


@admin.register(Document)
class DocumentAdmin(DonneeVehiculeAdmin):
    champs_fichier = ("fichier",)
    list_display = ("type", "titre", "vehicule", "proprietaire", "date_expiration", "montant", "fichier_lien")
    list_filter = ("type",)
    readonly_fields = ("fichier_lien",)
    fichier_lien = lien_fichier("document", "fichier")


@admin.register(Rappel)
class RappelAdmin(DonneeVehiculeAdmin):
    list_display = ("libelle", "vehicule", "proprietaire", "echeance_date", "echeance_km", "actif")
    list_filter = ("actif", "type_entretien")


@admin.register(Depense)
class DepenseAdmin(DonneeVehiculeAdmin):
    list_display = ("date", "categorie", "libelle", "vehicule", "proprietaire", "montant")
    list_filter = ("categorie",)
    date_hierarchy = "date"


@admin.register(ReleveKilometrique)
class ReleveAdmin(DonneeVehiculeAdmin):
    list_display = ("date", "kilometrage", "vehicule", "proprietaire")


@admin.register(AbonnementParticulier)
class AbonnementAdmin(AccesAdminParticuliers, admin.ModelAdmin):
    """Formules des comptes. En développement, attribution directe ; en production, par achat dans l'application."""
    list_display = ("utilisateur", "formule", "formule_en_cours", "date_fin", "source", "renouvellement_auto",
                    "environnement", "updated_at")
    list_filter = ("formule", "source", "environnement", "renouvellement_auto")
    search_fields = ("utilisateur__email", "utilisateur__nom", "reference_store", "produit")
    list_select_related = ("utilisateur",)
    raw_id_fields = ("utilisateur",)
    readonly_fields = ("produit", "reference_store", "environnement", "renouvellement_auto", "created_at", "updated_at")
    fields = ("utilisateur", "formule", "date_fin", "source", "note", *readonly_fields)

    @admin.display(description=_("Formule en cours"))
    def formule_en_cours(self, obj):
        from .abonnements import formule_effective
        from .models import Formule
        return Formule(formule_effective(obj.utilisateur, obj)).label

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "utilisateur":
            from utilisateurs.models import Utilisateur
            kwargs["queryset"] = Utilisateur.objects.filter(role="particulier")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Financement)
class FinancementAdmin(AccesAdminParticuliers, admin.ModelAdmin):
    list_display = ("vehicule", "type_achat", "organisme", "date_debut", "duree_mois", "mensualite")
    list_filter = ("type_achat",)
    search_fields = ("vehicule__marque", "vehicule__modele", "vehicule__proprietaire__email", "organisme")
    raw_id_fields = ("vehicule",)


@admin.register(ProfilFiscal)
class ProfilFiscalAdmin(admin.ModelAdmin):
    list_display = ("vehicule", "statut", "usage_pro", "co2", "updated_at")
    list_filter = ("statut",)


@admin.register(MaintenanceParticulier)
class MaintenanceParticulierAdmin(admin.ModelAdmin):
    list_display = ("vehicule", "date", "type_maintenance", "garage", "pieces_htva", "main_oeuvre_htva", "total_tvac")
    list_filter = ("type_maintenance",)
    readonly_fields = ("tva_pieces", "tva_main_oeuvre", "total_pieces_tvac", "total_main_oeuvre_tvac",
                       "total_htva", "total_tva", "total_tvac")


@admin.register(TrainPneus)
class TrainPneusAdmin(admin.ModelAdmin):
    list_display = ("vehicule", "position", "monte", "numero", "type_pneus", "marque", "actif", "est_monte", "km_cumules")
    list_filter = ("position", "monte", "actif", "type_pneus")


@admin.register(VenteParticulier)
class VenteParticulierAdmin(admin.ModelAdmin):
    list_display = ("vehicule", "statut", "date_vente", "acheteur_nom", "regime_tva", "prix_tvac")
    list_filter = ("statut", "regime_tva")
