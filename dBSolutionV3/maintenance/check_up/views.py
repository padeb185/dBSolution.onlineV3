from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django_tenants.utils import tenant_context

from maintenance.models import Maintenance
from maintenance.check_up.models import (
    ControleGeneral, AmortisseurControle, RessortControle, ControleBruit, JeuPiece,
    ControleFreins, NettoyageInterieur, NettoyageExterieur, NoteMaintenance
)
from voiture.voiture_exemplaire.models import VoitureExemplaire
from utilisateurs.models import Utilisateur
from django.utils.translation import gettext_lazy as _
from utilisateurs.models import Mecanicien


from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import ( Maintenance, ControleGeneral, AmortisseurControle, RessortControle,
    ControleBruit, JeuPiece, ControleFreins, NettoyageExterieur, NettoyageInterieur,
    NoteMaintenance
)



@login_required
def creer_checkup_complet(request, exemplaire_id):
    tenant = request.user.societe

    with tenant_context(tenant):
        # Récupère l'exemplaire
        exemplaire = get_object_or_404(VoitureExemplaire, id=exemplaire_id)

        # Vérifie que l'utilisateur est mécanicien
        if request.user.role != "mécanicien":
            raise PermissionError("Seuls les mécaniciens peuvent créer un check-up")

        mecanicien = get_object_or_404(Mecanicien, id=request.user.id)

        # --- Création de la maintenance ---
        maintenance = Maintenance.objects.create(
            voiture_exemplaire=exemplaire,
            mecanicien=mecanicien,
            immatriculation=exemplaire.immatriculation,
            date_intervention=timezone.now().date(),
            kilometres_total=exemplaire.kilometres_total,
            kilometres_derniere_intervention=exemplaire.kilometres_derniere_intervention,
            type_maintenance="checkup",
            tag=Maintenance.Tag.JAUNE,
        )

        # --- Création des contrôles ---
        controle_general = ControleGeneral.objects.create(maintenance=maintenance)

        # Amortisseurs et ressorts
        for loc in ["AVG", "AVD", "ARG", "ARD"]:
            AmortisseurControle.objects.create(controle_general=controle_general, emplacement=loc)
            RessortControle.objects.create(controle_general=controle_general, emplacement=loc)

        # Bruits
        for loc in ["AVG", "AVD", "ARG", "ARD"]:
            for type_bruit in ["ROULEMENT_ROUE", "ROULEMENT_SUSPENSION", "MOTEUR", "BOITE_VITESSE", "PONT"]:
                ControleBruit.objects.create(maintenance=maintenance, emplacement=loc, type_bruit=type_bruit)

        # Pièces
        for loc in ["AVG", "AVD", "ARG", "ARD"]:
            for piece in ["ROTULE_DIRECTION", "ROTULE_SUSPENSION", "BIELLETTE_BARRE_STAB",
                          "BARRE_STABILISATRICE", "AMORTISSEUR", "ROULEMENT_ROUE",
                          "TRIANGLE", "MULTI_BRAS"]:
                JeuPiece.objects.create(maintenance=maintenance, vehicle=exemplaire, type_piece=piece, emplacement=loc)

        # Freins
        for partie in ["AVANT", "ARRIERE", "AV_AR"]:
            ControleFreins.objects.create(maintenance=maintenance, partie=partie, usure_plaquettes=0.0, epaisseur_disques=100.0)

        # Nettoyage
        NettoyageExterieur.objects.create(maintenance=maintenance, voiture_exemplaire=exemplaire, mecanicien=mecanicien)
        NettoyageInterieur.objects.create(maintenance=maintenance, voiture_exemplaire=exemplaire, mecanicien=mecanicien)

        # Note initiale
        NoteMaintenance.objects.create(
            maintenance=maintenance,
            auteur=mecanicien,
            role="MECANICIEN",
            note="Check-up initial créé automatiquement"
        )

        # Redirection vers la page de détail de la maintenance (ou autre page)
        return redirect('maintenance_detail', maintenance_id=maintenance.id)




@login_required
def detail_exemplaire_maintenance(request, exemplaire_id):
    tenant = request.user.societe
    with tenant_context(tenant):
        exemplaire = get_object_or_404(VoitureExemplaire, id=exemplaire_id)

    return render(request, "maintenance/exemplaire_detail.html", {
        "exemplaire": exemplaire,
    })




# Types possibles de maintenance
TYPES_MAINTENANCE = [
    {"code": "checkup", "nom": _("Checkup")},
    {"code": "entretien", "nom": _("Entretien")},
    {"code": "freins", "nom": _("Freins")},
    {"code": "pneus", "nom": _("Pneus")},
    {"code": "nettoyage_ext", "nom": _("Nettoyage extérieur")},
    {"code": "nettoyage_int", "nom": _("Nettoyage intérieur")},
    {"code": "niveaux", "nom": _("Niveaux")},
    {"code": "autres", "nom": _("Autres interventions")},
]






