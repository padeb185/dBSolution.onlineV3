import re

from django.db.models.functions import Greatest
from django.urls import reverse
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.db import models, transaction
from maindoeuvre.models import MainDoeuvre
from utilisateurs.models import UserLog
from django.contrib import messages
from maintenance.models import Maintenance
from voiture.voiture_exemplaire.models import VoitureExemplaire
from django.utils.translation import gettext_lazy as _, gettext_noop
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.db.models import Q, F
from .forms import RemplacementBoiteForm
from .models import RemplacementBoite
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from weasyprint import HTML, pdf
from django.core.exceptions import ValidationError






@method_decorator([login_required, never_cache], name="dispatch")
class RemplacementBoiteListView(ListView):
    model = RemplacementBoite
    template_name = "remplacement_boite/remplacement_boite_list.html"
    context_object_name = "remplacements"



    def get_queryset(self):
        queryset = RemplacementBoite.objects.select_related(
            "voiture_exemplaire", "maintenance", "tech_societe"
        )

        societe = getattr(self.request.user, "societe", None)
        if societe:
            queryset = queryset.filter(
                models.Q(tech_societe=societe) | models.Q(tech_societe__isnull=True)
            )

        return queryset.order_by("-date")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        exemplaire_id = self.kwargs.get("exemplaire_id")
        if exemplaire_id:
            context["exemplaire"] = VoitureExemplaire.objects.get(id=exemplaire_id)

        roles_autorises = [
            "mecanicien",
            "apprenti",
            "magasinier",
            "chef_mecanicien",
            "direction",
        ]

        context["is_checkup_allowed"] = self.request.user.role in roles_autorises

        return context





