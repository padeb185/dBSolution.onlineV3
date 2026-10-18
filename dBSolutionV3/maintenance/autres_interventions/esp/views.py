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
from maintenance.autres_interventions.esp.models import Esp
from maintenance.autres_interventions.esp.forms import EspForm
from weasyprint import HTML
from utils.securite import q_intervention_tenant







@method_decorator([login_required, never_cache], name='dispatch')
class EspListView(ListView):
    model = Esp
    template_name = "esp/esp_list.html"
    context_object_name = "esps"
    ordering = ["-id"]

    def get_queryset(self):
        queryset = Esp.objects.select_related(
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
def esp_form_view(request, exemplaire_id):
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

        form = EspForm(
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

                km = form.cleaned_data.get("kilometrage_esp")


                if km is None:
                    form.add_error(
                        "kilometrage_esp",
                        _("Le kilométrage est obligatoire."),
                    )

                else:
                    km = int(km)

                    if km < ancien_kilometrage:
                        form.add_error(
                            "kilometrage_esp",
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
                                type_maintenance=Maintenance.TypeMaintenance.ESP,
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
                            # CONTRÔLE ESP
                            # ==================================================
                            esp_obj = form.save(commit=False)


                            esp_obj.voiture_exemplaire = (
                                exemplaire
                            )

                            esp_obj.maintenance = (
                                maintenance
                            )

                            # ---------------------------------------------
                            # Kilométrage AVANT intervention
                            # ---------------------------------------------
                            esp_obj.kilometres_chassis = (
                                ancien_kilometrage
                            )

                            esp_obj.kilometres_boite = (
                                ancien_kilometrage_boite
                            )

                            esp_obj.kilometres_moteur = (
                                ancien_kilometrage_moteur
                            )

                            esp_obj.kilometres_embrayage = (
                                ancien_kilometrage_embrayage
                            )


                            # ---------------------------------------------
                            # Kilométrage esp
                            # ---------------------------------------------
                            esp_obj.kilometrage_esp = km

                            # ---------------------------------------------
                            # Variation kilométrique
                            # ---------------------------------------------
                            esp_obj.kilometrage_variation = (
                                kilometrage_variation
                            )

                            # =============================================
                            # TECHNICIEN
                            # =============================================
                            esp_obj.assign_technicien(
                                request.user
                            )

                            esp_obj.tech_last_maintained_by = (
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
                            if esp_obj.main_oeuvre_id:

                                main_oeuvre = (
                                    esp_obj.main_oeuvre
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

                                esp_obj.main_oeuvre = (
                                    main_oeuvre
                                )

                            # ==================================================
                            # SAUVEGARDE esp_obj
                            # IMPORTANT :
                            # EN DEHORS DU IF/ELSE MAIN-D'ŒUVRE
                            # ==================================================
                            esp_obj.save()

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



                        ACTION_ESPBUTION = gettext_noop(
                            "Intervention ESP"
                        )

                        UserLog.objects.create(
                            utilisateur=request.user,
                            action=f"{ACTION_ESPBUTION} - {exemplaire.immatriculation}"
                        )

                        messages.success(request, _("Intervention enregistrée avec succès."))


                        return redirect(
                            f"{reverse('esp:esp_list', kwargs={'exemplaire_id': exemplaire.id})}?saved=1"
                        )


            except Exception as e:
                messages.error(request, _(f"Erreur lors de l'enregistrement : {str(e)}"))

        else:
            messages.error(request, _("Le formulaire contient des erreurs."))
            print(form.errors)
    else:
        esp_nouveau = Esp(
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
        esp_nouveau.assign_technicien(request.user)

        form = EspForm(
            instance=esp_nouveau,
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
            "title": _("Groupe hydraulique ESP (bloc et pompe)"),
            "icon": "icons/esp_groupe_hydraulique.png",
            "fields": [form[f.name] for f in form if f.name == "groupe_hydraulique_esp" or f.name.startswith("groupe_hydraulique_esp_")],
        },
        {
            "title": _("Calculateur ESP"),
            "icon": "icons/esp_calculateur.png",
            "fields": [form[f.name] for f in form if f.name == "calculateur_esp" or f.name.startswith("calculateur_esp_")],
        },
        {
            "title": _("Capteur d'angle de volant"),
            "icon": "icons/esp_capteur_angle_volant.png",
            "fields": [form[f.name] for f in form if f.name == "capteur_angle_volant" or f.name.startswith("capteur_angle_volant_")],
        },
        {
            "title": _("Capteur de lacet et d'accélération transversale"),
            "icon": "icons/esp_capteur_lacet.png",
            "fields": [form[f.name] for f in form if f.name == "capteur_lacet" or f.name.startswith("capteur_lacet_")],
        },
        {
            "title": _("Capteur de pression de freinage"),
            "icon": "icons/esp_capteur_pression.png",
            "fields": [form[f.name] for f in form if f.name == "capteur_pression_freinage" or f.name.startswith("capteur_pression_freinage_")],
        },
        {
            "title": _("Capteurs de vitesse de roue"),
            "icon": "icons/esp_capteur_roue.png",
            "fields": [form[f.name] for f in form if f.name == "capteurs_vitesse_roue" or f.name.startswith("capteurs_vitesse_roue_")],
        },
        {
            "title": _("Contacteur de feux stop"),
            "icon": "icons/esp_contacteur_stop.png",
            "fields": [form[f.name] for f in form if f.name == "contacteur_feux_stop" or f.name.startswith("contacteur_feux_stop_")],
        },
        {
            "title": _("Bouton ESP (désactivation)"),
            "icon": "icons/esp_bouton.png",
            "fields": [form[f.name] for f in form if f.name == "bouton_esp" or f.name.startswith("bouton_esp_")],
        },
        {
            "title": _("Faisceau et connecteurs ESP"),
            "icon": "icons/esp_faisceau.png",
            "fields": [form[f.name] for f in form if f.name == "faisceau_connecteurs_esp" or f.name.startswith("faisceau_connecteurs_esp_")],
        },
        {
            "title": _("Liquide de frein (purge du groupe ESP)"),
            "icon": "icons/esp_liquide_frein.png",
            "fields": [form[f.name] for f in form if f.name == "liquide_frein_esp" or f.name.startswith("liquide_frein_esp_")],
        },
        {
            "title": _("Calibrage des capteurs (angle de volant, lacet)"),
            "icon": "icons/esp_calibrage.png",
            "fields": [form[f.name] for f in form if f.name == "calibrage_capteurs_esp" or f.name.startswith("calibrage_capteurs_esp_")],
        },
        {
            "title": _("Diagnostic et codage du calculateur ESP"),
            "icon": "icons/esp_diagnostic.png",
            "fields": [form[f.name] for f in form if f.name == "diagnostic_codage_esp" or f.name.startswith("diagnostic_codage_esp_")],
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

    return render(request, 'esp/esp_form.html', {
        "exemplaire": exemplaire,
        "immatriculation": exemplaire.immatriculation,
        "maintenance": maintenance,
        "form": form,
        "sections": sections,
        "now": timezone.now(),
    })






# ------------
# Vue détail esp
# -----------------------------

@never_cache
@login_required
def esp_detail_view(request, esp_id):
    esp = get_object_or_404(
        Esp.objects.select_related("voiture_exemplaire").filter(q_intervention_tenant(request.user)),
        id=esp_id
    )

    context = {
        "esp": esp,
        "exemplaire": esp.voiture_exemplaire,
    }
    return render(request, "esp/esp_detail.html", context)







@login_required
def modifier_esp_view(request, esp_id):
    tenant = request.user.societe

    esp = get_object_or_404(
        Esp.objects.select_related("voiture_exemplaire"),
        id=esp_id
    )
    exemplaire = esp.voiture_exemplaire
    # -------------------------
    # POST
    # -------------------------
    if request.method == "POST":
        form = EspForm(
            request.POST,
            instance=esp,
            user=request.user,
            exemplaire=esp.voiture_exemplaire
        )

        if form.is_valid():

            try:
                with transaction.atomic():

                    # ==================================================
                    # NOUVEAU KILOMÉTRAGE SAISI
                    # ==================================================
                    km = form.cleaned_data.get(
                        "kilometrage_esp"
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
                    esp_obj = form.save(
                        commit=False
                    )

                    esp_obj.voiture_exemplaire = (
                        exemplaire
                    )

                    # ==================================================
                    # ROLLBACK LOCAL
                    # ==================================================
                    esp_obj.kilometres_chassis = (
                        rollback_chassis
                    )

                    esp_obj.kilometres_moteur = (
                        rollback_moteur
                    )

                    esp_obj.kilometres_boite = (
                        rollback_boite
                    )

                    esp_obj.kilometres_embrayage = (
                        rollback_embrayage
                    )

                    # ==================================================
                    # NOUVEAU KILOMÉTRAGE
                    # ==================================================
                    esp_obj.kilometrage_esp = km

                    # ==================================================
                    # VARIATION
                    # ==================================================
                    if km is not None:
                        esp_obj.kilometrage_variation = (
                                km - rollback_chassis
                        )
                    else:
                        esp_obj.kilometrage_variation = 0

                    # ==================================================
                    # TECHNICIEN
                    # ==================================================
                    esp_obj.assign_technicien(
                        request.user
                    )

                    esp_obj.tech_last_maintained_by = (
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
                    esp_obj.save()

                    form.save_m2m()



                    ACTION_MODIFICATION_ESPBUTION = gettext_noop(
                        "Modification intervention ESP"
                    )

                    UserLog.objects.create(
                        utilisateur=request.user,
                        action=f"{ACTION_MODIFICATION_ESPBUTION} - {exemplaire.immatriculation}"
                    )

                    messages.success(
                        request,
                        _("Intervention modifiée avec succès !")
                    )

                    return redirect(
                        f"{reverse('esp:esp_detail', kwargs={'esp_id': esp.id})}?saved=1"
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
        form = EspForm(
            instance=esp,
            user=request.user,
            exemplaire=esp.voiture_exemplaire
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
            "title": _("Groupe hydraulique ESP (bloc et pompe)"),
            "icon": "icons/esp_groupe_hydraulique.png",
            "fields": [form[f.name] for f in form if f.name == "groupe_hydraulique_esp" or f.name.startswith("groupe_hydraulique_esp_")],
        },
        {
            "title": _("Calculateur ESP"),
            "icon": "icons/esp_calculateur.png",
            "fields": [form[f.name] for f in form if f.name == "calculateur_esp" or f.name.startswith("calculateur_esp_")],
        },
        {
            "title": _("Capteur d'angle de volant"),
            "icon": "icons/esp_capteur_angle_volant.png",
            "fields": [form[f.name] for f in form if f.name == "capteur_angle_volant" or f.name.startswith("capteur_angle_volant_")],
        },
        {
            "title": _("Capteur de lacet et d'accélération transversale"),
            "icon": "icons/esp_capteur_lacet.png",
            "fields": [form[f.name] for f in form if f.name == "capteur_lacet" or f.name.startswith("capteur_lacet_")],
        },
        {
            "title": _("Capteur de pression de freinage"),
            "icon": "icons/esp_capteur_pression.png",
            "fields": [form[f.name] for f in form if f.name == "capteur_pression_freinage" or f.name.startswith("capteur_pression_freinage_")],
        },
        {
            "title": _("Capteurs de vitesse de roue"),
            "icon": "icons/esp_capteur_roue.png",
            "fields": [form[f.name] for f in form if f.name == "capteurs_vitesse_roue" or f.name.startswith("capteurs_vitesse_roue_")],
        },
        {
            "title": _("Contacteur de feux stop"),
            "icon": "icons/esp_contacteur_stop.png",
            "fields": [form[f.name] for f in form if f.name == "contacteur_feux_stop" or f.name.startswith("contacteur_feux_stop_")],
        },
        {
            "title": _("Bouton ESP (désactivation)"),
            "icon": "icons/esp_bouton.png",
            "fields": [form[f.name] for f in form if f.name == "bouton_esp" or f.name.startswith("bouton_esp_")],
        },
        {
            "title": _("Faisceau et connecteurs ESP"),
            "icon": "icons/esp_faisceau.png",
            "fields": [form[f.name] for f in form if f.name == "faisceau_connecteurs_esp" or f.name.startswith("faisceau_connecteurs_esp_")],
        },
        {
            "title": _("Liquide de frein (purge du groupe ESP)"),
            "icon": "icons/esp_liquide_frein.png",
            "fields": [form[f.name] for f in form if f.name == "liquide_frein_esp" or f.name.startswith("liquide_frein_esp_")],
        },
        {
            "title": _("Calibrage des capteurs (angle de volant, lacet)"),
            "icon": "icons/esp_calibrage.png",
            "fields": [form[f.name] for f in form if f.name == "calibrage_capteurs_esp" or f.name.startswith("calibrage_capteurs_esp_")],
        },
        {
            "title": _("Diagnostic et codage du calculateur ESP"),
            "icon": "icons/esp_diagnostic.png",
            "fields": [form[f.name] for f in form if f.name == "diagnostic_codage_esp" or f.name.startswith("diagnostic_codage_esp_")],
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
        "esp/modifier_esp.html",
        {
            "form": form,
            "esp": esp,
            "sections": sections,
            "exemplaire": exemplaire,
        }
    )




@never_cache
@login_required
def delete_esp_view(request, esp_id):

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
    esp = get_object_or_404(
        Esp.objects.select_related(
            "voiture_exemplaire",
            "maintenance",
        ),
        id=esp_id,
    )

    exemplaire = esp.voiture_exemplaire
    maintenance = esp.maintenance

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
                esp.delete()

                # ==================================================
                # SUPPRESSION MAINTENANCE ASSOCIÉE
                # ==================================================
                if maintenance:
                    maintenance.delete()

                # ==================================================
                # USER LOG
                # ==================================================
                ACTION_SUPPRESSION_ATERNATEUR = gettext_noop(
                    "Suppression de l'intervention ESP"
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
                f"{reverse('esp:esp_list', kwargs={'exemplaire_id': exemplaire.id})}?deleted=1"
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
        "esp/delete_esp.html",
        {
            "esp": esp,
            "exemplaire": exemplaire,
        }
    )








@login_required
def esp_detail_pdf_view(request, pk):
    esp = get_object_or_404(Esp, pk=pk)

    rapport = esp.generer_rapport_remplacement()

    html_string = render_to_string(
        "esp/esp_detail_pdf.html",
        {
            "esp": esp,
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
        esp.voiture_exemplaire.immatriculation
        if esp.voiture_exemplaire
        else "sans_immatriculation"
    )

    # =========================================================
    # TECHNICIEN
    # =========================================================

    technicien = (
            esp.tech_nom_technicien
            or "technicien_inconnu"
    )

    # Nettoyage pour le nom du fichier
    technicien = str(technicien).replace(" ", "_")
    immatriculation = str(immatriculation).replace(" ", "_")

    # =========================================================
    # DATE
    # =========================================================

    date_pdf = (
        esp.date.strftime("%Y-%m-%d")
        if esp.date
        else timezone.now().strftime("%Y-%m-%d")
    )

    # =========================================================
    # TITRE / NOM DU PDF
    # =========================================================

    titre_pdf = str(_("ESP (contrôle de stabilité)")).replace(" ", "_").replace("'", "")
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
