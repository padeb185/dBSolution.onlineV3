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
from maintenance.autres_interventions.boitier_electronique.models import BoitierElectronique
from maintenance.autres_interventions.boitier_electronique.forms import BoitierElectroniqueForm
from weasyprint import HTML
from utils.securite import atelier_requis, q_intervention_tenant







@method_decorator([login_required, never_cache], name='dispatch')
class BoitierElectroniqueListView(ListView):
    model = BoitierElectronique
    template_name = "boitier_electronique/boitier_list.html"
    context_object_name = "boitiers"
    ordering = ["-id"]

    def get_queryset(self):
        queryset = BoitierElectronique.objects.select_related(
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
            "apprenti", "apprentis",
            "magasinier",
            "chef_mecanicien",
            "direction",
        ]

        context["is_checkup_allowed"] = self.request.user.role in roles_autorises

        return context





@never_cache
@login_required
def boitier_form_view(request, exemplaire_id):
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
        "apprenti", "apprentis",
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

        form = BoitierElectroniqueForm(
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

                km = form.cleaned_data.get("kilometrage_boitier")


                if km is None:
                    form.add_error(
                        "kilometrage_boitier",
                        _("Le kilométrage est obligatoire."),
                    )

                else:
                    km = int(km)

                    if km < ancien_kilometrage:
                        form.add_error(
                            "kilometrage_boitier",
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
                                type_maintenance=Maintenance.TypeMaintenance.BOITIER_ELECTRONIQUE,
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
                            # INTERVENTION BOÎTIER ÉLECTRONIQUE
                            # ==================================================
                            boitier_obj = form.save(commit=False)


                            boitier_obj.voiture_exemplaire = (
                                exemplaire
                            )

                            boitier_obj.maintenance = (
                                maintenance
                            )

                            # ---------------------------------------------
                            # Kilométrage AVANT intervention
                            # ---------------------------------------------
                            boitier_obj.kilometres_chassis = (
                                ancien_kilometrage
                            )

                            boitier_obj.kilometres_boite = (
                                ancien_kilometrage_boite
                            )

                            boitier_obj.kilometres_moteur = (
                                ancien_kilometrage_moteur
                            )

                            boitier_obj.kilometres_embrayage = (
                                ancien_kilometrage_embrayage
                            )


                            # ---------------------------------------------
                            # Kilométrage boitier
                            # ---------------------------------------------
                            boitier_obj.kilometrage_boitier = km

                            # ---------------------------------------------
                            # Variation kilométrique
                            # ---------------------------------------------
                            boitier_obj.kilometrage_variation = (
                                kilometrage_variation
                            )

                            # =============================================
                            # TECHNICIEN
                            # =============================================
                            boitier_obj.assign_technicien(
                                request.user
                            )

                            boitier_obj.tech_last_maintained_by = (
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
                            if boitier_obj.main_oeuvre_id:

                                main_oeuvre = (
                                    boitier_obj.main_oeuvre
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

                                boitier_obj.main_oeuvre = (
                                    main_oeuvre
                                )

                            # ==================================================
                            # SAUVEGARDE boitier_obj
                            # IMPORTANT :
                            # EN DEHORS DU IF/ELSE MAIN-D'ŒUVRE
                            # ==================================================
                            boitier_obj.save()

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



                        ACTION_BOITIER = gettext_noop(
                            "Intervention boîtier électronique"
                        )

                        UserLog.objects.create(
                            utilisateur=request.user,
                            action=f"{ACTION_BOITIER} - {exemplaire.immatriculation}"
                        )

                        messages.success(request, _("Intervention enregistrée avec succès."))


                        return redirect(
                            f"{reverse('boitier_electronique:boitier_list', kwargs={'exemplaire_id': exemplaire.id})}?saved=1"
                        )


            except Exception as e:
                messages.error(request, _("Erreur lors de l'enregistrement : %(erreur)s") % {"erreur": str(e)})

        else:
            messages.error(request, _("Le formulaire contient des erreurs."))
            print(form.errors)
    else:
        boitier_nouveau = BoitierElectronique(
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
        boitier_nouveau.assign_technicien(request.user)

        form = BoitierElectroniqueForm(
            instance=boitier_nouveau,
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
            "title": _("Boîtier de servitude moteur (BSM)"),
            "icon": "icons/be_bsm.png",
            "fields": [form[f.name] for f in form if f.name == "boitier_servitude_moteur" or f.name.startswith("boitier_servitude_moteur_")],
        },
        {
            "title": _("Boîtier de servitude intelligent (BSI / BCM)"),
            "icon": "icons/be_bsi.png",
            "fields": [form[f.name] for f in form if f.name == "boitier_servitude_intelligent" or f.name.startswith("boitier_servitude_intelligent_")],
        },
        {
            "title": _("Boîtier additionnel (puissance / piggyback)"),
            "icon": "icons/be_additionnel.png",
            "fields": [form[f.name] for f in form if f.name == "boitier_additionnel" or f.name.startswith("boitier_additionnel_")],
        },
        {
            "title": _("Boîtier ABS (calculateur)"),
            "icon": "icons/be_abs.png",
            "fields": [form[f.name] for f in form if f.name == "boitier_abs" or f.name.startswith("boitier_abs_")],
        },
        {
            "title": _("Boîtier ESP (calculateur)"),
            "icon": "icons/be_esp.png",
            "fields": [form[f.name] for f in form if f.name == "boitier_esp" or f.name.startswith("boitier_esp_")],
        },
        {
            "title": _("Boîtier Carpark (aide au stationnement)"),
            "icon": "icons/be_carpark.png",
            "fields": [form[f.name] for f in form if f.name == "boitier_carpark" or f.name.startswith("boitier_carpark_")],
        },
        {
            "title": _("Boîtier d'attelage (module remorque)"),
            "icon": "icons/be_attelage.png",
            "fields": [form[f.name] for f in form if f.name == "boitier_attelage" or f.name.startswith("boitier_attelage_")],
        },
        {
            "title": _("Boîtier airbag (calculateur SRS)"),
            "icon": "icons/be_airbag.png",
            "fields": [form[f.name] for f in form if f.name == "boitier_airbag" or f.name.startswith("boitier_airbag_")],
        },
        {
            "title": _("Boîtier de boîte automatique (TCU)"),
            "icon": "icons/be_tcu.png",
            "fields": [form[f.name] for f in form if f.name == "boitier_boite_auto" or f.name.startswith("boitier_boite_auto_")],
        },
        {
            "title": _("Passerelle / gateway (réseau CAN)"),
            "icon": "icons/be_gateway.png",
            "fields": [form[f.name] for f in form if f.name == "boitier_passerelle" or f.name.startswith("boitier_passerelle_")],
        },
        {
            "title": _("Autre boîtier électronique (préciser en remarques)"),
            "icon": "icons/be_autre.png",
            "fields": [form[f.name] for f in form if f.name == "autre_boitier" or f.name.startswith("autre_boitier_")],
        },
        {
            "title": _("Faisceau et connecteurs des boîtiers"),
            "icon": "icons/be_connecteurs.png",
            "fields": [form[f.name] for f in form if f.name == "faisceau_connecteurs_boitiers" or f.name.startswith("faisceau_connecteurs_boitiers_")],
        },
        {
            "title": _("Programmation, codage et mise à jour logicielle"),
            "icon": "icons/be_programmation.png",
            "fields": [form[f.name] for f in form if f.name == "programmation_codage_boitiers" or f.name.startswith("programmation_codage_boitiers_")],
        },
        {
            "title": _("Diagnostic (lecture et effacement des défauts)"),
            "icon": "icons/be_diagnostic.png",
            "fields": [form[f.name] for f in form if f.name == "diagnostic_boitiers" or f.name.startswith("diagnostic_boitiers_")],
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

    return render(request, 'boitier_electronique/boitier_form.html', {
        "exemplaire": exemplaire,
        "immatriculation": exemplaire.immatriculation,
        "maintenance": maintenance,
        "form": form,
        "sections": sections,
        "now": timezone.now(),
    })






# ------------
# Vue détail boitier
# -----------------------------

@never_cache
@login_required
def boitier_detail_view(request, boitier_id):
    boitier = get_object_or_404(
        BoitierElectronique.objects.select_related("voiture_exemplaire").filter(q_intervention_tenant(request.user)),
        id=boitier_id
    )

    context = {
        "boitier": boitier,
        "exemplaire": boitier.voiture_exemplaire,
    }
    return render(request, "boitier_electronique/boitier_detail.html", context)







@login_required
@atelier_requis
def modifier_boitier_view(request, boitier_id):
    tenant = request.user.societe

    boitier = get_object_or_404(
        BoitierElectronique.objects.select_related("voiture_exemplaire"),
        id=boitier_id
    )
    exemplaire = boitier.voiture_exemplaire
    # -------------------------
    # POST
    # -------------------------
    if request.method == "POST":
        form = BoitierElectroniqueForm(
            request.POST,
            instance=boitier,
            user=request.user,
            exemplaire=boitier.voiture_exemplaire
        )

        if form.is_valid():

            try:
                with transaction.atomic():

                    # ==================================================
                    # NOUVEAU KILOMÉTRAGE SAISI
                    # ==================================================
                    km = form.cleaned_data.get(
                        "kilometrage_boitier"
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
                    boitier_obj = form.save(
                        commit=False
                    )

                    boitier_obj.voiture_exemplaire = (
                        exemplaire
                    )

                    # ==================================================
                    # ROLLBACK LOCAL
                    # ==================================================
                    boitier_obj.kilometres_chassis = (
                        rollback_chassis
                    )

                    boitier_obj.kilometres_moteur = (
                        rollback_moteur
                    )

                    boitier_obj.kilometres_boite = (
                        rollback_boite
                    )

                    boitier_obj.kilometres_embrayage = (
                        rollback_embrayage
                    )

                    # ==================================================
                    # NOUVEAU KILOMÉTRAGE
                    # ==================================================
                    boitier_obj.kilometrage_boitier = km

                    # ==================================================
                    # VARIATION
                    # ==================================================
                    if km is not None:
                        boitier_obj.kilometrage_variation = (
                                km - rollback_chassis
                        )
                    else:
                        boitier_obj.kilometrage_variation = 0

                    # ==================================================
                    # TECHNICIEN
                    # ==================================================
                    boitier_obj.assign_technicien(
                        request.user
                    )

                    boitier_obj.tech_last_maintained_by = (
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
                    boitier_obj.save()

                    form.save_m2m()



                    ACTION_MODIFICATION_BOITIER = gettext_noop(
                        "Modification intervention boîtier électronique"
                    )

                    UserLog.objects.create(
                        utilisateur=request.user,
                        action=f"{ACTION_MODIFICATION_BOITIER} - {exemplaire.immatriculation}"
                    )

                    messages.success(
                        request,
                        _("Intervention modifiée avec succès !")
                    )

                    return redirect(
                        f"{reverse('boitier_electronique:boitier_detail', kwargs={'boitier_id': boitier.id})}?saved=1"
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
        form = BoitierElectroniqueForm(
            instance=boitier,
            user=request.user,
            exemplaire=boitier.voiture_exemplaire
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
            "title": _("Boîtier de servitude moteur (BSM)"),
            "icon": "icons/be_bsm.png",
            "fields": [form[f.name] for f in form if f.name == "boitier_servitude_moteur" or f.name.startswith("boitier_servitude_moteur_")],
        },
        {
            "title": _("Boîtier de servitude intelligent (BSI / BCM)"),
            "icon": "icons/be_bsi.png",
            "fields": [form[f.name] for f in form if f.name == "boitier_servitude_intelligent" or f.name.startswith("boitier_servitude_intelligent_")],
        },
        {
            "title": _("Boîtier additionnel (puissance / piggyback)"),
            "icon": "icons/be_additionnel.png",
            "fields": [form[f.name] for f in form if f.name == "boitier_additionnel" or f.name.startswith("boitier_additionnel_")],
        },
        {
            "title": _("Boîtier ABS (calculateur)"),
            "icon": "icons/be_abs.png",
            "fields": [form[f.name] for f in form if f.name == "boitier_abs" or f.name.startswith("boitier_abs_")],
        },
        {
            "title": _("Boîtier ESP (calculateur)"),
            "icon": "icons/be_esp.png",
            "fields": [form[f.name] for f in form if f.name == "boitier_esp" or f.name.startswith("boitier_esp_")],
        },
        {
            "title": _("Boîtier Carpark (aide au stationnement)"),
            "icon": "icons/be_carpark.png",
            "fields": [form[f.name] for f in form if f.name == "boitier_carpark" or f.name.startswith("boitier_carpark_")],
        },
        {
            "title": _("Boîtier d'attelage (module remorque)"),
            "icon": "icons/be_attelage.png",
            "fields": [form[f.name] for f in form if f.name == "boitier_attelage" or f.name.startswith("boitier_attelage_")],
        },
        {
            "title": _("Boîtier airbag (calculateur SRS)"),
            "icon": "icons/be_airbag.png",
            "fields": [form[f.name] for f in form if f.name == "boitier_airbag" or f.name.startswith("boitier_airbag_")],
        },
        {
            "title": _("Boîtier de boîte automatique (TCU)"),
            "icon": "icons/be_tcu.png",
            "fields": [form[f.name] for f in form if f.name == "boitier_boite_auto" or f.name.startswith("boitier_boite_auto_")],
        },
        {
            "title": _("Passerelle / gateway (réseau CAN)"),
            "icon": "icons/be_gateway.png",
            "fields": [form[f.name] for f in form if f.name == "boitier_passerelle" or f.name.startswith("boitier_passerelle_")],
        },
        {
            "title": _("Autre boîtier électronique (préciser en remarques)"),
            "icon": "icons/be_autre.png",
            "fields": [form[f.name] for f in form if f.name == "autre_boitier" or f.name.startswith("autre_boitier_")],
        },
        {
            "title": _("Faisceau et connecteurs des boîtiers"),
            "icon": "icons/be_connecteurs.png",
            "fields": [form[f.name] for f in form if f.name == "faisceau_connecteurs_boitiers" or f.name.startswith("faisceau_connecteurs_boitiers_")],
        },
        {
            "title": _("Programmation, codage et mise à jour logicielle"),
            "icon": "icons/be_programmation.png",
            "fields": [form[f.name] for f in form if f.name == "programmation_codage_boitiers" or f.name.startswith("programmation_codage_boitiers_")],
        },
        {
            "title": _("Diagnostic (lecture et effacement des défauts)"),
            "icon": "icons/be_diagnostic.png",
            "fields": [form[f.name] for f in form if f.name == "diagnostic_boitiers" or f.name.startswith("diagnostic_boitiers_")],
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
        "boitier_electronique/modifier_boitier.html",
        {
            "form": form,
            "boitier": boitier,
            "sections": sections,
            "exemplaire": exemplaire,
        }
    )




@never_cache
@login_required
def delete_boitier_view(request, boitier_id):

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
    boitier = get_object_or_404(
        BoitierElectronique.objects.select_related(
            "voiture_exemplaire",
            "maintenance",
        ),
        id=boitier_id,
    )

    exemplaire = boitier.voiture_exemplaire
    maintenance = boitier.maintenance

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
                boitier.delete()

                # ==================================================
                # SUPPRESSION MAINTENANCE ASSOCIÉE
                # ==================================================
                if maintenance:
                    maintenance.delete()

                # ==================================================
                # USER LOG
                # ==================================================
                ACTION_SUPPRESSION_ATERNATEUR = gettext_noop(
                    "Suppression de l'intervention boîtier électronique"
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
                f"{reverse('boitier_electronique:boitier_list', kwargs={'exemplaire_id': exemplaire.id})}?deleted=1"
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
        "boitier_electronique/delete_boitier.html",
        {
            "boitier": boitier,
            "exemplaire": exemplaire,
        }
    )








@login_required
def boitier_detail_pdf_view(request, pk):
    boitier = get_object_or_404(BoitierElectronique, pk=pk)

    rapport = boitier.generer_rapport_remplacement()

    html_string = render_to_string(
        "boitier_electronique/boitier_detail_pdf.html",
        {
            "boitier": boitier,
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
        boitier.voiture_exemplaire.immatriculation
        if boitier.voiture_exemplaire
        else "sans_immatriculation"
    )

    # =========================================================
    # TECHNICIEN
    # =========================================================

    technicien = (
            boitier.tech_nom_technicien
            or "technicien_inconnu"
    )

    # Nettoyage pour le nom du fichier
    technicien = str(technicien).replace(" ", "_")
    immatriculation = str(immatriculation).replace(" ", "_")

    # =========================================================
    # DATE
    # =========================================================

    date_pdf = (
        boitier.date.strftime("%Y-%m-%d")
        if boitier.date
        else timezone.now().strftime("%Y-%m-%d")
    )

    # =========================================================
    # TITRE / NOM DU PDF
    # =========================================================

    titre_pdf = str(_("Boîtier électronique")).replace(" ", "_").replace("'", "")
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