@never_cache
@login_required
def remplacement_boite_form_view(request, exemplaire_id):

    remplacement_boite = None
    tenant = request.user.societe
    role = request.user.role

    # 🔎 récupération exemplaire
    exemplaire = get_object_or_404(
        VoitureExemplaire.objects.filter(
            Q(client__societe=tenant) |
            Q(client__isnull=True, societe=tenant)
        ),
        id=exemplaire_id
    )

    # 🔐 rôles autorisés
    roles_autorises = [
        "mecanicien",
        "apprenti",
        "magasinier",
        "chef_mecanicien",
        "direction",
    ]

    if role not in roles_autorises:
        messages.error(request, _("Accès refusé"))
        return redirect("utilisateurs:dashboard")

    # =========================
    # POST
    # =========================
    if request.method == "POST":

        form = RemplacementBoiteForm(
            request.POST,
            user=request.user,
            exemplaire=exemplaire
        )

        if form.is_valid():

            try:
                with transaction.atomic():

                    # ==================================================
                    # VALEURS AVANT INTERVENTION
                    # ==================================================
                    ancien_chassis = exemplaire.kilometres_chassis or 0
                    ancien_moteur = exemplaire.kilometres_moteur or 0
                    ancien_boite = exemplaire.kilometres_boite or 0
                    ancien_embrayage = exemplaire.kilometres_embrayage or 0

                    # ==================================================
                    # NOUVEAU KILOMÉTRAGE
                    # ==================================================
                    nouveau_km = form.cleaned_data.get("kilometres_remplacement")

                    if nouveau_km is None:
                        nouveau_km = ancien_chassis

                    if nouveau_km < ancien_chassis:
                        form.add_error(
                            "kilometres_remplacement",
                            _("Le kilométrage ne peut pas être inférieur au dernier kilométrage.")
                        )
                        raise ValidationError("kilometrage_inferieur")

                    variation = nouveau_km - ancien_chassis

                    # ==================================================
                    # EXEMPLAIRE
                    # ==================================================
                    exemplaire.kilometres_rollback = ancien_chassis
                    exemplaire.kilometres_boite_rollback = ancien_boite
                    exemplaire.kilometres_moteur_rollback = ancien_moteur
                    exemplaire.kilometres_embrayage_rollback = ancien_embrayage

                    exemplaire.date_derniere_intervention = timezone.localtime(timezone.now()).date()
                    exemplaire.kilometres_chassis = nouveau_km

                    # Point de départ de la nouvelle boîte → kilometres_boite = 0
                    exemplaire.kilometres_remplacement_boite = nouveau_km

                    exemplaire.update_kilometres()

                    exemplaire.save(
                        update_fields=[
                            "kilometres_chassis",
                            "date_derniere_intervention",
                            "kilometres_rollback",
                            "kilometres_boite_rollback",
                            "kilometres_moteur_rollback",
                            "kilometres_embrayage_rollback",
                            "kilometres_remplacement_boite",
                            "kilometres_moteur",
                            "kilometres_boite",
                            "kilometres_embrayage",
                            "variation_kilometres",
                        ]
                    )

                    # ==================================================
                    # MAINTENANCE
                    # ==================================================
                    maintenance = Maintenance.objects.create(
                        societe=request.user.societe,
                        voiture_exemplaire=exemplaire,
                        immatriculation=exemplaire.immatriculation,
                        date_intervention=timezone.now().date(),
                        kilometres_chassis=exemplaire.kilometres_chassis,
                        kilometres_dernier_entretien=exemplaire.kilometres_dernier_entretien,
                        type_maintenance=Maintenance.TypeMaintenance.REMPLACEMENT_BOITE,
                        tag=Maintenance.Tag.JAUNE,
                        tech_technicien=request.user,
                        tech_societe=request.user.societe,
                        tech_nom_technicien=f"{request.user.prenom} {request.user.nom}",
                        tech_role_technicien=request.user.role,
                    )

                    if role == "mecanicien":
                        maintenance.mecanicien = request.user
                    elif role == "chef_mecanicien":
                        maintenance.chef_mecanicien = request.user
                    elif role == "apprenti":
                        maintenance.apprentis = request.user

                    maintenance.save()

                    # ==================================================
                    # REMPLACEMENT
                    # ==================================================
                    remplacement_boite = form.save(commit=False)
                    remplacement_boite.voiture_exemplaire = exemplaire
                    remplacement_boite.maintenance = maintenance

                    # Kilométrages au moment de l'intervention
                    remplacement_boite.kilometres_chassis = ancien_chassis
                    remplacement_boite.kilometres_moteur = ancien_moteur
                    remplacement_boite.kilometres_embrayage = ancien_embrayage
                    remplacement_boite.kilometres_boite = ancien_boite + variation  # boîte déposée
                    remplacement_boite.kilometres_remplacement = nouveau_km

                    # Sauvegardes pour la suppression (valeurs AVANT)
                    remplacement_boite.kilometres_rollback = ancien_chassis
                    remplacement_boite.kilometres_boite_rollback = ancien_boite
                    remplacement_boite.kilometres_moteur_rollback = ancien_moteur
                    remplacement_boite.kilometres_embrayage_rollback = ancien_embrayage

                    # ==================================================
                    # MAIN-D'ŒUVRE
                    # ==================================================
                    heures = form.cleaned_data.get("temps_heures") or 0
                    minutes = form.cleaned_data.get("temps_minutes") or 0
                    total_minutes = heures * 60 + minutes
                    taux_horaire = form.cleaned_data.get("taux_horaire") or 0

                    if remplacement_boite.main_oeuvre_id:
                        main_oeuvre = remplacement_boite.main_oeuvre
                        main_oeuvre.temps_minutes = total_minutes
                        main_oeuvre.taux_horaire = taux_horaire
                        main_oeuvre.save(update_fields=["temps_minutes", "taux_horaire"])
                    else:
                        remplacement_boite.main_oeuvre = MainDoeuvre.objects.create(
                            utilisateur=request.user,
                            temps_minutes=total_minutes,
                            taux_horaire=taux_horaire,
                        )

                    remplacement_boite.save()
                    form.save_m2m()

                    # ==================================================
                    # BOÎTE NEUVE = 0 KM
                    # (RemplacementBoite.save() réécrit kilometres_boite)
                    # ==================================================
                    VoitureExemplaire.objects.filter(pk=exemplaire.pk).update(
                        kilometres_boite=0,
                        nombre_remplacements_boites=F("nombre_remplacements_boites") + 1,
                    )

                    # ==================================================
                    # LOG
                    # ==================================================
                    ACTION_REMPLACEMENT_BOITE_VITESSE = gettext_noop(
                        "Remplacement de la boite de vitesse"
                    )

                    UserLog.objects.create(
                        utilisateur=request.user,
                        action=f"{ACTION_REMPLACEMENT_BOITE_VITESSE} - {exemplaire.immatriculation}"
                    )

                messages.success(
                    request,
                    _("Remplacement de la boîte enregistré avec succès")
                )

                return redirect(
                    f"{reverse('remplacement_boite:remplacement_boite_list', kwargs={'exemplaire_id': exemplaire.id})}?saved=1"
                )

            except ValidationError:
                # L'erreur est déjà attachée au champ du formulaire
                messages.error(request, _("Veuillez corriger les erreurs du formulaire"))

            except Exception as e:
                messages.error(request, str(e))

        else:
            messages.error(request, _("Veuillez corriger les erreurs du formulaire"))

    # =========================
    # GET
    # =========================
    else:
        remplacement_boite = RemplacementBoite(
            voiture_exemplaire=exemplaire,
            kilometres_chassis=exemplaire.kilometres_chassis or 0,
            kilometres_moteur=exemplaire.kilometres_moteur or 0,
            kilometres_boite=exemplaire.kilometres_boite or 0,
            kilometres_embrayage=exemplaire.kilometres_embrayage or 0,
        )

        remplacement_boite.assign_technicien(request.user)

        form = RemplacementBoiteForm(
            instance=remplacement_boite,
            user=request.user,
            exemplaire=exemplaire
        )

    # =========================
    # SECTIONS UI
    # =========================
    sections = [
        {
            "title": _("Kilométrage"),
            "icon": "icons/compteur.png",
            "fields": [form[f.name] for f in form if "kilo" in f.name],
        },
        {
            "title": _("Remplacement de la boite"),
            "icon": "icons/boite-de-vitesse.png",
            "fields": [form[f.name] for f in form if "remplacement_boite" in f.name],
        },
        {
            "title": _("Niveau de la boite de vitesse"),
            "icon": "icons/niveaux.png",
            "fields": [form[f.name] for f in form if "boite_niveau" in f.name],
        },
        {
            "title": _("Remise à zéro"),
            "icon": "icons/km.png",
            "fields": [form[f.name] for f in form if "remplacement_effectue" in f.name],
        },
        {
            "title": _("Pays"),
            "icon": "icons/pays.png",
            "fields": [form[f.name] for f in form if "pays" in f.name],
        },
        {
            "title": _("Étiquette"),
            "icon": "icons/tag.png",
            "fields": [form[f.name] for f in form if "tag" in f.name],
        },
        {
            "title": _("Remarques"),
            "icon": "icons/notes.png",
            "fields": [form[f.name] for f in form if "remarques" in f.name],
        },
        {
            "title": _("Serrage des roues"),
            "icon": "icons/roue.png",
            "fields": [form[f.name] for f in form if "serrage" in f.name],
        },
        {
            "title": _("Technicien"),
            "icon": "icons/mecanicien.png",
            "fields": [form[f.name] for f in form if "tech" in f.name],
        },
        {
            "title": _("Taux horaire"),
            "icon": "icons/taux.png",
            "fields": [form[f.name] for f in form if "taux" in f.name],
        },
    ]

    return render(request, "remplacement_boite/remplacement_boite_form.html", {
        "remplacement_boite": remplacement_boite,
        "form": form,
        "exemplaire": exemplaire,
        "sections": sections,
        "now": timezone.now(),
    })





