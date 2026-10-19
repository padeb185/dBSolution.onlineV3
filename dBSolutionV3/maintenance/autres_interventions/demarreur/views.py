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
from maintenance.autres_interventions.demarreur.models import Demarreur
from maintenance.autres_interventions.demarreur.forms import DemarreurForm
from weasyprint import HTML
from utils.securite import q_intervention_tenant







@method_decorator([login_required, never_cache], name='dispatch')
class DemarreurListView(ListView):
    model = Demarreur
    template_name = "demarreur/demarreur_list.html"
    context_object_name = "demarreurs"
    ordering = ["-id"]

    def get_queryset(self):
        queryset = Demarreur.objects.select_related(
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
def demarreur_form_view(request, exemplaire_id):
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

        form = DemarreurForm(
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

                km = form.cleaned_data.get("kilometrage_demarreur")


                if km is None:
                    form.add_error(
                        "kilometrage_demarreur",
                        _("Le kilométrage est obligatoire."),
                    )

                else:
                    km = int(km)

                    if km < ancien_kilometrage:
                        form.add_error(
                            "kilometrage_demarreur",
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
                                type_maintenance=Maintenance.TypeMaintenance.DEMARREUR,
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
                            # CONTRÔLE DEMARREUR
                            # ==================================================
                            demarreur_obj = form.save(commit=False)


                            demarreur_obj.voiture_exemplaire = (
                                exemplaire
                            )

                            demarreur_obj.maintenance = (
                                maintenance
                            )

                            # ---------------------------------------------
                            # Kilométrage AVANT intervention
                            # ---------------------------------------------
                            demarreur_obj.kilometres_chassis = (
                                ancien_kilometrage
                            )

                            demarreur_obj.kilometres_boite = (
                                ancien_kilometrage_boite
                            )

                            demarreur_obj.kilometres_moteur = (
                                ancien_kilometrage_moteur
                            )

                            demarreur_obj.kilometres_embrayage = (
                                ancien_kilometrage_embrayage
                            )


                            # ---------------------------------------------
                            # Kilométrage demarreur
                            # ---------------------------------------------
                            demarreur_obj.kilometrage_demarreur = km

                            # ---------------------------------------------
                            # Variation kilométrique
                            # ---------------------------------------------
                            demarreur_obj.kilometrage_variation = (
                                kilometrage_variation
                            )

                            # =============================================
                            # TECHNICIEN
                            # =============================================
                            demarreur_obj.assign_technicien(
                                request.user
                            )

                            demarreur_obj.tech_last_maintained_by = (
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
                            if demarreur_obj.main_oeuvre_id:

                                main_oeuvre = (
                                    demarreur_obj.main_oeuvre
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

                                demarreur_obj.main_oeuvre = (
                                    main_oeuvre
                                )

                            # ==================================================
                            # SAUVEGARDE demarreur_obj
                            # IMPORTANT :
                            # EN DEHORS DU IF/ELSE MAIN-D'ŒUVRE
                            # ==================================================
                            demarreur_obj.save()

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



                        ACTION_DEMARREURBUTION = gettext_noop(
                            "Intervention démarreur"
                        )

                        UserLog.objects.create(
                            utilisateur=request.user,
                            action=f"{ACTION_DEMARREURBUTION} - {exemplaire.immatriculation}"
                        )

                        messages.success(request, _("Intervention enregistrée avec succès."))


                        return redirect(
                            f"{reverse('demarreur:demarreur_list', kwargs={'exemplaire_id': exemplaire.id})}?saved=1"
                        )


            except Exception as e:
                messages.error(request, _("Erreur lors de l'enregistrement : %(erreur)s") % {"erreur": str(e)})

        else:
            messages.error(request, _("Le formulaire contient des erreurs."))
            print(form.errors)
    else:
        demarreur_nouveau = Demarreur(
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
        demarreur_nouveau.assign_technicien(request.user)

        form = DemarreurForm(
            instance=demarreur_nouveau,
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
            "title": _("Type d'intervention"),
            "icon": "icons/demarreur.png",
            "fields": [form[f.name] for f in form if f.name == "type_intervention"],
        },
        {
            "title": _("Démarreur complet (neuf ou échange standard)"),
            "icon": "icons/dem_demarreur_complet.png",
            "fields": [form[f.name] for f in form if f.name == "demarreur_complet" or f.name.startswith("demarreur_complet_")],
        },
        {
            "title": _("Solénoïde (contacteur / relais de démarreur)"),
            "icon": "icons/dem_solenoide.png",
            "fields": [form[f.name] for f in form if f.name == "solenoide" or f.name.startswith("solenoide_")],
        },
        {
            "title": _("Lanceur (pignon / bendix)"),
            "icon": "icons/dem_lanceur.png",
            "fields": [form[f.name] for f in form if f.name == "lanceur" or f.name.startswith("lanceur_")],
        },
        {
            "title": _("Roue libre du lanceur"),
            "icon": "icons/dem_roue_libre.png",
            "fields": [form[f.name] for f in form if f.name == "roue_libre" or f.name.startswith("roue_libre_")],
        },
        {
            "title": _("Fourchette d'engrènement"),
            "icon": "icons/dem_fourchette.png",
            "fields": [form[f.name] for f in form if f.name == "fourchette" or f.name.startswith("fourchette_")],
        },
        {
            "title": _("Induit (rotor)"),
            "icon": "icons/dem_induit.png",
            "fields": [form[f.name] for f in form if f.name == "induit" or f.name.startswith("induit_")],
        },
        {
            "title": _("Inducteurs / aimants (stator)"),
            "icon": "icons/dem_inducteurs.png",
            "fields": [form[f.name] for f in form if f.name == "inducteurs" or f.name.startswith("inducteurs_")],
        },
        {
            "title": _("Charbons (balais)"),
            "icon": "icons/dem_charbons.png",
            "fields": [form[f.name] for f in form if f.name == "charbons" or f.name.startswith("charbons_")],
        },
        {
            "title": _("Porte-balais"),
            "icon": "icons/dem_porte_balais.png",
            "fields": [form[f.name] for f in form if f.name == "porte_balais" or f.name.startswith("porte_balais_")],
        },
        {
            "title": _("Collecteur de l'induit (rectification)"),
            "icon": "icons/dem_collecteur.png",
            "fields": [form[f.name] for f in form if f.name == "collecteur_induit" or f.name.startswith("collecteur_induit_")],
        },
        {
            "title": _("Coussinets / bagues de palier"),
            "icon": "icons/dem_coussinets.png",
            "fields": [form[f.name] for f in form if f.name == "coussinets" or f.name.startswith("coussinets_")],
        },
        {
            "title": _("Réducteur planétaire"),
            "icon": "icons/dem_reducteur.png",
            "fields": [form[f.name] for f in form if f.name == "reducteur" or f.name.startswith("reducteur_")],
        },
        {
            "title": _("Joints et visserie"),
            "icon": "icons/dem_joints.png",
            "fields": [form[f.name] for f in form if f.name == "joints_demarreur" or f.name.startswith("joints_demarreur_")],
        },
        {
            "title": _("Câble d'alimentation (+ batterie)"),
            "icon": "icons/dem_cable.png",
            "fields": [form[f.name] for f in form if f.name == "cable_alimentation" or f.name.startswith("cable_alimentation_")],
        },
        {
            "title": _("Câble de masse"),
            "icon": "icons/dem_masse.png",
            "fields": [form[f.name] for f in form if f.name == "cable_masse_demarreur" or f.name.startswith("cable_masse_demarreur_")],
        },
        {
            "title": _("Relais de démarrage"),
            "icon": "icons/dem_relais.png",
            "fields": [form[f.name] for f in form if f.name == "relais_demarrage" or f.name.startswith("relais_demarrage_")],
        },
        {
            "title": _("Graisse (nettoyage et graissage)"),
            "icon": "icons/dem_graisse.png",
            "fields": [form[f.name] for f in form if f.name == "graisse_demarreur" or f.name.startswith("graisse_demarreur_")],
        },
        {
            "title": _("Couronne du volant moteur"),
            "icon": "icons/dem_couronne.png",
            "fields": [form[f.name] for f in form if f.name == "couronne_volant" or f.name.startswith("couronne_volant_")],
        },
        {
            "title": _("Essai au banc / test de démarrage"),
            "icon": "icons/dem_essai.png",
            "fields": [form[f.name] for f in form if f.name == "essai_banc" or f.name.startswith("essai_banc_")],
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

    return render(request, 'demarreur/demarreur_form.html', {
        "exemplaire": exemplaire,
        "immatriculation": exemplaire.immatriculation,
        "maintenance": maintenance,
        "form": form,
        "sections": sections,
        "now": timezone.now(),
    })






# ------------
# Vue détail demarreur
# -----------------------------

@never_cache
@login_required
def demarreur_detail_view(request, demarreur_id):
    demarreur = get_object_or_404(
        Demarreur.objects.select_related("voiture_exemplaire").filter(q_intervention_tenant(request.user)),
        id=demarreur_id
    )

    context = {
        "demarreur": demarreur,
        "exemplaire": demarreur.voiture_exemplaire,
    }
    return render(request, "demarreur/demarreur_detail.html", context)







@login_required
def modifier_demarreur_view(request, demarreur_id):
    tenant = request.user.societe

    demarreur = get_object_or_404(
        Demarreur.objects.select_related("voiture_exemplaire"),
        id=demarreur_id
    )
    exemplaire = demarreur.voiture_exemplaire
    # -------------------------
    # POST
    # -------------------------
    if request.method == "POST":
        form = DemarreurForm(
            request.POST,
            instance=demarreur,
            user=request.user,
            exemplaire=demarreur.voiture_exemplaire
        )

        if form.is_valid():

            try:
                with transaction.atomic():

                    # ==================================================
                    # NOUVEAU KILOMÉTRAGE SAISI
                    # ==================================================
                    km = form.cleaned_data.get(
                        "kilometrage_demarreur"
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
                    demarreur_obj = form.save(
                        commit=False
                    )

                    demarreur_obj.voiture_exemplaire = (
                        exemplaire
                    )

                    # ==================================================
                    # ROLLBACK LOCAL
                    # ==================================================
                    demarreur_obj.kilometres_chassis = (
                        rollback_chassis
                    )

                    demarreur_obj.kilometres_moteur = (
                        rollback_moteur
                    )

                    demarreur_obj.kilometres_boite = (
                        rollback_boite
                    )

                    demarreur_obj.kilometres_embrayage = (
                        rollback_embrayage
                    )

                    # ==================================================
                    # NOUVEAU KILOMÉTRAGE
                    # ==================================================
                    demarreur_obj.kilometrage_demarreur = km

                    # ==================================================
                    # VARIATION
                    # ==================================================
                    if km is not None:
                        demarreur_obj.kilometrage_variation = (
                                km - rollback_chassis
                        )
                    else:
                        demarreur_obj.kilometrage_variation = 0

                    # ==================================================
                    # TECHNICIEN
                    # ==================================================
                    demarreur_obj.assign_technicien(
                        request.user
                    )

                    demarreur_obj.tech_last_maintained_by = (
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
                    demarreur_obj.save()

                    form.save_m2m()



                    ACTION_MODIFICATION_DEMARREURBUTION = gettext_noop(
                        "Modification intervention démarreur"
                    )

                    UserLog.objects.create(
                        utilisateur=request.user,
                        action=f"{ACTION_MODIFICATION_DEMARREURBUTION} - {exemplaire.immatriculation}"
                    )

                    messages.success(
                        request,
                        _("Intervention modifiée avec succès !")
                    )

                    return redirect(
                        f"{reverse('demarreur:demarreur_detail', kwargs={'demarreur_id': demarreur.id})}?saved=1"
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
        form = DemarreurForm(
            instance=demarreur,
            user=request.user,
            exemplaire=demarreur.voiture_exemplaire
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
            "title": _("Type d'intervention"),
            "icon": "icons/demarreur.png",
            "fields": [form[f.name] for f in form if f.name == "type_intervention"],
        },
        {
            "title": _("Démarreur complet (neuf ou échange standard)"),
            "icon": "icons/dem_demarreur_complet.png",
            "fields": [form[f.name] for f in form if f.name == "demarreur_complet" or f.name.startswith("demarreur_complet_")],
        },
        {
            "title": _("Solénoïde (contacteur / relais de démarreur)"),
            "icon": "icons/dem_solenoide.png",
            "fields": [form[f.name] for f in form if f.name == "solenoide" or f.name.startswith("solenoide_")],
        },
        {
            "title": _("Lanceur (pignon / bendix)"),
            "icon": "icons/dem_lanceur.png",
            "fields": [form[f.name] for f in form if f.name == "lanceur" or f.name.startswith("lanceur_")],
        },
        {
            "title": _("Roue libre du lanceur"),
            "icon": "icons/dem_roue_libre.png",
            "fields": [form[f.name] for f in form if f.name == "roue_libre" or f.name.startswith("roue_libre_")],
        },
        {
            "title": _("Fourchette d'engrènement"),
            "icon": "icons/dem_fourchette.png",
            "fields": [form[f.name] for f in form if f.name == "fourchette" or f.name.startswith("fourchette_")],
        },
        {
            "title": _("Induit (rotor)"),
            "icon": "icons/dem_induit.png",
            "fields": [form[f.name] for f in form if f.name == "induit" or f.name.startswith("induit_")],
        },
        {
            "title": _("Inducteurs / aimants (stator)"),
            "icon": "icons/dem_inducteurs.png",
            "fields": [form[f.name] for f in form if f.name == "inducteurs" or f.name.startswith("inducteurs_")],
        },
        {
            "title": _("Charbons (balais)"),
            "icon": "icons/dem_charbons.png",
            "fields": [form[f.name] for f in form if f.name == "charbons" or f.name.startswith("charbons_")],
        },
        {
            "title": _("Porte-balais"),
            "icon": "icons/dem_porte_balais.png",
            "fields": [form[f.name] for f in form if f.name == "porte_balais" or f.name.startswith("porte_balais_")],
        },
        {
            "title": _("Collecteur de l'induit (rectification)"),
            "icon": "icons/dem_collecteur.png",
            "fields": [form[f.name] for f in form if f.name == "collecteur_induit" or f.name.startswith("collecteur_induit_")],
        },
        {
            "title": _("Coussinets / bagues de palier"),
            "icon": "icons/dem_coussinets.png",
            "fields": [form[f.name] for f in form if f.name == "coussinets" or f.name.startswith("coussinets_")],
        },
        {
            "title": _("Réducteur planétaire"),
            "icon": "icons/dem_reducteur.png",
            "fields": [form[f.name] for f in form if f.name == "reducteur" or f.name.startswith("reducteur_")],
        },
        {
            "title": _("Joints et visserie"),
            "icon": "icons/dem_joints.png",
            "fields": [form[f.name] for f in form if f.name == "joints_demarreur" or f.name.startswith("joints_demarreur_")],
        },
        {
            "title": _("Câble d'alimentation (+ batterie)"),
            "icon": "icons/dem_cable.png",
            "fields": [form[f.name] for f in form if f.name == "cable_alimentation" or f.name.startswith("cable_alimentation_")],
        },
        {
            "title": _("Câble de masse"),
            "icon": "icons/dem_masse.png",
            "fields": [form[f.name] for f in form if f.name == "cable_masse_demarreur" or f.name.startswith("cable_masse_demarreur_")],
        },
        {
            "title": _("Relais de démarrage"),
            "icon": "icons/dem_relais.png",
            "fields": [form[f.name] for f in form if f.name == "relais_demarrage" or f.name.startswith("relais_demarrage_")],
        },
        {
            "title": _("Graisse (nettoyage et graissage)"),
            "icon": "icons/dem_graisse.png",
            "fields": [form[f.name] for f in form if f.name == "graisse_demarreur" or f.name.startswith("graisse_demarreur_")],
        },
        {
            "title": _("Couronne du volant moteur"),
            "icon": "icons/dem_couronne.png",
            "fields": [form[f.name] for f in form if f.name == "couronne_volant" or f.name.startswith("couronne_volant_")],
        },
        {
            "title": _("Essai au banc / test de démarrage"),
            "icon": "icons/dem_essai.png",
            "fields": [form[f.name] for f in form if f.name == "essai_banc" or f.name.startswith("essai_banc_")],
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
        "demarreur/modifier_demarreur.html",
        {
            "form": form,
            "demarreur": demarreur,
            "sections": sections,
            "exemplaire": exemplaire,
        }
    )




@never_cache
@login_required
def delete_demarreur_view(request, demarreur_id):

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
    demarreur = get_object_or_404(
        Demarreur.objects.select_related(
            "voiture_exemplaire",
            "maintenance",
        ),
        id=demarreur_id,
    )

    exemplaire = demarreur.voiture_exemplaire
    maintenance = demarreur.maintenance

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
                demarreur.delete()

                # ==================================================
                # SUPPRESSION MAINTENANCE ASSOCIÉE
                # ==================================================
                if maintenance:
                    maintenance.delete()

                # ==================================================
                # USER LOG
                # ==================================================
                ACTION_SUPPRESSION_ATERNATEUR = gettext_noop(
                    "Suppression de l'intervention démarreur"
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
                _("Intervention supprimée avec succès.")
            )

            return redirect(
                f"{reverse('demarreur:demarreur_list', kwargs={'exemplaire_id': exemplaire.id})}?deleted=1"
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
        "demarreur/delete_demarreur.html",
        {
            "demarreur": demarreur,
            "exemplaire": exemplaire,
        }
    )








@login_required
def demarreur_detail_pdf_view(request, pk):
    demarreur = get_object_or_404(Demarreur, pk=pk)

    rapport = demarreur.generer_rapport_remplacement()

    html_string = render_to_string(
        "demarreur/demarreur_detail_pdf.html",
        {
            "demarreur": demarreur,
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
        demarreur.voiture_exemplaire.immatriculation
        if demarreur.voiture_exemplaire
        else "sans_immatriculation"
    )

    # =========================================================
    # TECHNICIEN
    # =========================================================

    technicien = (
            demarreur.tech_nom_technicien
            or "technicien_inconnu"
    )

    # Nettoyage pour le nom du fichier
    technicien = str(technicien).replace(" ", "_")
    immatriculation = str(immatriculation).replace(" ", "_")

    # =========================================================
    # DATE
    # =========================================================

    date_pdf = (
        demarreur.date.strftime("%Y-%m-%d")
        if demarreur.date
        else timezone.now().strftime("%Y-%m-%d")
    )

    # =========================================================
    # TITRE / NOM DU PDF
    # =========================================================

    titre_pdf = str(_("Démarreur")).replace(" ", "_").replace("'", "")
    nom_fichier = (
        f"{titre_pdf}_{technicien}_{immatriculation}_{date_pdf}.pdf"
    )

    response = HttpResponse(
        pdf,
        content_type="application/pdf",
    )

    response["Content-Disposition"] = (
        f'inline; filename="{nom_fichier}"'
    )

    return response
