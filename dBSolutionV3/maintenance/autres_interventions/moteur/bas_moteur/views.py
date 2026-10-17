from datetime import datetime
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.contrib import messages
from django.db import transaction, models
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import ListView
from maindoeuvre.models import MainDoeuvre
from maintenance.models import Maintenance
from utilisateurs.models import UserLog
from voiture.voiture_exemplaire.models import VoitureExemplaire
from django.db.models import Q
from django.utils.translation import gettext_lazy as _, gettext_noop
from maintenance.autres_interventions.moteur.bas_moteur.models import BasMoteur
from maintenance.autres_interventions.moteur.bas_moteur.forms import BasMoteurForm
from weasyprint import HTML
from utils.securite import q_intervention_tenant







@method_decorator([login_required, never_cache], name='dispatch')
class BasMoteurListView(ListView):
    model = BasMoteur
    template_name = "bas_moteur/bas_moteur_list.html"
    context_object_name = "bas_moteurs"
    ordering = ["-id"]

    def get_queryset(self):
        queryset = BasMoteur.objects.select_related(
            "voiture_exemplaire", "maintenance", "tech_societe"
        )

        societe = getattr(self.request.user, "societe", None)
        if societe:
            queryset = queryset.filter(
                models.Q(tech_societe=societe) | models.Q(tech_societe__isnull=True)
            )

        return queryset.order_by("-id")

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
def bas_moteur_form_view(request, exemplaire_id):
    tenant = request.user.societe
    role = request.user.role

    maintenance = None



    # 🔎 Récupération exemplaire
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

        form = BasMoteurForm(
            request.POST,
            user=request.user,
            exemplaire=exemplaire
        )

        if form.is_valid():

            try:

                # ==================================================
                # KILOMÉTRAGE
                # ==================================================
                ancien_kilometrage = (
                        exemplaire.kilometres_chassis or 0
                )

                ancien_kilometrage_boite = (
                        exemplaire.kilometres_boite or 0
                )

                ancien_kilometrage_moteur = (
                        exemplaire.kilometres_moteur or 0
                )

                ancien_kilometrage_embrayage = (
                        exemplaire.kilometres_embrayage or 0
                )

                km = form.cleaned_data.get("kilometrage_bas_moteur")


                if km is None:
                    form.add_error(
                        "kilometrage_bas_moteur",
                        _("Le kilométrage est obligatoire."),
                    )

                else:
                    km = int(km)

                    if km < ancien_kilometrage:
                        form.add_error(
                            "kilometrage_bas_moteur",
                            _(
                                "Le kilométrage du contrôle "
                                "ne peut pas être inférieur au "
                                "kilométrage actuel du véhicule."
                            ),
                        )

                    else:
                        kilometrage_variation = (
                                km - ancien_kilometrage
                        )



                        # ==================================================
                        # TRANSACTION
                        # ==================================================
                        with transaction.atomic():

                            # =============================================
                            # ROLLBACK VÉHICULE
                            # =============================================
                            exemplaire.kilometres_rollback = (
                                ancien_kilometrage
                            )

                            exemplaire.kilometres_boite_rollback = (
                                ancien_kilometrage_boite
                            )

                            exemplaire.kilometres_moteur_rollback = (
                                ancien_kilometrage_moteur
                            )

                            exemplaire.kilometres_embrayage_rollback = (
                                ancien_kilometrage_embrayage
                            )

                            # =============================================
                            # DATE INTERVENTION
                            # =============================================
                            exemplaire.date_derniere_intervention = (
                                timezone.localtime(
                                    timezone.now()
                                ).date()
                            )

                            # =============================================
                            # NOUVEAU KILOMÉTRAGE
                            # =============================================
                            exemplaire.kilometres_chassis = km

                            # Recalcule :
                            # - kilometres_moteur
                            # - kilometres_boite
                            # - variation_kilometres
                            exemplaire.update_kilometres()

                            # =============================================
                            # SAUVEGARDE VÉHICULE
                            # =============================================
                            exemplaire.save(
                                update_fields=[
                                    "kilometres_chassis",
                                    "date_derniere_intervention",

                                    # Rollback
                                    "kilometres_rollback",
                                    "kilometres_boite_rollback",
                                    "kilometres_moteur_rollback",
                                    "kilometres_embrayage_rollback",

                                    # Valeurs recalculées
                                    "kilometres_moteur",
                                    "kilometres_boite",
                                    "kilometres_embrayage",
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
                                type_maintenance=Maintenance.TypeMaintenance.BAS_MOTEUR,
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

                            # ==================================================
                            # CONTRÔLE BAS_MOTEUR
                            # ==================================================
                            bas_moteur_obj = form.save(commit=False)


                            bas_moteur_obj.voiture_exemplaire = (
                                exemplaire
                            )

                            bas_moteur_obj.maintenance = (
                                maintenance
                            )

                            # ---------------------------------------------
                            # Kilométrage AVANT intervention
                            # ---------------------------------------------
                            bas_moteur_obj.kilometres_chassis = (
                                ancien_kilometrage
                            )

                            bas_moteur_obj.kilometres_boite = (
                                ancien_kilometrage_boite
                            )

                            bas_moteur_obj.kilometres_moteur = (
                                ancien_kilometrage_moteur
                            )

                            bas_moteur_obj.kilometres_embrayage = (
                                ancien_kilometrage_embrayage
                            )


                            # ---------------------------------------------
                            # Kilométrage bas_moteur
                            # ---------------------------------------------
                            bas_moteur_obj.kilometrage_bas_moteur = km

                            # ---------------------------------------------
                            # Variation kilométrique
                            # ---------------------------------------------
                            bas_moteur_obj.kilometrage_variation = (
                                kilometrage_variation
                            )

                            # =============================================
                            # TECHNICIEN
                            # =============================================
                            bas_moteur_obj.assign_technicien(
                                request.user
                            )

                            bas_moteur_obj.tech_last_maintained_by = (
                                request.user
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
                            if bas_moteur_obj.main_oeuvre_id:

                                main_oeuvre = (
                                    bas_moteur_obj.main_oeuvre
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

                                bas_moteur_obj.main_oeuvre = (
                                    main_oeuvre
                                )

                            # ==================================================
                            # SAUVEGARDE bas_moteur_obj
                            # IMPORTANT :
                            # EN DEHORS DU IF/ELSE MAIN-D'ŒUVRE
                            # ==================================================
                            bas_moteur_obj.save()

                            form.save_m2m()

                            # ==================================================
                            # MISE À JOUR DU VÉHICULE
                            # ==================================================
                            exemplaire.kilometres_chassis = km

                            exemplaire.save(
                                update_fields=[
                                    "kilometres_chassis",
                                    "kilometres_boite",
                                    "kilometres_moteur"
                                ]
                            )



                        ACTION_BAS_MOTEURBUTION = gettext_noop(
                            "Bas moteur"
                        )

                        UserLog.objects.create(
                            utilisateur=request.user,
                            action=f"{ACTION_BAS_MOTEURBUTION} - {exemplaire.immatriculation}"
                        )

                        messages.success(request, _("Contrôle du bas moteur enregistré avec succès."))


                        return redirect(
                            f"{reverse('bas_moteur:bas_moteur_list', kwargs={'exemplaire_id': exemplaire.id})}?saved=1"
                        )


            except Exception as e:
                messages.error(request, _(f"Erreur lors de l'enregistrement : {str(e)}"))

        else:
            messages.error(request, _("Le formulaire contient des erreurs."))
            print(form.errors)
    else:
        bas_moteur_nouveau = BasMoteur(
            voiture_exemplaire=exemplaire,
            kilometres_chassis=(
                    exemplaire.kilometres_chassis or 0
            ),

            kilometres_moteur=(
                    exemplaire.kilometres_moteur or 0
            ),

            kilometres_boite=(
                    exemplaire.kilometres_boite or 0
            ),
            kilometres_embrayage=(
                    exemplaire.kilometres_embrayage or 0
            ),
        )
        bas_moteur_nouveau.assign_technicien(request.user)

        form = BasMoteurForm(
            instance=bas_moteur_nouveau,
            user=request.user,
            exemplaire=exemplaire
        )

    # --- Génération des champs par section ---
    sections = [
        {
            "title": _("Kilométrage"),
            "icon": "icons/compteur.png",
            "fields": [form[f.name] for f in form if "kilo" in f.name],
        },
        {
            "title": _("Bloc moteur"),
            "icon": "icons/bm_bloc_moteur.png",
            "fields": [form[f.name] for f in form if f.name == "bloc_moteur" or f.name.startswith("bloc_moteur_")],
        },
        {
            "title": _("Chemises"),
            "icon": "icons/bm_chemises.png",
            "fields": [form[f.name] for f in form if f.name == "chemises" or f.name.startswith("chemises_")],
        },
        {
            "title": _("Vilebrequin"),
            "icon": "icons/bm_vilebrequin.png",
            "fields": [form[f.name] for f in form if f.name == "vilebrequin" or f.name.startswith("vilebrequin_")],
        },
        {
            "title": _("Manetons"),
            "icon": "icons/bm_manetons.png",
            "fields": [form[f.name] for f in form if f.name == "manetons" or f.name.startswith("manetons_")],
        },
        {
            "title": _("Tourillons"),
            "icon": "icons/bm_tourillons.png",
            "fields": [form[f.name] for f in form if f.name == "tourillons" or f.name.startswith("tourillons_")],
        },
        {
            "title": _("Coussinets de vilebrequin"),
            "icon": "icons/bm_coussinets_vilebrequin.png",
            "fields": [form[f.name] for f in form if f.name == "coussinets_vilebrequin" or f.name.startswith("coussinets_vilebrequin_")],
        },
        {
            "title": _("Coussinets de bielle"),
            "icon": "icons/bm_coussinets_bielle.png",
            "fields": [form[f.name] for f in form if f.name == "coussinets_bielle" or f.name.startswith("coussinets_bielle_")],
        },
        {
            "title": _("Bielles"),
            "icon": "icons/bm_bielles.png",
            "fields": [form[f.name] for f in form if f.name == "bielles" or f.name.startswith("bielles_")],
        },
        {
            "title": _("Axes de bielle (axes de piston)"),
            "icon": "icons/bm_axes_bielle.png",
            "fields": [form[f.name] for f in form if f.name == "axes_bielle" or f.name.startswith("axes_bielle_")],
        },
        {
            "title": _("Pistons"),
            "icon": "icons/bm_pistons.png",
            "fields": [form[f.name] for f in form if f.name == "pistons" or f.name.startswith("pistons_")],
        },
        {
            "title": _("Pompe à huile"),
            "icon": "icons/bm_pompe_huile.png",
            "fields": [form[f.name] for f in form if f.name == "pompe_huile" or f.name.startswith("pompe_huile_")],
        },
        {
            "title": _("Crépine"),
            "icon": "icons/bm_crepine.png",
            "fields": [form[f.name] for f in form if f.name == "crepine" or f.name.startswith("crepine_")],
        },
        {
            "title": _("Carter d'huile"),
            "icon": "icons/bm_carter_huile.png",
            "fields": [form[f.name] for f in form if f.name == "carter_huile" or f.name.startswith("carter_huile_")],
        },
        {
            "title": _("Carter sec"),
            "icon": "icons/bm_carter_sec.png",
            "fields": [form[f.name] for f in form if f.name == "carter_sec" or f.name.startswith("carter_sec_")],
        },
        {
            "title": _("Gicleurs d'huile"),
            "icon": "icons/bm_gicleurs_huile.png",
            "fields": [form[f.name] for f in form if f.name == "gicleurs_huile" or f.name.startswith("gicleurs_huile_")],
        },
        {
            "title": _("Huile moteur"),
            "icon": "icons/cd_huile.png",
            "fields": [form[f.name] for f in form if f.name.startswith("huile_moteur")],
        },
        {
            "title": _("Liquide de refroidissement"),
            "icon": "icons/cd_liquide_refroidissement.png",
            "fields": [form[f.name] for f in form if f.name.startswith("refroidissement")],
        },
        {
            "title": _("Etiquette"),
            "icon": "icons/tag.png",
            "fields": [form[f.name] for f in form if "tag" in f.name],
        },
        {
            "title": _("Pays"),
            "icon": "icons/pays.png",
            "fields": [form[f.name] for f in form if "pays" in f.name],
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
            "title": _("Main-d'œuvre"),
            "icon": "icons/taux.png",
            "fields": [
                field
                for field in form
                if field.name in {
                    "taux_horaire",
                }
            ],
        },

    ]

    return render(request, 'bas_moteur/bas_moteur_form.html', {
        "exemplaire": exemplaire,
        "immatriculation": exemplaire.immatriculation,
        "maintenance": maintenance,
        "form": form,
        "sections": sections,
        "now": timezone.now(),
    })






# ------------
# Vue détail bas_moteur
# -----------------------------

@never_cache
@login_required
def bas_moteur_detail_view(request, bas_moteur_id):
    bas_moteur = get_object_or_404(
        BasMoteur.objects.select_related("voiture_exemplaire").filter(q_intervention_tenant(request.user)),
        id=bas_moteur_id
    )

    context = {
        "bas_moteur": bas_moteur,
        "exemplaire": bas_moteur.voiture_exemplaire,
    }
    return render(request, "bas_moteur/bas_moteur_detail.html", context)







@login_required
def modifier_bas_moteur_view(request, bas_moteur_id):
    tenant = request.user.societe

    bas_moteur = get_object_or_404(
        BasMoteur.objects.select_related("voiture_exemplaire"),
        id=bas_moteur_id
    )
    exemplaire = bas_moteur.voiture_exemplaire
    # -------------------------
    # POST
    # -------------------------
    if request.method == "POST":
        form = BasMoteurForm(
            request.POST,
            instance=bas_moteur,
            user=request.user,
            exemplaire=bas_moteur.voiture_exemplaire
        )

        if form.is_valid():

            try:
                with transaction.atomic():

                    # ==================================================
                    # NOUVEAU KILOMÉTRAGE SAISI
                    # ==================================================
                    km = form.cleaned_data.get(
                        "kilometrage_bas_moteur"
                    )

                    if km is not None:
                        km = int(km)

                    # ==================================================
                    # VALEURS ACTUELLES = ROLLBACK LOCAL
                    # ==================================================
                    rollback_chassis = (
                            exemplaire.kilometres_chassis or 0
                    )

                    rollback_moteur = (
                            exemplaire.kilometres_moteur or 0
                    )

                    rollback_boite = (
                            exemplaire.kilometres_boite or 0
                    )

                    rollback_embrayage = (
                            exemplaire.kilometres_embrayage or 0
                    )

                    # ==================================================
                    # VALIDATION
                    # ==================================================
                    if km is not None:

                        if km < 0:
                            raise ValidationError(
                                _(
                                    "Le kilométrage ne peut pas "
                                    "être négatif."
                                )
                            )

                        if km < rollback_chassis:
                            raise ValidationError(
                                _(
                                    "Le kilométrage ne peut pas être "
                                    "inférieur à %(km)s km."
                                ) % {
                                    "km": rollback_chassis
                                }
                            )

                    # ==================================================
                    # ÉCHAPPEMENT
                    # ==================================================
                    bas_moteur_obj = form.save(
                        commit=False
                    )

                    bas_moteur_obj.voiture_exemplaire = (
                        exemplaire
                    )

                    # ==================================================
                    # ROLLBACK LOCAL
                    # ==================================================
                    bas_moteur_obj.kilometres_chassis = (
                        rollback_chassis
                    )

                    bas_moteur_obj.kilometres_moteur = (
                        rollback_moteur
                    )

                    bas_moteur_obj.kilometres_boite = (
                        rollback_boite
                    )

                    bas_moteur_obj.kilometres_embrayage = (
                        rollback_embrayage
                    )

                    # ==================================================
                    # NOUVEAU KILOMÉTRAGE
                    # ==================================================
                    bas_moteur_obj.kilometrage_bas_moteur = km

                    # ==================================================
                    # VARIATION
                    # ==================================================
                    if km is not None:
                        bas_moteur_obj.kilometrage_variation = (
                                km - rollback_chassis
                        )
                    else:
                        bas_moteur_obj.kilometrage_variation = 0

                    # ==================================================
                    # TECHNICIEN
                    # ==================================================
                    bas_moteur_obj.assign_technicien(
                        request.user
                    )

                    bas_moteur_obj.tech_last_maintained_by = (
                        request.user
                    )

                    # ==================================================
                    # MISE À JOUR DU VÉHICULE
                    # ==================================================
                    if km is not None:
                        exemplaire.kilometres_chassis = km

                        exemplaire.date_derniere_intervention = (
                            timezone.localtime(
                                timezone.now()
                            ).date()
                        )

                        exemplaire.save()

                    # ==================================================
                    # SAUVEGARDE ÉCHAPPEMENT
                    # ==================================================
                    bas_moteur_obj.save()

                    form.save_m2m()



                    ACTION_MODIFICATION_BAS_MOTEURBUTION = gettext_noop(
                        "Modification bas moteur"
                    )

                    UserLog.objects.create(
                        utilisateur=request.user,
                        action=f"{ACTION_MODIFICATION_BAS_MOTEURBUTION} - {exemplaire.immatriculation}"
                    )

                    messages.success(
                        request,
                        _("Contrôle du bas moteur modifié avec succès !")
                    )

                    return redirect(
                        f"{reverse('bas_moteur:bas_moteur_detail', kwargs={'bas_moteur_id': bas_moteur.id})}?saved=1"
                    )

            except ValidationError as e:
                form.add_error(None, e)
                messages.error(request, _("Kilométrage invalide"))

        else:
            messages.error(request, _("Le formulaire contient des erreurs."))
            print(form.errors)

    # -------------------------
    # GET
    # -------------------------
    else:
        form = BasMoteurForm(
            instance=bas_moteur,
            user=request.user,
            exemplaire=bas_moteur.voiture_exemplaire
        )

    # -------------------------
    # Sections pour le template
    # -------------------------
    sections = [
        {
            "title": _("Kilométrage"),
            "icon": "icons/compteur.png",
            "fields": [form[f.name] for f in form if "kilo" in f.name],
        },
        {
            "title": _("Bloc moteur"),
            "icon": "icons/bm_bloc_moteur.png",
            "fields": [form[f.name] for f in form if f.name == "bloc_moteur" or f.name.startswith("bloc_moteur_")],
        },
        {
            "title": _("Chemises"),
            "icon": "icons/bm_chemises.png",
            "fields": [form[f.name] for f in form if f.name == "chemises" or f.name.startswith("chemises_")],
        },
        {
            "title": _("Vilebrequin"),
            "icon": "icons/bm_vilebrequin.png",
            "fields": [form[f.name] for f in form if f.name == "vilebrequin" or f.name.startswith("vilebrequin_")],
        },
        {
            "title": _("Manetons"),
            "icon": "icons/bm_manetons.png",
            "fields": [form[f.name] for f in form if f.name == "manetons" or f.name.startswith("manetons_")],
        },
        {
            "title": _("Tourillons"),
            "icon": "icons/bm_tourillons.png",
            "fields": [form[f.name] for f in form if f.name == "tourillons" or f.name.startswith("tourillons_")],
        },
        {
            "title": _("Coussinets de vilebrequin"),
            "icon": "icons/bm_coussinets_vilebrequin.png",
            "fields": [form[f.name] for f in form if f.name == "coussinets_vilebrequin" or f.name.startswith("coussinets_vilebrequin_")],
        },
        {
            "title": _("Coussinets de bielle"),
            "icon": "icons/bm_coussinets_bielle.png",
            "fields": [form[f.name] for f in form if f.name == "coussinets_bielle" or f.name.startswith("coussinets_bielle_")],
        },
        {
            "title": _("Bielles"),
            "icon": "icons/bm_bielles.png",
            "fields": [form[f.name] for f in form if f.name == "bielles" or f.name.startswith("bielles_")],
        },
        {
            "title": _("Axes de bielle (axes de piston)"),
            "icon": "icons/bm_axes_bielle.png",
            "fields": [form[f.name] for f in form if f.name == "axes_bielle" or f.name.startswith("axes_bielle_")],
        },
        {
            "title": _("Pistons"),
            "icon": "icons/bm_pistons.png",
            "fields": [form[f.name] for f in form if f.name == "pistons" or f.name.startswith("pistons_")],
        },
        {
            "title": _("Pompe à huile"),
            "icon": "icons/bm_pompe_huile.png",
            "fields": [form[f.name] for f in form if f.name == "pompe_huile" or f.name.startswith("pompe_huile_")],
        },
        {
            "title": _("Crépine"),
            "icon": "icons/bm_crepine.png",
            "fields": [form[f.name] for f in form if f.name == "crepine" or f.name.startswith("crepine_")],
        },
        {
            "title": _("Carter d'huile"),
            "icon": "icons/bm_carter_huile.png",
            "fields": [form[f.name] for f in form if f.name == "carter_huile" or f.name.startswith("carter_huile_")],
        },
        {
            "title": _("Carter sec"),
            "icon": "icons/bm_carter_sec.png",
            "fields": [form[f.name] for f in form if f.name == "carter_sec" or f.name.startswith("carter_sec_")],
        },
        {
            "title": _("Gicleurs d'huile"),
            "icon": "icons/bm_gicleurs_huile.png",
            "fields": [form[f.name] for f in form if f.name == "gicleurs_huile" or f.name.startswith("gicleurs_huile_")],
        },
        {
            "title": _("Huile moteur"),
            "icon": "icons/cd_huile.png",
            "fields": [form[f.name] for f in form if f.name.startswith("huile_moteur")],
        },
        {
            "title": _("Liquide de refroidissement"),
            "icon": "icons/cd_liquide_refroidissement.png",
            "fields": [form[f.name] for f in form if f.name.startswith("refroidissement")],
        },
        {
            "title": _("Etiquette"),
            "icon": "icons/tag.png",
            "fields": [form[f.name] for f in form if "tag" in f.name],
        },
        {
            "title": _("Pays"),
            "icon": "icons/pays.png",
            "fields": [form[f.name] for f in form if "pays" in f.name],
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
            "title": _("Main-d'œuvre"),
            "icon": "icons/taux.png",
            "fields": [
                field
                for field in form
                if field.name in {
                    "taux_horaire",
                }
            ],
        },

    ]

    return render(
        request,
        "bas_moteur/modifier_bas_moteur.html",
        {
            "form": form,
            "bas_moteur": bas_moteur,
            "sections": sections,
            "exemplaire": exemplaire,
        }
    )




@never_cache
@login_required
def delete_bas_moteur_view(request, bas_moteur_id):

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
    bas_moteur = get_object_or_404(
        BasMoteur.objects.select_related(
            "voiture_exemplaire",
            "maintenance",
        ),
        id=bas_moteur_id,
    )

    exemplaire = bas_moteur.voiture_exemplaire
    maintenance = bas_moteur.maintenance

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
                kilometrage_rollback_boite = (
                        exemplaire.kilometres_boite_rollback or 0
                )
                kilometrage_rollback_moteur = (
                        exemplaire.kilometres_moteur_rollback or 0
                )
                kilometrage_rollback_embrayage = (
                        exemplaire.kilometres_embrayage_rollback or 0
                )

                exemplaire.kilometres_chassis = (
                    kilometrage_rollback
                )
                exemplaire.kilometres_boite = (
                    kilometrage_rollback_boite
                )
                exemplaire.kilometres_moteur = (
                    kilometrage_rollback_moteur
                )
                exemplaire.kilometres_embrayage = (
                    kilometrage_rollback_embrayage
                )


                exemplaire.save(
                    update_fields=[
                        "kilometres_chassis",
                        "kilometres_boite",
                        "kilometres_moteur",
                        "kilometres_embrayage"
                    ]
                )



                # ==================================================
                # SUPPRESSION CHECKUP
                # ==================================================
                bas_moteur.delete()

                # ==================================================
                # SUPPRESSION MAINTENANCE ASSOCIÉE
                # ==================================================
                if maintenance:
                    maintenance.delete()

                # ==================================================
                # USER LOG
                # ==================================================
                ACTION_SUPPRESSION_ATERNATEUR = gettext_noop(
                    "Suppression du contrôle du bas moteur"
                )

                UserLog.objects.create(
                    utilisateur=request.user,
                    action=(
                        f"{ACTION_SUPPRESSION_ATERNATEUR} - "
                        f"{immatriculation}"
                    )
                )

            messages.success(
                request,
                _("Contrôle du bas moteur supprimé avec succès.")
            )

            return redirect(
                f"{reverse('bas_moteur:bas_moteur_list', kwargs={'exemplaire_id': exemplaire.id})}?deleted=1"
            )

        except Exception as e:

            messages.error(
                request,
                _("Erreur lors de la suppression : %(erreur)s")
                % {
                    "erreur": str(e)
                }
            )

    # ==================================================
    # GET → CONFIRMATION
    # ==================================================
    return render(
        request,
        "bas_moteur/delete_bas_moteur.html",
        {
            "bas_moteur": bas_moteur,
            "exemplaire": exemplaire,
        }
    )








@login_required
def bas_moteur_detail_pdf_view(request, pk):
    bas_moteur = get_object_or_404(BasMoteur, pk=pk)

    rapport = bas_moteur.generer_rapport_remplacement()

    html_string = render_to_string(
        "bas_moteur/bas_moteur_detail_pdf.html",
        {
            "bas_moteur": bas_moteur,
            "rapport": rapport,
            "date_export": datetime.now(),
            "societe": request.user.societe,
        }
    )

    pdf = HTML(
        string=html_string,
        base_url=request.build_absolute_uri()
    ).write_pdf()

    # =========================================================
    # IMMATRICULATION
    # =========================================================

    immatriculation = (
        bas_moteur.voiture_exemplaire.immatriculation
        if bas_moteur.voiture_exemplaire
        else "sans_immatriculation"
    )

    # =========================================================
    # TECHNICIEN
    # =========================================================

    technicien = (
            bas_moteur.tech_nom_technicien
            or "technicien_inconnu"
    )

    # Nettoyage pour le nom du fichier
    technicien = str(technicien).replace(" ", "_")
    immatriculation = str(immatriculation).replace(" ", "_")

    # =========================================================
    # DATE
    # =========================================================

    date_pdf = (
        bas_moteur.date.strftime("%Y-%m-%d")
        if bas_moteur.date
        else timezone.now().strftime("%Y-%m-%d")
    )

    # =========================================================
    # TITRE / NOM DU PDF
    # =========================================================

    nom_fichier = (
        f"{_('Bas moteur')}_{technicien}_{immatriculation}_{date_pdf}.pdf"
    )

    response = HttpResponse(
        pdf,
        content_type="application/pdf",
    )

    response["Content-Disposition"] = (
        f'inline; filename="{nom_fichier}"'
    )

    return response
