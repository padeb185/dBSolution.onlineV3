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
from maintenance.autres_interventions.ventilation.models import Ventilation
from maintenance.autres_interventions.ventilation.forms import VentilationForm
from weasyprint import HTML
from utils.securite import atelier_requis, q_intervention_tenant







@method_decorator([login_required, never_cache], name='dispatch')
class VentilationListView(ListView):
    model = Ventilation
    template_name = "ventilation/ventilation_list.html"
    context_object_name = "ventilations"
    ordering = ["-id"]

    def get_queryset(self):
        queryset = Ventilation.objects.select_related(
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
def ventilation_form_view(request, exemplaire_id):
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

        form = VentilationForm(
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

                km = form.cleaned_data.get("kilometrage_ventilation")


                if km is None:
                    form.add_error(
                        "kilometrage_ventilation",
                        _("Le kilométrage est obligatoire."),
                    )

                else:
                    km = int(km)

                    if km < ancien_kilometrage:
                        form.add_error(
                            "kilometrage_ventilation",
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
                                type_maintenance=Maintenance.TypeMaintenance.VENTILATION,
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
                            # CONTRÔLE VENTILATION
                            # ==================================================
                            ventilation_obj = form.save(commit=False)


                            ventilation_obj.voiture_exemplaire = (
                                exemplaire
                            )

                            ventilation_obj.maintenance = (
                                maintenance
                            )

                            # ---------------------------------------------
                            # Kilométrage AVANT intervention
                            # ---------------------------------------------
                            ventilation_obj.kilometres_chassis = (
                                ancien_kilometrage
                            )

                            ventilation_obj.kilometres_boite = (
                                ancien_kilometrage_boite
                            )

                            ventilation_obj.kilometres_moteur = (
                                ancien_kilometrage_moteur
                            )

                            ventilation_obj.kilometres_embrayage = (
                                ancien_kilometrage_embrayage
                            )


                            # ---------------------------------------------
                            # Kilométrage ventilation
                            # ---------------------------------------------
                            ventilation_obj.kilometrage_ventilation = km

                            # ---------------------------------------------
                            # Variation kilométrique
                            # ---------------------------------------------
                            ventilation_obj.kilometrage_variation = (
                                kilometrage_variation
                            )

                            # =============================================
                            # TECHNICIEN
                            # =============================================
                            ventilation_obj.assign_technicien(
                                request.user
                            )

                            ventilation_obj.tech_last_maintained_by = (
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
                            if ventilation_obj.main_oeuvre_id:

                                main_oeuvre = (
                                    ventilation_obj.main_oeuvre
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

                                ventilation_obj.main_oeuvre = (
                                    main_oeuvre
                                )

                            # ==================================================
                            # SAUVEGARDE ventilation_obj
                            # IMPORTANT :
                            # EN DEHORS DU IF/ELSE MAIN-D'ŒUVRE
                            # ==================================================
                            ventilation_obj.save()

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



                        ACTION_VENTILATION = gettext_noop(
                            "Intervention ventilation"
                        )

                        UserLog.objects.create(
                            utilisateur=request.user,
                            action=f"{ACTION_VENTILATION} - {exemplaire.immatriculation}"
                        )

                        messages.success(request, _("Intervention enregistrée avec succès."))


                        return redirect(
                            f"{reverse('ventilation:ventilation_list', kwargs={'exemplaire_id': exemplaire.id})}?saved=1"
                        )


            except Exception as e:
                messages.error(request, _("Erreur lors de l'enregistrement : %(erreur)s") % {"erreur": str(e)})

        else:
            messages.error(request, _("Le formulaire contient des erreurs."))
            print(form.errors)
    else:
        ventilation_nouveau = Ventilation(
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
        ventilation_nouveau.assign_technicien(request.user)

        form = VentilationForm(
            instance=ventilation_nouveau,
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
            "title": _("Soufflerie (pulseur d'air habitacle)"),
            "icon": "icons/vent_soufflerie.png",
            "fields": [form[f.name] for f in form if f.name == "soufflerie" or f.name.startswith("soufflerie_")],
        },
        {
            "title": _("Moteur de ventilation"),
            "icon": "icons/vent_moteur.png",
            "fields": [form[f.name] for f in form if f.name == "moteur_ventilation" or f.name.startswith("moteur_ventilation_")],
        },
        {
            "title": _("Résistance de vitesse du moteur de ventilation"),
            "icon": "icons/vent_resistance_vitesse.png",
            "fields": [form[f.name] for f in form if f.name == "resistance_vitesse" or f.name.startswith("resistance_vitesse_")],
        },
        {
            "title": _("Module de commande électronique du pulseur"),
            "icon": "icons/vent_module_pulseur.png",
            "fields": [form[f.name] for f in form if f.name == "module_commande_pulseur" or f.name.startswith("module_commande_pulseur_")],
        },
        {
            "title": _("Filtre d'habitacle (pollen / charbon actif)"),
            "icon": "icons/vent_filtre_habitacle.png",
            "fields": [form[f.name] for f in form if f.name == "filtre_habitacle" or f.name.startswith("filtre_habitacle_")],
        },
        {
            "title": _("Résistance de chauffage additionnel (PTC)"),
            "icon": "icons/vent_resistance_chauffage.png",
            "fields": [form[f.name] for f in form if f.name == "resistance_chauffage" or f.name.startswith("resistance_chauffage_")],
        },
        {
            "title": _("Commande / tableau de ventilation-chauffage"),
            "icon": "icons/vent_commande.png",
            "fields": [form[f.name] for f in form if f.name == "commande_ventilation" or f.name.startswith("commande_ventilation_")],
        },
        {
            "title": _("Volets de répartition et de mixage d'air"),
            "icon": "icons/vent_volets.png",
            "fields": [form[f.name] for f in form if f.name == "volets_repartition" or f.name.startswith("volets_repartition_")],
        },
        {
            "title": _("Moteurs (actionneurs) de volets"),
            "icon": "icons/vent_moteurs_volets.png",
            "fields": [form[f.name] for f in form if f.name == "moteurs_volets" or f.name.startswith("moteurs_volets_")],
        },
        {
            "title": _("Volet de recyclage d'air"),
            "icon": "icons/vent_recyclage.png",
            "fields": [form[f.name] for f in form if f.name == "volet_recyclage" or f.name.startswith("volet_recyclage_")],
        },
        {
            "title": _("Sonde de température habitacle"),
            "icon": "icons/vent_sonde_temperature.png",
            "fields": [form[f.name] for f in form if f.name == "sonde_temperature_habitacle" or f.name.startswith("sonde_temperature_habitacle_")],
        },
        {
            "title": _("Aérateurs et grilles de ventilation"),
            "icon": "icons/vent_aerateurs.png",
            "fields": [form[f.name] for f in form if f.name == "aerateurs" or f.name.startswith("aerateurs_")],
        },
        {
            "title": _("Conduits et gaines d'air"),
            "icon": "icons/vent_conduits.png",
            "fields": [form[f.name] for f in form if f.name == "conduits_ventilation" or f.name.startswith("conduits_ventilation_")],
        },
        {
            "title": _("Faisceau et connecteurs"),
            "icon": "icons/vent_faisceau.png",
            "fields": [form[f.name] for f in form if f.name == "faisceau_ventilation" or f.name.startswith("faisceau_ventilation_")],
        },
        {
            "title": _("Désinfection / traitement antibactérien du circuit"),
            "icon": "icons/vent_desinfection.png",
            "fields": [form[f.name] for f in form if f.name == "desinfection_ventilation" or f.name.startswith("desinfection_ventilation_")],
        },
        {
            "title": _("Diagnostic et codage"),
            "icon": "icons/vent_diagnostic.png",
            "fields": [form[f.name] for f in form if f.name == "diagnostic_ventilation" or f.name.startswith("diagnostic_ventilation_")],
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

    return render(request, 'ventilation/ventilation_form.html', {
        "exemplaire": exemplaire,
        "immatriculation": exemplaire.immatriculation,
        "maintenance": maintenance,
        "form": form,
        "sections": sections,
        "now": timezone.now(),
    })






# ------------
# Vue détail ventilation
# -----------------------------

@never_cache
@login_required
def ventilation_detail_view(request, ventilation_id):
    ventilation = get_object_or_404(
        Ventilation.objects.select_related("voiture_exemplaire").filter(q_intervention_tenant(request.user)),
        id=ventilation_id
    )

    context = {
        "ventilation": ventilation,
        "exemplaire": ventilation.voiture_exemplaire,
    }
    return render(request, "ventilation/ventilation_detail.html", context)







@login_required
@atelier_requis
def modifier_ventilation_view(request, ventilation_id):
    tenant = request.user.societe

    ventilation = get_object_or_404(
        Ventilation.objects.select_related("voiture_exemplaire"),
        id=ventilation_id
    )
    exemplaire = ventilation.voiture_exemplaire
    # -------------------------
    # POST
    # -------------------------
    if request.method == "POST":
        form = VentilationForm(
            request.POST,
            instance=ventilation,
            user=request.user,
            exemplaire=ventilation.voiture_exemplaire
        )

        if form.is_valid():

            try:
                with transaction.atomic():

                    # ==================================================
                    # NOUVEAU KILOMÉTRAGE SAISI
                    # ==================================================
                    km = form.cleaned_data.get(
                        "kilometrage_ventilation"
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
                    ventilation_obj = form.save(
                        commit=False
                    )

                    ventilation_obj.voiture_exemplaire = (
                        exemplaire
                    )

                    # ==================================================
                    # ROLLBACK LOCAL
                    # ==================================================
                    ventilation_obj.kilometres_chassis = (
                        rollback_chassis
                    )

                    ventilation_obj.kilometres_moteur = (
                        rollback_moteur
                    )

                    ventilation_obj.kilometres_boite = (
                        rollback_boite
                    )

                    ventilation_obj.kilometres_embrayage = (
                        rollback_embrayage
                    )

                    # ==================================================
                    # NOUVEAU KILOMÉTRAGE
                    # ==================================================
                    ventilation_obj.kilometrage_ventilation = km

                    # ==================================================
                    # VARIATION
                    # ==================================================
                    if km is not None:
                        ventilation_obj.kilometrage_variation = (
                                km - rollback_chassis
                        )
                    else:
                        ventilation_obj.kilometrage_variation = 0

                    # ==================================================
                    # TECHNICIEN
                    # ==================================================
                    ventilation_obj.assign_technicien(
                        request.user
                    )

                    ventilation_obj.tech_last_maintained_by = (
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
                    ventilation_obj.save()

                    form.save_m2m()



                    ACTION_MODIFICATION_VENTILATION = gettext_noop(
                        "Modification intervention ventilation"
                    )

                    UserLog.objects.create(
                        utilisateur=request.user,
                        action=f"{ACTION_MODIFICATION_VENTILATION} - {exemplaire.immatriculation}"
                    )

                    messages.success(
                        request,
                        _("Intervention modifiée avec succès !")
                    )

                    return redirect(
                        f"{reverse('ventilation:ventilation_detail', kwargs={'ventilation_id': ventilation.id})}?saved=1"
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
        form = VentilationForm(
            instance=ventilation,
            user=request.user,
            exemplaire=ventilation.voiture_exemplaire
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
            "title": _("Soufflerie (pulseur d'air habitacle)"),
            "icon": "icons/vent_soufflerie.png",
            "fields": [form[f.name] for f in form if f.name == "soufflerie" or f.name.startswith("soufflerie_")],
        },
        {
            "title": _("Moteur de ventilation"),
            "icon": "icons/vent_moteur.png",
            "fields": [form[f.name] for f in form if f.name == "moteur_ventilation" or f.name.startswith("moteur_ventilation_")],
        },
        {
            "title": _("Résistance de vitesse du moteur de ventilation"),
            "icon": "icons/vent_resistance_vitesse.png",
            "fields": [form[f.name] for f in form if f.name == "resistance_vitesse" or f.name.startswith("resistance_vitesse_")],
        },
        {
            "title": _("Module de commande électronique du pulseur"),
            "icon": "icons/vent_module_pulseur.png",
            "fields": [form[f.name] for f in form if f.name == "module_commande_pulseur" or f.name.startswith("module_commande_pulseur_")],
        },
        {
            "title": _("Filtre d'habitacle (pollen / charbon actif)"),
            "icon": "icons/vent_filtre_habitacle.png",
            "fields": [form[f.name] for f in form if f.name == "filtre_habitacle" or f.name.startswith("filtre_habitacle_")],
        },
        {
            "title": _("Résistance de chauffage additionnel (PTC)"),
            "icon": "icons/vent_resistance_chauffage.png",
            "fields": [form[f.name] for f in form if f.name == "resistance_chauffage" or f.name.startswith("resistance_chauffage_")],
        },
        {
            "title": _("Commande / tableau de ventilation-chauffage"),
            "icon": "icons/vent_commande.png",
            "fields": [form[f.name] for f in form if f.name == "commande_ventilation" or f.name.startswith("commande_ventilation_")],
        },
        {
            "title": _("Volets de répartition et de mixage d'air"),
            "icon": "icons/vent_volets.png",
            "fields": [form[f.name] for f in form if f.name == "volets_repartition" or f.name.startswith("volets_repartition_")],
        },
        {
            "title": _("Moteurs (actionneurs) de volets"),
            "icon": "icons/vent_moteurs_volets.png",
            "fields": [form[f.name] for f in form if f.name == "moteurs_volets" or f.name.startswith("moteurs_volets_")],
        },
        {
            "title": _("Volet de recyclage d'air"),
            "icon": "icons/vent_recyclage.png",
            "fields": [form[f.name] for f in form if f.name == "volet_recyclage" or f.name.startswith("volet_recyclage_")],
        },
        {
            "title": _("Sonde de température habitacle"),
            "icon": "icons/vent_sonde_temperature.png",
            "fields": [form[f.name] for f in form if f.name == "sonde_temperature_habitacle" or f.name.startswith("sonde_temperature_habitacle_")],
        },
        {
            "title": _("Aérateurs et grilles de ventilation"),
            "icon": "icons/vent_aerateurs.png",
            "fields": [form[f.name] for f in form if f.name == "aerateurs" or f.name.startswith("aerateurs_")],
        },
        {
            "title": _("Conduits et gaines d'air"),
            "icon": "icons/vent_conduits.png",
            "fields": [form[f.name] for f in form if f.name == "conduits_ventilation" or f.name.startswith("conduits_ventilation_")],
        },
        {
            "title": _("Faisceau et connecteurs"),
            "icon": "icons/vent_faisceau.png",
            "fields": [form[f.name] for f in form if f.name == "faisceau_ventilation" or f.name.startswith("faisceau_ventilation_")],
        },
        {
            "title": _("Désinfection / traitement antibactérien du circuit"),
            "icon": "icons/vent_desinfection.png",
            "fields": [form[f.name] for f in form if f.name == "desinfection_ventilation" or f.name.startswith("desinfection_ventilation_")],
        },
        {
            "title": _("Diagnostic et codage"),
            "icon": "icons/vent_diagnostic.png",
            "fields": [form[f.name] for f in form if f.name == "diagnostic_ventilation" or f.name.startswith("diagnostic_ventilation_")],
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
        "ventilation/modifier_ventilation.html",
        {
            "form": form,
            "ventilation": ventilation,
            "sections": sections,
            "exemplaire": exemplaire,
        }
    )




@never_cache
@login_required
def delete_ventilation_view(request, ventilation_id):

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
    ventilation = get_object_or_404(
        Ventilation.objects.select_related(
            "voiture_exemplaire",
            "maintenance",
        ),
        id=ventilation_id,
    )

    exemplaire = ventilation.voiture_exemplaire
    maintenance = ventilation.maintenance

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
                ventilation.delete()

                # ==================================================
                # SUPPRESSION MAINTENANCE ASSOCIÉE
                # ==================================================
                if maintenance:
                    maintenance.delete()

                # ==================================================
                # USER LOG
                # ==================================================
                ACTION_SUPPRESSION_ATERNATEUR = gettext_noop(
                    "Suppression de l'intervention ventilation"
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
                f"{reverse('ventilation:ventilation_list', kwargs={'exemplaire_id': exemplaire.id})}?deleted=1"
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
        "ventilation/delete_ventilation.html",
        {
            "ventilation": ventilation,
            "exemplaire": exemplaire,
        }
    )








@login_required
def ventilation_detail_pdf_view(request, pk):
    ventilation = get_object_or_404(Ventilation, pk=pk)

    rapport = ventilation.generer_rapport_remplacement()

    html_string = render_to_string(
        "ventilation/ventilation_detail_pdf.html",
        {
            "ventilation": ventilation,
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
        ventilation.voiture_exemplaire.immatriculation
        if ventilation.voiture_exemplaire
        else "sans_immatriculation"
    )

    # =========================================================
    # TECHNICIEN
    # =========================================================

    technicien = (
            ventilation.tech_nom_technicien
            or "technicien_inconnu"
    )

    # Nettoyage pour le nom du fichier
    technicien = str(technicien).replace(" ", "_")
    immatriculation = str(immatriculation).replace(" ", "_")

    # =========================================================
    # DATE
    # =========================================================

    date_pdf = (
        ventilation.date.strftime("%Y-%m-%d")
        if ventilation.date
        else timezone.now().strftime("%Y-%m-%d")
    )

    # =========================================================
    # TITRE / NOM DU PDF
    # =========================================================

    titre_pdf = str(_("Ventilation")).replace(" ", "_").replace("'", "")
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
