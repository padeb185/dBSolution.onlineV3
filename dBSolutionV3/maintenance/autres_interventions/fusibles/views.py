import json
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
from maintenance.autres_interventions.fusibles.models import AMPERAGES_FUSIBLES, LIGNE_PAR_TYPE, Fusibles, synchroniser_quantites
from maintenance.autres_interventions.fusibles.forms import FusiblesForm, FusibleDetailFormSet
from weasyprint import HTML
from utils.securite import q_intervention_tenant







@method_decorator([login_required, never_cache], name='dispatch')
class FusiblesListView(ListView):
    model = Fusibles
    template_name = "fusibles/fusibles_list.html"
    context_object_name = "fusibless"
    ordering = ["-id"]

    def get_queryset(self):
        queryset = Fusibles.objects.select_related(
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
def fusibles_form_view(request, exemplaire_id):
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

        form = FusiblesForm(
            request.POST,
            user=request.user,
            exemplaire=exemplaire
        )
        detail_fs = FusibleDetailFormSet(request.POST, instance=Fusibles(), prefix="detail")

        if form.is_valid() and detail_fs.is_valid():

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

                km = form.cleaned_data.get("kilometrage_fusibles")


                if km is None:
                    form.add_error(
                        "kilometrage_fusibles",
                        _("Le kilométrage est obligatoire."),
                    )

                else:
                    km = int(km)

                    if km < ancien_kilometrage:
                        form.add_error(
                            "kilometrage_fusibles",
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
                                type_maintenance=Maintenance.TypeMaintenance.FUSIBLES,
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
                            # CONTRÔLE FUSIBLES
                            # ==================================================
                            fusibles_obj = form.save(commit=False)


                            fusibles_obj.voiture_exemplaire = (
                                exemplaire
                            )

                            fusibles_obj.maintenance = (
                                maintenance
                            )

                            # ---------------------------------------------
                            # Kilométrage AVANT intervention
                            # ---------------------------------------------
                            fusibles_obj.kilometres_chassis = (
                                ancien_kilometrage
                            )

                            fusibles_obj.kilometres_boite = (
                                ancien_kilometrage_boite
                            )

                            fusibles_obj.kilometres_moteur = (
                                ancien_kilometrage_moteur
                            )

                            fusibles_obj.kilometres_embrayage = (
                                ancien_kilometrage_embrayage
                            )


                            # ---------------------------------------------
                            # Kilométrage fusibles
                            # ---------------------------------------------
                            fusibles_obj.kilometrage_fusibles = km

                            # ---------------------------------------------
                            # Variation kilométrique
                            # ---------------------------------------------
                            fusibles_obj.kilometrage_variation = (
                                kilometrage_variation
                            )

                            # =============================================
                            # TECHNICIEN
                            # =============================================
                            fusibles_obj.assign_technicien(
                                request.user
                            )

                            fusibles_obj.tech_last_maintained_by = (
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
                            if fusibles_obj.main_oeuvre_id:

                                main_oeuvre = (
                                    fusibles_obj.main_oeuvre
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

                                fusibles_obj.main_oeuvre = (
                                    main_oeuvre
                                )

                            # ==================================================
                            # SAUVEGARDE fusibles_obj
                            # IMPORTANT :
                            # EN DEHORS DU IF/ELSE MAIN-D'ŒUVRE
                            # ==================================================
                            fusibles_obj.save()

                            form.save_m2m()

                            # Détail des fusibles (boîte, repère, ampérage, organe)
                            detail_fs.instance = fusibles_obj
                            detail_fs.save()
                            # quantités facturées = fusibles remplacés par type
                            synchroniser_quantites(fusibles_obj)

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



                        ACTION_FUSIBLESBUTION = gettext_noop(
                            "Intervention boîtes à fusibles"
                        )

                        UserLog.objects.create(
                            utilisateur=request.user,
                            action=f"{ACTION_FUSIBLESBUTION} - {exemplaire.immatriculation}"
                        )

                        messages.success(request, _("Intervention enregistrée avec succès."))


                        return redirect(
                            f"{reverse('fusibles:fusibles_list', kwargs={'exemplaire_id': exemplaire.id})}?saved=1"
                        )


            except Exception as e:
                messages.error(request, _("Erreur lors de l'enregistrement : %(erreur)s") % {"erreur": str(e)})

        else:
            messages.error(request, _("Le formulaire contient des erreurs."))
            print(form.errors)
    else:
        fusibles_nouveau = Fusibles(
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
        fusibles_nouveau.assign_technicien(request.user)

        form = FusiblesForm(
            instance=fusibles_nouveau,
            user=request.user,
            exemplaire=exemplaire
        )
        detail_fs = FusibleDetailFormSet(instance=Fusibles(), prefix="detail")

    # --- Génération des champs par section ---
    sections = [
        {
            "title": _("Kilométrage"),
            "icon": "icons/compteur.png",
            "fields": [form[f.name] for f in form if "kilo" in f.name],
        },
        {
            "title": _("Boîte à fusibles compartiment moteur"),
            "icon": "icons/fusibles_boite_moteur.png",
            "fields": [form[f.name] for f in form if f.name == "boite_fusibles_moteur" or f.name.startswith("boite_fusibles_moteur_")],
        },
        {
            "title": _("Boîte à fusibles habitacle (côté conducteur)"),
            "icon": "icons/fusibles_boite_habitacle.png",
            "fields": [form[f.name] for f in form if f.name == "boite_fusibles_habitacle" or f.name.startswith("boite_fusibles_habitacle_")],
        },
        {
            "title": _("Boîte à fusibles coffre / arrière"),
            "icon": "icons/fusibles_boite_coffre.png",
            "fields": [form[f.name] for f in form if f.name == "boite_fusibles_coffre" or f.name.startswith("boite_fusibles_coffre_")],
        },
        {
            "title": _("Fusibles à lame (standard)"),
            "icon": "icons/fusibles_fusible_lame.png",
            "fields": [form[f.name] for f in form if f.name == "fusibles_lame" or f.name.startswith("fusibles_lame_")],
        },
        {
            "title": _("Mini-fusibles"),
            "icon": "icons/fusibles_mini_fusible.png",
            "fields": [form[f.name] for f in form if f.name == "mini_fusibles" or f.name.startswith("mini_fusibles_")],
        },
        {
            "title": _("Maxi-fusibles"),
            "icon": "icons/fusibles_maxi_fusible.png",
            "fields": [form[f.name] for f in form if f.name == "maxi_fusibles" or f.name.startswith("maxi_fusibles_")],
        },
        {
            "title": _("Méga-fusibles (fusibles à vis)"),
            "icon": "icons/fusibles_mega_fusible.png",
            "fields": [form[f.name] for f in form if f.name == "mega_fusibles" or f.name.startswith("mega_fusibles_")],
        },
        {
            "title": _("Relais"),
            "icon": "icons/fusibles_relais.png",
            "fields": [form[f.name] for f in form if f.name == "relais_fusibles" or f.name.startswith("relais_fusibles_")],
        },
        {
            "title": _("Contrôle des fusibles (test de continuité)"),
            "icon": "icons/fusibles_controle.png",
            "fields": [form[f.name] for f in form if f.name == "controle_fusibles" or f.name.startswith("controle_fusibles_")],
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

    return render(request, 'fusibles/fusibles_form.html', {
        "exemplaire": exemplaire,
        "immatriculation": exemplaire.immatriculation,
        "maintenance": maintenance,
        "form": form,
        "detail_fs": detail_fs,
        "amperages_fusibles": AMPERAGES_FUSIBLES,
        "ligne_par_type_json": json.dumps({str(k): v for k, v in LIGNE_PAR_TYPE.items()}),
        "sections": sections,
        "now": timezone.now(),
    })






# ------------
# Vue détail fusibles
# -----------------------------

@never_cache
@login_required
def fusibles_detail_view(request, fusibles_id):
    fusibles = get_object_or_404(
        Fusibles.objects.select_related("voiture_exemplaire").filter(q_intervention_tenant(request.user)),
        id=fusibles_id
    )

    context = {
        "fusibles": fusibles,
        "exemplaire": fusibles.voiture_exemplaire,
    }
    return render(request, "fusibles/fusibles_detail.html", context)







@login_required
def modifier_fusibles_view(request, fusibles_id):
    tenant = request.user.societe

    fusibles = get_object_or_404(
        Fusibles.objects.select_related("voiture_exemplaire"),
        id=fusibles_id
    )
    exemplaire = fusibles.voiture_exemplaire
    # -------------------------
    # POST
    # -------------------------
    if request.method == "POST":
        form = FusiblesForm(
            request.POST,
            instance=fusibles,
            user=request.user,
            exemplaire=fusibles.voiture_exemplaire
        )
        detail_fs = FusibleDetailFormSet(request.POST, instance=fusibles, prefix="detail")

        if form.is_valid() and detail_fs.is_valid():

            try:
                with transaction.atomic():

                    # ==================================================
                    # NOUVEAU KILOMÉTRAGE SAISI
                    # ==================================================
                    km = form.cleaned_data.get(
                        "kilometrage_fusibles"
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
                    fusibles_obj = form.save(
                        commit=False
                    )

                    fusibles_obj.voiture_exemplaire = (
                        exemplaire
                    )

                    # ==================================================
                    # ROLLBACK LOCAL
                    # ==================================================
                    fusibles_obj.kilometres_chassis = (
                        rollback_chassis
                    )

                    fusibles_obj.kilometres_moteur = (
                        rollback_moteur
                    )

                    fusibles_obj.kilometres_boite = (
                        rollback_boite
                    )

                    fusibles_obj.kilometres_embrayage = (
                        rollback_embrayage
                    )

                    # ==================================================
                    # NOUVEAU KILOMÉTRAGE
                    # ==================================================
                    fusibles_obj.kilometrage_fusibles = km

                    # ==================================================
                    # VARIATION
                    # ==================================================
                    if km is not None:
                        fusibles_obj.kilometrage_variation = (
                                km - rollback_chassis
                        )
                    else:
                        fusibles_obj.kilometrage_variation = 0

                    # ==================================================
                    # TECHNICIEN
                    # ==================================================
                    fusibles_obj.assign_technicien(
                        request.user
                    )

                    fusibles_obj.tech_last_maintained_by = (
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
                    fusibles_obj.save()

                    form.save_m2m()

                    # Détail des fusibles (boîte, repère, ampérage, organe)
                    detail_fs.instance = fusibles_obj
                    detail_fs.save()
                    # quantités facturées = fusibles remplacés par type
                    synchroniser_quantites(fusibles_obj)



                    ACTION_MODIFICATION_FUSIBLESBUTION = gettext_noop(
                        "Modification intervention boîtes à fusibles"
                    )

                    UserLog.objects.create(
                        utilisateur=request.user,
                        action=f"{ACTION_MODIFICATION_FUSIBLESBUTION} - {exemplaire.immatriculation}"
                    )

                    messages.success(
                        request,
                        _("Intervention modifiée avec succès !")
                    )

                    return redirect(
                        f"{reverse('fusibles:fusibles_detail', kwargs={'fusibles_id': fusibles.id})}?saved=1"
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
        form = FusiblesForm(
            instance=fusibles,
            user=request.user,
            exemplaire=fusibles.voiture_exemplaire
        )
        detail_fs = FusibleDetailFormSet(instance=fusibles, prefix="detail")

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
            "title": _("Boîte à fusibles compartiment moteur"),
            "icon": "icons/fusibles_boite_moteur.png",
            "fields": [form[f.name] for f in form if f.name == "boite_fusibles_moteur" or f.name.startswith("boite_fusibles_moteur_")],
        },
        {
            "title": _("Boîte à fusibles habitacle (côté conducteur)"),
            "icon": "icons/fusibles_boite_habitacle.png",
            "fields": [form[f.name] for f in form if f.name == "boite_fusibles_habitacle" or f.name.startswith("boite_fusibles_habitacle_")],
        },
        {
            "title": _("Boîte à fusibles coffre / arrière"),
            "icon": "icons/fusibles_boite_coffre.png",
            "fields": [form[f.name] for f in form if f.name == "boite_fusibles_coffre" or f.name.startswith("boite_fusibles_coffre_")],
        },
        {
            "title": _("Fusibles à lame (standard)"),
            "icon": "icons/fusibles_fusible_lame.png",
            "fields": [form[f.name] for f in form if f.name == "fusibles_lame" or f.name.startswith("fusibles_lame_")],
        },
        {
            "title": _("Mini-fusibles"),
            "icon": "icons/fusibles_mini_fusible.png",
            "fields": [form[f.name] for f in form if f.name == "mini_fusibles" or f.name.startswith("mini_fusibles_")],
        },
        {
            "title": _("Maxi-fusibles"),
            "icon": "icons/fusibles_maxi_fusible.png",
            "fields": [form[f.name] for f in form if f.name == "maxi_fusibles" or f.name.startswith("maxi_fusibles_")],
        },
        {
            "title": _("Méga-fusibles (fusibles à vis)"),
            "icon": "icons/fusibles_mega_fusible.png",
            "fields": [form[f.name] for f in form if f.name == "mega_fusibles" or f.name.startswith("mega_fusibles_")],
        },
        {
            "title": _("Relais"),
            "icon": "icons/fusibles_relais.png",
            "fields": [form[f.name] for f in form if f.name == "relais_fusibles" or f.name.startswith("relais_fusibles_")],
        },
        {
            "title": _("Contrôle des fusibles (test de continuité)"),
            "icon": "icons/fusibles_controle.png",
            "fields": [form[f.name] for f in form if f.name == "controle_fusibles" or f.name.startswith("controle_fusibles_")],
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
        "fusibles/modifier_fusibles.html",
        {
            "form": form,
            "detail_fs": detail_fs,
        "amperages_fusibles": AMPERAGES_FUSIBLES,
        "ligne_par_type_json": json.dumps({str(k): v for k, v in LIGNE_PAR_TYPE.items()}),
            "fusibles": fusibles,
            "sections": sections,
            "exemplaire": exemplaire,
        }
    )




@never_cache
@login_required
def delete_fusibles_view(request, fusibles_id):

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
    fusibles = get_object_or_404(
        Fusibles.objects.select_related(
            "voiture_exemplaire",
            "maintenance",
        ),
        id=fusibles_id,
    )

    exemplaire = fusibles.voiture_exemplaire
    maintenance = fusibles.maintenance

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
                fusibles.delete()

                # ==================================================
                # SUPPRESSION MAINTENANCE ASSOCIÉE
                # ==================================================
                if maintenance:
                    maintenance.delete()

                # ==================================================
                # USER LOG
                # ==================================================
                ACTION_SUPPRESSION_ATERNATEUR = gettext_noop(
                    "Suppression de l'intervention boîtes à fusibles"
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
                f"{reverse('fusibles:fusibles_list', kwargs={'exemplaire_id': exemplaire.id})}?deleted=1"
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
        "fusibles/delete_fusibles.html",
        {
            "fusibles": fusibles,
            "exemplaire": exemplaire,
        }
    )








@login_required
def fusibles_detail_pdf_view(request, pk):
    fusibles = get_object_or_404(Fusibles, pk=pk)

    rapport = fusibles.generer_rapport_remplacement()

    html_string = render_to_string(
        "fusibles/fusibles_detail_pdf.html",
        {
            "fusibles": fusibles,
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
        fusibles.voiture_exemplaire.immatriculation
        if fusibles.voiture_exemplaire
        else "sans_immatriculation"
    )

    # =========================================================
    # TECHNICIEN
    # =========================================================

    technicien = (
            fusibles.tech_nom_technicien
            or "technicien_inconnu"
    )

    # Nettoyage pour le nom du fichier
    technicien = str(technicien).replace(" ", "_")
    immatriculation = str(immatriculation).replace(" ", "_")

    # =========================================================
    # DATE
    # =========================================================

    date_pdf = (
        fusibles.date.strftime("%Y-%m-%d")
        if fusibles.date
        else timezone.now().strftime("%Y-%m-%d")
    )

    # =========================================================
    # TITRE / NOM DU PDF
    # =========================================================

    titre_pdf = str(_("Boîtes à fusibles")).replace(" ", "_").replace("'", "")
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