@login_required
def remplacement_boite_detail_view(request, remplacement_boite_id):
    remplacement_boite = get_object_or_404(
        RemplacementBoite.objects.select_related("voiture_exemplaire"),
        id=remplacement_boite_id
    )

    context = {
        "remplacement_boite": remplacement_boite,
        "exemplaire": remplacement_boite.voiture_exemplaire,
    }
    return render(request, "remplacement_boite/remplacement_boite_detail.html", context)






@login_required
def modifier_remplacement_boite_view(request, remplacement_boite_id):

    remplacement_boite = get_object_or_404(
        RemplacementBoite.objects.select_related("voiture_exemplaire"),
        id=remplacement_boite_id,
    )

    exemplaire = remplacement_boite.voiture_exemplaire

    # ==================================================
    # VALEURS ENREGISTRÉES (lues en base, avant le formulaire)
    # ==================================================
    original = RemplacementBoite.objects.get(pk=remplacement_boite.pk)

    if original.kilometres_rollback:
        # Remplacement récent : sauvegardes remplies à la création
        avant_chassis = original.kilometres_rollback
        avant_boite = original.kilometres_boite_rollback or 0
        avant_moteur = original.kilometres_moteur_rollback or 0
        avant_embrayage = original.kilometres_embrayage_rollback or 0
    else:
        # Ancien remplacement : les champs contiennent les valeurs d'avant
        avant_chassis = original.kilometres_chassis or 0
        avant_boite = original.kilometres_boite or 0
        avant_moteur = original.kilometres_moteur or 0
        avant_embrayage = original.kilometres_embrayage or 0

    ancien_km_remplacement = original.kilometres_remplacement or avant_chassis
    ancienne_boite_deposee = original.kilometres_boite or 0

    if request.method == "POST":

        form = RemplacementBoiteForm(
            request.POST,
            instance=remplacement_boite,
            user=request.user,
            exemplaire=exemplaire,
        )

        if form.is_valid():
            try:
                with transaction.atomic():

                    # ==================================================
                    # KILOMÉTRAGE DU REMPLACEMENT (formulaire)
                    # ==================================================
                    km = form.cleaned_data.get("kilometres_remplacement")
                    km = int(km) if km is not None else ancien_km_remplacement

                    if km < avant_chassis:
                        form.add_error(
                            "kilometres_remplacement",
                            _("Le kilométrage ne peut pas être inférieur à %(km)s km.")
                            % {"km": avant_chassis},
                        )
                        raise ValidationError("kilometrage_inferieur")

                    variation = km - avant_chassis

                    # ==================================================
                    # BOÎTE DÉPOSÉE : valeur du formulaire,
                    # jamais inférieure à la valeur enregistrée
                    # ==================================================
                    boite_form = form.cleaned_data.get("kilometres_boite")

                    if boite_form is None:
                        boite_form = avant_boite + variation

                    boite_deposee = max(int(boite_form), ancienne_boite_deposee)

                    # ==================================================
                    # REMPLACEMENT
                    # ==================================================
                    remplacement_boite = form.save(commit=False)
                    remplacement_boite.voiture_exemplaire = exemplaire

                    remplacement_boite.kilometres_chassis = avant_chassis
                    remplacement_boite.kilometres_moteur = avant_moteur
                    remplacement_boite.kilometres_embrayage = avant_embrayage
                    remplacement_boite.kilometres_boite = boite_deposee
                    remplacement_boite.kilometres_remplacement = km

                    # Les sauvegardes ne changent jamais en modification
                    remplacement_boite.kilometres_rollback = original.kilometres_rollback
                    remplacement_boite.kilometres_boite_rollback = original.kilometres_boite_rollback
                    remplacement_boite.kilometres_moteur_rollback = original.kilometres_moteur_rollback
                    remplacement_boite.kilometres_embrayage_rollback = original.kilometres_embrayage_rollback

                    remplacement_boite.assign_technicien(request.user)
                    remplacement_boite.tech_last_maintained_by = request.user

                    remplacement_boite.save()
                    form.save_m2m()

                    # ==================================================
                    # EXEMPLAIRE (écrit EN DERNIER, après save())
                    # ==================================================
                    chassis_actuel = exemplaire.kilometres_chassis or 0

                    # Rien n'a bougé depuis ce remplacement ?
                    est_derniere = chassis_actuel == ancien_km_remplacement

                    if est_derniere:
                        nouveau_chassis = km
                        nouveau_moteur = avant_moteur + variation
                        nouvel_embrayage = avant_embrayage + variation
                    else:
                        nouveau_chassis = chassis_actuel
                        nouveau_moteur = exemplaire.kilometres_moteur or 0
                        nouvel_embrayage = exemplaire.kilometres_embrayage or 0

                    # Boîte neuve : kilomètres parcourus depuis le remplacement
                    nouvelle_boite = max(0, nouveau_chassis - km)

                    VoitureExemplaire.objects.filter(pk=exemplaire.pk).update(
                        kilometres_chassis=nouveau_chassis,
                        kilometres_remplacement_boite=km,
                        kilometres_boite=nouvelle_boite,
                        kilometres_moteur=nouveau_moteur,
                        kilometres_embrayage=nouvel_embrayage,
                        date_derniere_intervention=timezone.localtime(timezone.now()).date(),
                    )

                    # ==================================================
                    # LOG
                    # ==================================================
                    ACTION_MODIFICATION_REMPLACEMENT_BOITE_VITESSE = gettext_noop(
                        "Modification du remplacement de la boite de vitesse"
                    )

                    UserLog.objects.create(
                        utilisateur=request.user,
                        action=f"{ACTION_MODIFICATION_REMPLACEMENT_BOITE_VITESSE} - {exemplaire.immatriculation}",
                    )

                messages.success(request, _("Remplacement de la boite modifié avec succès !"))

                return redirect(
                    f"{reverse('remplacement_boite:remplacement_boite_detail', kwargs={'remplacement_boite_id': remplacement_boite.id})}?saved=1"
                )

            except ValidationError:
                messages.error(request, _("Kilométrage invalide"))

        else:
            messages.error(request, _("Le formulaire contient des erreurs."))

    else:
        form = RemplacementBoiteForm(
            instance=remplacement_boite,
            user=request.user,
            exemplaire=exemplaire,
        )

    # -------------------------
    # SECTIONS
    # -------------------------
    sections = [
        {
            "title": _("Kilométrage"),
            "icon": "icons/compteur.png",
            "fields": [form[f.name] for f in form if "kilo" in f.name],
        },
        {
            "title": _("Remplacement de la boite de vitesse"),
            "icon": "icons/boite-de-vitesse.png",
            "fields": [form[f.name] for f in form if "remplacement_boite" in f.name],
        },
        {
            "title": _("Niveau de la boite de vitesse"),
            "icon": "icons/niveaux.png",
            "fields": [form[f.name] for f in form if "boite_niveau" in f.name],
        },
        {
            "title": _("Remise à Zéro des kilomètres de la boite de vitesse"),
            "icon": "icons/km.png",
            "fields": [form[f.name] for f in form if "remplacement_effectue" in f.name],
        },
        {
            "title": _("Pays"),
            "icon": "icons/pays.png",
            "fields": [form[f.name] for f in form if "pays" in f.name],
        },
        {
            "title": _("Etiquette"),
            "icon": "icons/tag.png",
            "fields": [form[f.name] for f in form if "tag" in f.name],
        },
        {
            "title": _("Remarques"),
            "icon": "icons/notes.png",
            "fields": [form[f.name] for f in form if "remarques" in f.name],
        },
        {
            "title": _("Serrage des roues"),
            "icon": "icons/roue.png",
            "fields": [form[f.name] for f in form if "serrage" in f.name],
        },
        {
            "title": _("Technicien"),
            "icon": "icons/mecanicien.png",
            "fields": [form[f.name] for f in form if "tech" in f.name],
        },
        {
            "title": _("Taux horaire"),
            "icon": "icons/taux.png",
            "fields": [form[f.name] for f in form if "taux" in f.name],
        },
    ]

    return render(request, "remplacement_boite/modifier_remplacement_boite.html", {
        "remplacement_boite": remplacement_boite,
        "form": form,
        "sections": sections,
        "exemplaire": exemplaire,
    })





