import re
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
        "direction"
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
        remplacement_boite = RemplacementBoite(
            voiture_exemplaire=exemplaire
        )

        if form.is_valid():

            try:
                with transaction.atomic():

                    # ==========================================================
                    # VALEURS AVANT MODIFICATION
                    # ==========================================================
                    ancien_km_chassis = (
                            exemplaire.kilometres_chassis
                            or 0
                    )

                    ancien_kilometrage = (
                            exemplaire.kilometres_chassis
                            or 0
                    )

                    ancien_kilometrage_moteur = (
                            exemplaire.kilometres_moteur
                            or 0
                    )

                    ancien_kilometrage_boite = (
                            exemplaire.kilometres_boite
                            or 0
                    )

                    # ==========================================================
                    # NOUVEAU KILOMÉTRAGE
                    # ==========================================================
                    nouveau_km = form.cleaned_data.get(
                        "kilometres_remplacement"
                    )

                    # ==========================================================
                    # VALIDATION
                    # ==========================================================
                    if (
                            nouveau_km is not None
                            and nouveau_km < ancien_km_chassis
                    ):
                        form.add_error(
                            "kilometres_remplacement",
                            _(
                                "Le kilométrage ne peut pas être "
                                "inférieur au dernier kilométrage."
                            )
                        )

                        raise ValidationError(
                            _(
                                "Le kilométrage ne peut pas être "
                                "inférieur au dernier kilométrage."
                            )
                        )

                    # ==========================================================
                    # VARIATION
                    # ==========================================================
                    kilometrage_variation = (
                            nouveau_km - ancien_kilometrage
                    )

                    # ==========================================================
                    # ROLLBACK CHÂSSIS
                    # ==========================================================
                    exemplaire.kilometres_rollback = (
                        ancien_kilometrage
                    )

                    # ==========================================================
                    # ROLLBACK KILOMÉTRAGE BOÎTE
                    #
                    # Sauvegarde UNE SEULE FOIS du kilométrage boîte actuel.
                    # ==========================================================
                    if nouveau_km is not None:

                        if exemplaire.kilometres_boite_rollback is None:
                            exemplaire.kilometres_boite_rollback = (
                                ancien_kilometrage_boite
                            )

                    # ==========================================================
                    # DATE INTERVENTION
                    # ==========================================================
                    exemplaire.date_derniere_intervention = (
                        timezone.localtime(
                            timezone.now()
                        ).date()
                    )

                    # ==========================================================
                    # NOUVEAU KILOMÉTRAGE CHÂSSIS
                    # ==========================================================
                    exemplaire.kilometres_chassis = nouveau_km

                    # Recalcule :
                    # - kilometres_moteur
                    # - kilometres_boite
                    # - variation_kilometres
                    exemplaire.update_kilometres()

                    # ==========================================================
                    # SAUVEGARDE VÉHICULE
                    # ==========================================================
                    exemplaire.save(
                        update_fields=[
                            "kilometres_chassis",
                            "date_derniere_intervention",

                            "kilometres_rollback",
                            "kilometres_boite_rollback",

                            "kilometres_moteur",
                            "kilometres_boite",
                            "variation_kilometres",
                        ]
                    )


                    # 🔴 maintenance unique
                    maintenance = Maintenance.objects.create(
                        societe=request.user.societe,
                        voiture_exemplaire=exemplaire,
                        immatriculation=exemplaire.immatriculation,
                        date_intervention=timezone.now().date(),
                        kilometres_chassis=exemplaire.kilometres_chassis,
                        kilometres_dernier_entretien=exemplaire.kilometres_dernier_entretien,
                        type_maintenance=Maintenance.TypeMaintenance.REMPLACEMENT_BOITE,
                        tag=Maintenance.Tag.JAUNE,
                    )

                    # 🔧 rôle
                    if role == "mecanicien":
                        maintenance.mecanicien = request.user
                    elif role == "chef_mecanicien":
                        maintenance.chef_mecanicien = request.user
                    elif role == "apprenti":
                        maintenance.apprentis.add(request.user)
                    elif role == "magasinier":
                        maintenance.magasinier = request.user
                    elif role == "direction":
                        maintenance.direction = request.user

                    maintenance.save()

                    remplacement_boite = form.save(commit=False)

                    remplacement_boite.voiture_exemplaire = (
                        exemplaire
                    )

                    remplacement_boite.maintenance = (
                        maintenance
                    )

                    # ==========================================================
                    # KILOMÉTRAGES AVANT INTERVENTION
                    # ==========================================================
                    remplacement_boite.kilometres_chassis = (
                        ancien_kilometrage
                    )

                    remplacement_boite.kilometres_moteur = (
                        ancien_kilometrage_moteur
                    )

                    remplacement_boite.kilometres_boite = (
                        ancien_kilometrage_boite
                    )

                    # ==========================================================
                    # KILOMÉTRAGE DU REMPLACEMENT
                    # ==========================================================
                    remplacement_boite.kilometres_remplacement = (
                        nouveau_km
                    )

                    # ==========================================================
                    # VARIATION
                    # ==========================================================
                    remplacement_boite.kilometrage_variation = (
                        kilometrage_variation
                    )

                    # ==================================================
                    # MAIN-D'ŒUVRE
                    # ==================================================
                    heures = (
                            form.cleaned_data.get("temps_heures")
                            or 0
                    )

                    minutes = (
                            form.cleaned_data.get("temps_minutes")
                            or 0
                    )

                    total_minutes = (
                            heures * 60 + minutes
                    )

                    taux_horaire = (
                            form.cleaned_data.get("taux_horaire")
                            or 0
                    )

                    # --------------------------------------------------
                    # Mise à jour main-d'œuvre existante
                    # --------------------------------------------------
                    if remplacement_boite.main_oeuvre_id:

                        main_oeuvre = (
                            remplacement_boite.main_oeuvre
                        )

                        main_oeuvre.temps_minutes = (
                            total_minutes
                        )

                        main_oeuvre.taux_horaire = (
                            taux_horaire
                        )

                        main_oeuvre.save(
                            update_fields=[
                                "temps_minutes",
                                "taux_horaire",
                            ]
                        )

                    # --------------------------------------------------
                    # Création main-d'œuvre
                    # --------------------------------------------------
                    else:

                        main_oeuvre = (
                            MainDoeuvre.objects.create(
                                utilisateur=request.user,
                                temps_minutes=total_minutes,
                                taux_horaire=taux_horaire,
                            )
                        )

                        remplacement_boite.main_oeuvre = (
                            main_oeuvre
                        )

                    # ==================================================
                    # SAUVEGARDE remplacement_boite
                    # IMPORTANT :
                    # EN DEHORS DU IF/ELSE MAIN-D'ŒUVRE
                    # ==================================================
                    remplacement_boite.save()

                    form.save_m2m()



                    ACTION_REMPLACEMENT_BOITE_VITESSE = gettext_noop(
                        "Remplacement de la boite de vitesse"
                    )

                    UserLog.objects.create(
                        utilisateur=request.user,
                        action=f"{ACTION_REMPLACEMENT_BOITE_VITESSE} - {exemplaire.immatriculation}"
                    )
                    # ➕ compteur (si champ existe)
                    if remplacement_boite.pk:
                        exemplaire.nombre_remplacements_boites = F("nombre_remplacements_boites") + 1
                        exemplaire.save(update_fields=["nombre_remplacements_boites"])
                        exemplaire.refresh_from_db()

                messages.success(
                    request,
                    _("Remplacement de la boîte enregistré avec succès")
                )
                return redirect(
                    "remplacement_boite:remplacement_boite_list",
                    exemplaire_id=exemplaire.id,
                )

            except Exception as e:
                messages.error(request, str(e))

        else:
            messages.error(request, _("Veuillez corriger les erreurs du formulaire"))
            print(form.errors)  # 🔥 DEBUG IMPORTANT

    # =========================
    # GET
    # =========================
    else:
        remplacement_boite = RemplacementBoite(
            voiture_exemplaire=exemplaire,
            kilometres_chassis=(
                    exemplaire.kilometres_chassis
                    or 0
            ),

            kilometres_moteur=(
                    exemplaire.kilometres_moteur
                    or 0
            ),
            kilometres_boite=(
                    exemplaire.kilometres_boite or 0
            ),
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
            "fields": [
                form[f.name]
                for f in form
                if "serrage" in f.name
            ],
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





from django.core.exceptions import ValidationError

@login_required
def modifier_remplacement_boite_view(request, remplacement_boite_id):
    tenant = request.user.societe

    remplacement_boite = get_object_or_404(
        RemplacementBoite.objects.select_related(
            "voiture_exemplaire"
        ),
        id=remplacement_boite_id
    )

    exemplaire = remplacement_boite.voiture_exemplaire

    # ==========================================================
    # VALEUR BOÎTE ENREGISTRÉE LORS DE LA CRÉATION
    # ==========================================================
    ancien_kilometrage_boite = (
        remplacement_boite.kilometres_boite
        if remplacement_boite.kilometres_boite is not None
        else (exemplaire.kilometres_boite or 0)
    )

    # ==========================================================
    # KILOMÉTRAGE boite DE RÉFÉRENCE
    #
    # Cette valeur vient de remplacement_boite_form_view
    # et ne doit PAS être recalculée lors d'une modification.
    # ==========================================================
    km_boite_reference = remplacement_boite.kilometres_boite_rollback

    if request.method == "POST":
        form = RemplacementBoiteForm(
            request.POST,
            instance=remplacement_boite,
            user=request.user,
            exemplaire=exemplaire
        )

        if form.is_valid():
            try:
                with transaction.atomic():

                    remplacement = form.save(commit=False)

                    # ======================================================
                    # NE PAS PERDRE LE KILOMÉTRAGE BOÎTE D'ORIGINE
                    # ======================================================
                    remplacement.kilometres_boite = (
                        ancien_kilometrage_boite
                    )

                    remplacement.save()
                    form.save_m2m()

                ACTION_MODIFICATION_REMPLACEMENT_BOITE_VITESSE = gettext_noop(
                    "Modification du remplacement de la boite de vitesse"
                )

                UserLog.objects.create(
                    utilisateur=request.user,
                    action=f"{ACTION_MODIFICATION_REMPLACEMENT_BOITE_VITESSE} - {exemplaire.immatriculation}"
                )

                messages.success(request, _("Remplacement de la boite modifié avec succès !"))

                return redirect(
                    "remplacement_boite:remplacement_boite_detail",
                    remplacement_boite_id=remplacement_boite.id
                )

            except ValidationError as e:
                form.add_error(None, e)
                messages.error(request, _("Kilométrage invalide"))

        else:
            messages.error(request, _("Le formulaire contient des erreurs."))
            print(form.errors)

    else:
        form = RemplacementBoiteForm(
            instance=remplacement_boite,
            user=request.user,
            exemplaire=exemplaire
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
            "fields": [
                form[f.name]
                for f in form
                if "serrage" in f.name
            ],
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

    if (
        role not in roles_autorises
        and not request.user.is_superuser
    ):
        messages.error(
            request,
            _("Accès refusé")
        )
        return redirect(
            "utilisateurs:dashboard"
        )

    # ==================================================
    # RÉCUPÉRATION CHECKUP
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
        (
            exemplaire.client
            and exemplaire.client.societe == tenant
        )
        or
        (
            exemplaire.client is None
            and exemplaire.societe == tenant
        )
    ):
        messages.error(
            request,
            _("Accès refusé")
        )
        return redirect(
            "utilisateurs:dashboard"
        )

    # ==================================================
    # DELETE
    # ==================================================
    if request.method == "POST":

        try:
            with transaction.atomic():

                immatriculation = exemplaire.immatriculation

                # ==================================================
                # RESTAURATION DU KILOMÉTRAGE
                # ==================================================
                kilometrage_rollback = (
                    exemplaire.kilometres_rollback or 0
                )

                exemplaire.kilometres_chassis = (
                    kilometrage_rollback
                )

                exemplaire.save(
                    update_fields=[
                        "kilometres_chassis",
                    ]
                )

                # ==================================================
                # SUPPRESSION CHECKUP
                # ==================================================
                remplacement_boite.delete()

                # ==================================================
                # SUPPRESSION MAINTENANCE ASSOCIÉE
                # ==================================================
                if maintenance:
                    maintenance.delete()

                # ==================================================
                # USER LOG
                # ==================================================
                ACTION_SUPPRESSION_REMPLACEMENT_BOITE = gettext_noop(
                    "Suppression du remplacement de la boite de vitesse"
                )

                UserLog.objects.create(
                    utilisateur=request.user,
                    action=(
                        f"{ACTION_SUPPRESSION_REMPLACEMENT_BOITE} - "
                        f"{immatriculation}"
                    )
                )

            messages.success(
                request,
                _("Remplacement de la boite supprimé avec succès.")
            )

            return redirect(
                "remplacement_boite:remplacement_boite_list",
                exemplaire_id=exemplaire.id
            )

        except Exception as e:

            messages.error(
                request,
                _("Erreur lors de la suppression : %(erreur)s")
                % {
                    "erreur": str(e)
                }
            )

            return redirect(
                "remplacement_boite:remplacement_boite_detail",
                 abs_id=remplacement_boite.id,
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
        }
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