from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django_tenants.utils import tenant_context
from django.contrib import messages
from django.db import transaction
from django.urls import reverse

from maintenance.models import Maintenance
from maintenance.check_up.models import (
    ControleGeneral, AmortisseurControle, RessortControle, ControleBruit, JeuPiece,
    ControleFreins, NettoyageExterieur, NettoyageInterieur, NoteMaintenance
)
from voiture.voiture_exemplaire.models import VoitureExemplaire
from utilisateurs.models import Utilisateur, Mecanicien
from django.utils.translation import gettext_lazy as _

@login_required
def controle_total_view(request, exemplaire_id):
    tenant = request.user.societe

    with tenant_context(tenant):
        # Récupération de l'exemplaire
        exemplaire = get_object_or_404(
            VoitureExemplaire.objects.filter(
                Q(client__societe=tenant) | Q(client__isnull=True, societe=tenant)
            ),
            id=exemplaire_id
        )

        # Vérifie que l'utilisateur est mécanicien
        if request.user.role != "mécanicien":
            messages.error(request, _("Seuls les mécaniciens peuvent accéder à cette page."))
            return redirect("maintenance_liste_all")

        mecanicien = get_object_or_404(Mecanicien, id=request.user.id)

        # Récupération ou création de la maintenance
        maintenance, _ = Maintenance.objects.get_or_create(
            exemplaire=exemplaire,
            defaults={
                "mecanicien": mecanicien,
                "immatriculation": exemplaire.immatriculation,
                "date_intervention": timezone.now().date(),
                "kilometres_total": exemplaire.kilometres_total,
                "kilometres_derniere_intervention": exemplaire.kilometres_derniere_intervention,
                "type_maintenance": "checkup",
                "tag": Maintenance.Tag.JAUNE,
            }
        )

        # Récupération ou création du contrôle général
        controle_general, _ = ControleGeneral.objects.get_or_create(maintenance=maintenance)

        # --- POST handling ---
        if request.method == "POST":
            try:
                with transaction.atomic():
                    # --- Contrôles généraux ---
                    controle_general.essuie_glace_av = request.POST.get("essuie_glace_av") == "on"
                    controle_general.essuie_glace_ar = request.POST.get("essuie_glace_ar") == "on"
                    controle_general.pare_brise = request.POST.get("pare_brise") == "on"
                    controle_general.moteur_fuite = request.POST.get("moteur_fuite") or "OK"
                    controle_general.boite_fuite = request.POST.get("boite_fuite") or "OK"
                    controle_general.liquide_frein_etat = request.POST.get("liquide_frein_etat") or "OK"
                    controle_general.remplacement_liquide_frein = request.POST.get("remplacement_liquide_frein") == "on"
                    controle_general.save()

                    # --- Amortisseurs ---
                    for amortisseur in controle_general.amortisseurs_checkup.all():
                        field_name = f"amortisseur_{amortisseur.emplacement}"
                        amortisseur.fuite = request.POST.get(field_name) == "on"
                        amortisseur.save()

                    # --- Ressorts ---
                    for ressort in controle_general.ressorts.all():
                        field_name = f"ressort_{ressort.emplacement}"
                        ressort.etat = request.POST.get(field_name) or "OK"
                        ressort.save()

                    # --- Bruits ---
                    for bruit in controle_general.bruits_checkup.all():
                        field_name = f"bruit_{bruit.id}_niveau"
                        bruit.niveau_bruit = request.POST.get(field_name, "NORMAL")
                        bruit.commentaire = request.POST.get(f"bruit_{bruit.id}_commentaire", "")
                        bruit.save()

                    # --- Pièces ---
                    for piece in maintenance.jeux_pieces_checkup.all():
                        field_name = f"piece_{piece.id}_etat"
                        piece.etat = request.POST.get(field_name) or piece.etat
                        piece.save()

                    # --- Freins ---
                    for frein in maintenance.controle_freins_checkup.all():
                        frein.usure_plaquettes = float(request.POST.get(f"frein_{frein.id}_usure", frein.usure_plaquettes))
                        frein.epaisseur_disques = float(request.POST.get(f"frein_{frein.id}_epaisseur", frein.epaisseur_disques))
                        frein.fentes_disques = request.POST.get(f"frein_{frein.id}_fentes") == "on"
                        frein.fuites = request.POST.get(f"frein_{frein.id}_fuites") == "on"
                        frein.save()

                    # --- Nettoyage Extérieur ---
                    nettoyage_ext = maintenance.nettoyages_exterieur_nettoyage_exterieur.first()
                    if nettoyage_ext:
                        nettoyage_ext.traces_gomme = request.POST.get("nettoyage_traces_gomme") == "on"
                        nettoyage_ext.carrosserie = request.POST.get("nettoyage_carrosserie") == "on"
                        nettoyage_ext.jantes = request.POST.get("nettoyage_jantes") == "on"
                        nettoyage_ext.save()

                    # --- Nettoyage Intérieur ---
                    nettoyage_int = maintenance.nettoyages_interieur_checkup.first()
                    if nettoyage_int:
                        nettoyage_int.vitres = request.POST.get("nettoyage_vitres") == "on"
                        nettoyage_int.pare_brise = request.POST.get("nettoyage_pare_brise") == "on"
                        nettoyage_int.aspirateur = request.POST.get("nettoyage_aspirateur") == "on"
                        nettoyage_int.tableau_de_bord = request.POST.get("nettoyage_tableau") == "on"
                        nettoyage_int.save()

                    messages.success(request, _("Maintenance mise à jour avec succès."))
                    return redirect(reverse("controle_total_view", args=[exemplaire.id]))

            except Exception as e:
                messages.error(request, _("Erreur lors de l'enregistrement : ") + str(e))

        context = {
            "exemplaire": exemplaire,
            "maintenance": maintenance,
            "now": timezone.now(),
        }

        return render(request, "maintenance/controle_total.html", context)