@never_cache
@login_required
def delete_remplacement_boite_view(request, remplacement_boite_id):

    tenant = request.user.societe
    role = request.user.role

    # ==================================================
    # AUTORISATIONS
    # ==================================================
    roles_autorises = [
        "direction",
        "chef_mecanicien",
    ]

    if role not in roles_autorises and not request.user.is_superuser:
        messages.error(request, _("Accès refusé"))
        return redirect("utilisateurs:dashboard")

    # ==================================================
    # RÉCUPÉRATION DU REMPLACEMENT
    # ==================================================
    remplacement_boite = get_object_or_404(
        RemplacementBoite.objects.select_related(
            "voiture_exemplaire",
            "maintenance",
        ),
        id=remplacement_boite_id,
    )

    exemplaire = remplacement_boite.voiture_exemplaire
    maintenance = remplacement_boite.maintenance

    # ==================================================
    # VÉRIFICATION TENANT
    # ==================================================
    if not (
        (exemplaire.client and exemplaire.client.societe == tenant)
        or (exemplaire.client is None and exemplaire.societe == tenant)
    ):
        messages.error(request, _("Accès refusé"))
        return redirect("utilisateurs:dashboard")

    # ==================================================
    # DELETE
    # ==================================================
    if request.method == "POST":

        try:
            with transaction.atomic():

                immatriculation = exemplaire.immatriculation
                r = remplacement_boite

                # ------------------------------------------
                # Valeurs AVANT intervention
                # ------------------------------------------
                if r.kilometres_rollback:
                    # Remplacement récent : sauvegardes remplies à la création
                    km_chassis = r.kilometres_rollback
                    km_boite = r.kilometres_boite_rollback or 0
                    km_moteur = r.kilometres_moteur_rollback or 0
                    km_embrayage = r.kilometres_embrayage_rollback or 0
                else:
                    # Ancien remplacement : les champs contiennent déjà
                    # les valeurs d'avant l'intervention
                    km_chassis = r.kilometres_chassis or 0
                    km_boite = r.kilometres_boite or 0
                    km_moteur = r.kilometres_moteur or 0
                    km_embrayage = r.kilometres_embrayage or 0

                # ------------------------------------------
                # Restauration directe en base
                # ------------------------------------------
                VoitureExemplaire.objects.filter(pk=exemplaire.pk).update(
                    kilometres_chassis=km_chassis,
                    kilometres_boite=km_boite,
                    kilometres_moteur=km_moteur,
                    kilometres_embrayage=km_embrayage,
                    kilometres_remplacement_boite=max(0, km_chassis - km_boite),
                    nombre_remplacements_boites=Greatest(
                        F("nombre_remplacements_boites") - 1, 0
                    ),
                )

                # ------------------------------------------
                # Suppression
                # ------------------------------------------
                remplacement_boite.delete()

                if maintenance:
                    maintenance.delete()

                ACTION_SUPPRESSION_REMPLACEMENT_BOITE = gettext_noop(
                    "Suppression du remplacement de la boite de vitesse"
                )

                UserLog.objects.create(
                    utilisateur=request.user,
                    action=f"{ACTION_SUPPRESSION_REMPLACEMENT_BOITE} - {immatriculation}",
                )

            messages.success(
                request,
                _("Remplacement de la boite supprimé avec succès.")
            )

            return redirect(
                f"{reverse('remplacement_boite:remplacement_boite_list', kwargs={'exemplaire_id': exemplaire.id})}?deleted=1"
            )

        except Exception as e:
            messages.error(
                request,
                _("Erreur lors de la suppression : %(erreur)s") % {"erreur": str(e)}
            )

    # ==================================================
    # GET → CONFIRMATION
    # ==================================================
    return render(
        request,
        "remplacement_boite/delete_remplacement_boite.html",
        {
            "remplacement_boite": remplacement_boite,
            "exemplaire": exemplaire,
        },
    )







