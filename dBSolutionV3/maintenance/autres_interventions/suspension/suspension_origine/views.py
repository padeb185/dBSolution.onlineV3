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
from maintenance.autres_interventions.suspension.suspension_origine.models import SuspensionOrigine
from maintenance.autres_interventions.suspension.suspension_origine.forms import SuspensionOrigineForm
from weasyprint import HTML
from utils.securite import q_intervention_tenant







@method_decorator([login_required, never_cache], name='dispatch')
class SuspensionOrigineListView(ListView):
    model = SuspensionOrigine
    template_name = "suspension_origine/suspension_origine_list.html"
    context_object_name = "suspension_origines"
    ordering = ["-id"]

    def get_queryset(self):
        queryset = SuspensionOrigine.objects.select_related(
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
def suspension_origine_form_view(request, exemplaire_id):
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

        form = SuspensionOrigineForm(
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

                km = form.cleaned_data.get("kilometrage_suspension_origine")


                if km is None:
                    form.add_error(
                        "kilometrage_suspension_origine",
                        _("Le kilométrage est obligatoire."),
                    )

                else:
                    km = int(km)

                    if km < ancien_kilometrage:
                        form.add_error(
                            "kilometrage_suspension_origine",
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
                                type_maintenance=Maintenance.TypeMaintenance.SUSPENSION_ORIGINE,
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
                            # CONTRÔLE SUSPENSION_ORIGINE
                            # ==================================================
                            suspension_origine_obj = form.save(commit=False)


                            suspension_origine_obj.voiture_exemplaire = (
                                exemplaire
                            )

                            suspension_origine_obj.maintenance = (
                                maintenance
                            )

                            # ---------------------------------------------
                            # Kilométrage AVANT intervention
                            # ---------------------------------------------
                            suspension_origine_obj.kilometres_chassis = (
                                ancien_kilometrage
                            )

                            suspension_origine_obj.kilometres_boite = (
                                ancien_kilometrage_boite
                            )

                            suspension_origine_obj.kilometres_moteur = (
                                ancien_kilometrage_moteur
                            )

                            suspension_origine_obj.kilometres_embrayage = (
                                ancien_kilometrage_embrayage
                            )


                            # ---------------------------------------------
                            # Kilométrage suspension_origine
                            # ---------------------------------------------
                            suspension_origine_obj.kilometrage_suspension_origine = km

                            # ---------------------------------------------
                            # Variation kilométrique
                            # ---------------------------------------------
                            suspension_origine_obj.kilometrage_variation = (
                                kilometrage_variation
                            )

                            # =============================================
                            # TECHNICIEN
                            # =============================================
                            suspension_origine_obj.assign_technicien(
                                request.user
                            )

                            suspension_origine_obj.tech_last_maintained_by = (
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
                            if suspension_origine_obj.main_oeuvre_id:

                                main_oeuvre = (
                                    suspension_origine_obj.main_oeuvre
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

                                suspension_origine_obj.main_oeuvre = (
                                    main_oeuvre
                                )

                            # ==================================================
                            # SAUVEGARDE suspension_origine_obj
                            # IMPORTANT :
                            # EN DEHORS DU IF/ELSE MAIN-D'ŒUVRE
                            # ==================================================
                            suspension_origine_obj.save()

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



                        ACTION_SUSPENSION_ORIGINEBUTION = gettext_noop(
                            "Intervention suspension"
                        )

                        UserLog.objects.create(
                            utilisateur=request.user,
                            action=f"{ACTION_SUSPENSION_ORIGINEBUTION} - {exemplaire.immatriculation}"
                        )

                        messages.success(request, _("Intervention enregistrée avec succès."))


                        return redirect(
                            f"{reverse('suspension_origine:suspension_origine_list', kwargs={'exemplaire_id': exemplaire.id})}?saved=1"
                        )


            except Exception as e:
                messages.error(request, _(f"Erreur lors de l'enregistrement : {str(e)}"))

        else:
            messages.error(request, _("Le formulaire contient des erreurs."))
            print(form.errors)
    else:
        suspension_origine_nouveau = SuspensionOrigine(
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
        suspension_origine_nouveau.assign_technicien(request.user)

        form = SuspensionOrigineForm(
            instance=suspension_origine_nouveau,
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
            "title": _("Amortisseurs avant"),
            "icon": "icons/susp_amortisseur.png",
            "fields": [form[f.name] for f in form if f.name == "amortisseurs_av" or f.name.startswith("amortisseurs_av_")],
        },
        {
            "title": _("Amortisseurs arrière"),
            "icon": "icons/susp_amortisseur.png",
            "fields": [form[f.name] for f in form if f.name == "amortisseurs_ar" or f.name.startswith("amortisseurs_ar_")],
        },
        {
            "title": _("Ressorts avant"),
            "icon": "icons/susp_ressort.png",
            "fields": [form[f.name] for f in form if f.name == "ressorts_av" or f.name.startswith("ressorts_av_")],
        },
        {
            "title": _("Ressorts arrière"),
            "icon": "icons/susp_ressort.png",
            "fields": [form[f.name] for f in form if f.name == "ressorts_ar" or f.name.startswith("ressorts_ar_")],
        },
        {
            "title": _("Coupelles (têtes d'amortisseur)"),
            "icon": "icons/susp_coupelle.png",
            "fields": [form[f.name] for f in form if f.name == "coupelles" or f.name.startswith("coupelles_")],
        },
        {
            "title": _("Roulements de suspension"),
            "icon": "icons/susp_roulement.png",
            "fields": [form[f.name] for f in form if f.name == "roulements_suspension" or f.name.startswith("roulements_suspension_")],
        },
        {
            "title": _("Butées de suspension"),
            "icon": "icons/susp_butee.png",
            "fields": [form[f.name] for f in form if f.name == "butees_suspension" or f.name.startswith("butees_suspension_")],
        },
        {
            "title": _("Soufflets / kits de protection"),
            "icon": "icons/susp_soufflet.png",
            "fields": [form[f.name] for f in form if f.name == "soufflets" or f.name.startswith("soufflets_")],
        },
        {
            "title": _("Écrous de tige d'amortisseur"),
            "icon": "icons/susp_ecrou.png",
            "fields": [form[f.name] for f in form if f.name == "ecrous" or f.name.startswith("ecrous_")],
        },
        {
            "title": _("Biellettes de barre stabilisatrice"),
            "icon": "icons/susp_biellette.png",
            "fields": [form[f.name] for f in form if f.name == "biellettes_barre_stab" or f.name.startswith("biellettes_barre_stab_")],
        },
        {
            "title": _("Silent blocs de barre stabilisatrice"),
            "icon": "icons/susp_silent_bloc.png",
            "fields": [form[f.name] for f in form if f.name == "silent_blocs_barre_stab" or f.name.startswith("silent_blocs_barre_stab_")],
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

    return render(request, 'suspension_origine/suspension_origine_form.html', {
        "exemplaire": exemplaire,
        "immatriculation": exemplaire.immatriculation,
        "maintenance": maintenance,
        "form": form,
        "sections": sections,
        "now": timezone.now(),
    })






# ------------
# Vue détail suspension_origine
# -----------------------------

@never_cache
@login_required
def suspension_origine_detail_view(request, suspension_origine_id):
    suspension_origine = get_object_or_404(
        SuspensionOrigine.objects.select_related("voiture_exemplaire").filter(q_intervention_tenant(request.user)),
        id=suspension_origine_id
    )

    context = {
        "suspension_origine": suspension_origine,
        "exemplaire": suspension_origine.voiture_exemplaire,
    }
    return render(request, "suspension_origine/suspension_origine_detail.html", context)







@login_required
def modifier_suspension_origine_view(request, suspension_origine_id):
    tenant = request.user.societe

    suspension_origine = get_object_or_404(
        SuspensionOrigine.objects.select_related("voiture_exemplaire"),
        id=suspension_origine_id
    )
    exemplaire = suspension_origine.voiture_exemplaire
    # -------------------------
    # POST
    # -------------------------
    if request.method == "POST":
        form = SuspensionOrigineForm(
            request.POST,
            instance=suspension_origine,
            user=request.user,
            exemplaire=suspension_origine.voiture_exemplaire
        )

        if form.is_valid():

            try:
                with transaction.atomic():

                    # ==================================================
                    # NOUVEAU KILOMÉTRAGE SAISI
                    # ==================================================
                    km = form.cleaned_data.get(
                        "kilometrage_suspension_origine"
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
                    suspension_origine_obj = form.save(
                        commit=False
                    )

                    suspension_origine_obj.voiture_exemplaire = (
                        exemplaire
                    )

                    # ==================================================
                    # ROLLBACK LOCAL
                    # ==================================================
                    suspension_origine_obj.kilometres_chassis = (
                        rollback_chassis
                    )

                    suspension_origine_obj.kilometres_moteur = (
                        rollback_moteur
                    )

                    suspension_origine_obj.kilometres_boite = (
                        rollback_boite
                    )

                    suspension_origine_obj.kilometres_embrayage = (
                        rollback_embrayage
                    )

                    # ==================================================
                    # NOUVEAU KILOMÉTRAGE
                    # ==================================================
                    suspension_origine_obj.kilometrage_suspension_origine = km

                    # ==================================================
                    # VARIATION
                    # ==================================================
                    if km is not None:
                        suspension_origine_obj.kilometrage_variation = (
                                km - rollback_chassis
                        )
                    else:
                        suspension_origine_obj.kilometrage_variation = 0

                    # ==================================================
                    # TECHNICIEN
                    # ==================================================
                    suspension_origine_obj.assign_technicien(
                        request.user
                    )

                    suspension_origine_obj.tech_last_maintained_by = (
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
                    suspension_origine_obj.save()

                    form.save_m2m()



                    ACTION_MODIFICATION_SUSPENSION_ORIGINEBUTION = gettext_noop(
                        "Modification intervention suspension"
                    )

                    UserLog.objects.create(
                        utilisateur=request.user,
                        action=f"{ACTION_MODIFICATION_SUSPENSION_ORIGINEBUTION} - {exemplaire.immatriculation}"
                    )

                    messages.success(
                        request,
                        _("Intervention modifiée avec succès !")
                    )

                    return redirect(
                        f"{reverse('suspension_origine:suspension_origine_detail', kwargs={'suspension_origine_id': suspension_origine.id})}?saved=1"
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
        form = SuspensionOrigineForm(
            instance=suspension_origine,
            user=request.user,
            exemplaire=suspension_origine.voiture_exemplaire
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
            "title": _("Amortisseurs avant"),
            "icon": "icons/susp_amortisseur.png",
            "fields": [form[f.name] for f in form if f.name == "amortisseurs_av" or f.name.startswith("amortisseurs_av_")],
        },
        {
            "title": _("Amortisseurs arrière"),
            "icon": "icons/susp_amortisseur.png",
            "fields": [form[f.name] for f in form if f.name == "amortisseurs_ar" or f.name.startswith("amortisseurs_ar_")],
        },
        {
            "title": _("Ressorts avant"),
            "icon": "icons/susp_ressort.png",
            "fields": [form[f.name] for f in form if f.name == "ressorts_av" or f.name.startswith("ressorts_av_")],
        },
        {
            "title": _("Ressorts arrière"),
            "icon": "icons/susp_ressort.png",
            "fields": [form[f.name] for f in form if f.name == "ressorts_ar" or f.name.startswith("ressorts_ar_")],
        },
        {
            "title": _("Coupelles (têtes d'amortisseur)"),
            "icon": "icons/susp_coupelle.png",
            "fields": [form[f.name] for f in form if f.name == "coupelles" or f.name.startswith("coupelles_")],
        },
        {
            "title": _("Roulements de suspension"),
            "icon": "icons/susp_roulement.png",
            "fields": [form[f.name] for f in form if f.name == "roulements_suspension" or f.name.startswith("roulements_suspension_")],
        },
        {
            "title": _("Butées de suspension"),
            "icon": "icons/susp_butee.png",
            "fields": [form[f.name] for f in form if f.name == "butees_suspension" or f.name.startswith("butees_suspension_")],
        },
        {
            "title": _("Soufflets / kits de protection"),
            "icon": "icons/susp_soufflet.png",
            "fields": [form[f.name] for f in form if f.name == "soufflets" or f.name.startswith("soufflets_")],
        },
        {
            "title": _("Écrous de tige d'amortisseur"),
            "icon": "icons/susp_ecrou.png",
            "fields": [form[f.name] for f in form if f.name == "ecrous" or f.name.startswith("ecrous_")],
        },
        {
            "title": _("Biellettes de barre stabilisatrice"),
            "icon": "icons/susp_biellette.png",
            "fields": [form[f.name] for f in form if f.name == "biellettes_barre_stab" or f.name.startswith("biellettes_barre_stab_")],
        },
        {
            "title": _("Silent blocs de barre stabilisatrice"),
            "icon": "icons/susp_silent_bloc.png",
            "fields": [form[f.name] for f in form if f.name == "silent_blocs_barre_stab" or f.name.startswith("silent_blocs_barre_stab_")],
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
        "suspension_origine/modifier_suspension_origine.html",
        {
            "form": form,
            "suspension_origine": suspension_origine,
            "sections": sections,
            "exemplaire": exemplaire,
        }
    )




@never_cache
@login_required
def delete_suspension_origine_view(request, suspension_origine_id):

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
    suspension_origine = get_object_or_404(
        SuspensionOrigine.objects.select_related(
            "voiture_exemplaire",
            "maintenance",
        ),
        id=suspension_origine_id,
    )

    exemplaire = suspension_origine.voiture_exemplaire
    maintenance = suspension_origine.maintenance

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
                suspension_origine.delete()

                # ==================================================
                # SUPPRESSION MAINTENANCE ASSOCIÉE
                # ==================================================
                if maintenance:
                    maintenance.delete()

                # ==================================================
                # USER LOG
                # ==================================================
                ACTION_SUPPRESSION_ATERNATEUR = gettext_noop(
                    "Suppression de l'intervention suspension"
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
                f"{reverse('suspension_origine:suspension_origine_list', kwargs={'exemplaire_id': exemplaire.id})}?deleted=1"
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
        "suspension_origine/delete_suspension_origine.html",
        {
            "suspension_origine": suspension_origine,
            "exemplaire": exemplaire,
        }
    )








@login_required
def suspension_origine_detail_pdf_view(request, pk):
    suspension_origine = get_object_or_404(SuspensionOrigine, pk=pk)

    rapport = suspension_origine.generer_rapport_remplacement()

    html_string = render_to_string(
        "suspension_origine/suspension_origine_detail_pdf.html",
        {
            "suspension_origine": suspension_origine,
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
        suspension_origine.voiture_exemplaire.immatriculation
        if suspension_origine.voiture_exemplaire
        else "sans_immatriculation"
    )

    # =========================================================
    # TECHNICIEN
    # =========================================================

    technicien = (
            suspension_origine.tech_nom_technicien
            or "technicien_inconnu"
    )

    # Nettoyage pour le nom du fichier
    technicien = str(technicien).replace(" ", "_")
    immatriculation = str(immatriculation).replace(" ", "_")

    # =========================================================
    # DATE
    # =========================================================

    date_pdf = (
        suspension_origine.date.strftime("%Y-%m-%d")
        if suspension_origine.date
        else timezone.now().strftime("%Y-%m-%d")
    )

    # =========================================================
    # TITRE / NOM DU PDF
    # =========================================================

    titre_pdf = str(_("Suspension d'origine")).replace(" ", "_").replace("'", "")
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