@login_required
def remplacement_boite_pdf_view(request, remplacement_boite_id):
    tenant = request.user.societe


    remplacement = get_object_or_404(
        RemplacementBoite.objects.select_related(
            "voiture_exemplaire",
            "voiture_exemplaire__voiture_marque",
            "voiture_exemplaire__voiture_modele",
            "client",
            "tech_technicien",
            "tech_societe",
            "main_oeuvre",
            "main_oeuvre__utilisateur",
            "maintenance",
        ),
        pk=remplacement_boite_id,
    )

    vehicule = remplacement.voiture_exemplaire
    maintenance = remplacement.maintenance

    # Rapport des pièces et produits
    rapport = remplacement.generer_rapport_remplacement()

    lignes_rapport = rapport.get("lignes", [])
    total_pieces = rapport.get("total_general", 0)

    # Informations pour le nom du fichier
    immatriculation = (
        vehicule.immatriculation
        if vehicule and vehicule.immatriculation
        else "sans_immatriculation"
    )

    technicien = (
        remplacement.tech_nom_technicien
        or (
            str(remplacement.tech_technicien)
            if remplacement.tech_technicien
            else "technicien_inconnu"
        )
    )

    html_string = render_to_string(
        "remplacement_boite/remplacement_boite_detail_pdf.html",
        {
            "remplacement": remplacement,
            "rapport": rapport,
            "lignes_rapport": lignes_rapport,
            "pieces_utilisees": lignes_rapport,
            "total_pieces": total_pieces,
            "cout_main_oeuvre": remplacement.cout_main_oeuvre,
            "total_general": (
                remplacement.total_general_avec_main_oeuvre
            ),
            "societe": tenant,
            "maintenance": maintenance,
            "vehicule": vehicule,
            "immatriculation": immatriculation,
            "technicien": technicien,
            "date_export": timezone.now(),
        },
        request=request,
    )

    pdf = HTML(
        string=html_string,
        base_url=request.build_absolute_uri("/"),
    ).write_pdf()

    # =========================================================
    # IMMATRICULATION
    # =========================================================

    immatriculation = (
        remplacement.voiture_exemplaire.immatriculation
        if remplacement.voiture_exemplaire
        else "sans_immatriculation"
    )

    # =========================================================
    # TECHNICIEN
    # =========================================================

    technicien = (
            remplacement.tech_nom_technicien
            or "technicien_inconnu"
    )

    # Nettoyage pour le nom du fichier
    technicien = str(technicien).replace(" ", "_")
    immatriculation = str(immatriculation).replace(" ", "_")

    # =========================================================
    # DATE
    # =========================================================

    date_pdf = (
        remplacement.date.strftime("%Y-%m-%d")
        if remplacement.date
        else timezone.now().strftime("%Y-%m-%d")
    )

    # =========================================================
    # TITRE / NOM DU PDF
    # =========================================================

    nom_fichier = (
        f"{_('Remplacement boite')}_{technicien}_{immatriculation}_{date_pdf}.pdf"
    )

    response = HttpResponse(
        pdf,
        content_type="application/pdf",
    )

    response["Content-Disposition"] = (
        f'inline; filename="{nom_fichier}"'
    )

    return response