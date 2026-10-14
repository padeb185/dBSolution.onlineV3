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
from maintenance.esthetique.ceramique.models import Ceramique
from maintenance.esthetique.ceramique.forms import CeramiqueForm
from weasyprint import HTML
from utils.securite import q_intervention_tenant







@method_decorator([login_required, never_cache], name='dispatch')
class CeramiqueListView(ListView):
    model = Ceramique
    template_name = "ceramique/ceramique_list.html"
    context_object_name = "interventions"
    ordering = ["-id"]

    def get_queryset(self):
        queryset = Ceramique.objects.select_related(
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
def ceramique_form_view(request, exemplaire_id):
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

        form = CeramiqueForm(
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

                km = form.cleaned_data.get("kilometrage_ceramique")


                if km is None:
                    form.add_error(
                        "kilometrage_ceramique",
                        _("Le kilométrage est obligatoire."),
                    )

                else:
                    km = int(km)

                    if km < ancien_kilometrage:
                        form.add_error(
                            "kilometrage_ceramique",
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
                                type_maintenance=Maintenance.TypeMaintenance.CERAMIQUE,
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
                            # CONTRÔLE
                            # ==================================================
                            obj_ceramique = form.save(commit=False)


                            obj_ceramique.voiture_exemplaire = (
                                exemplaire
                            )

                            obj_ceramique.maintenance = (
                                maintenance
                            )

                            # ---------------------------------------------
                            # Kilométrage AVANT intervention
                            # ---------------------------------------------
                            obj_ceramique.kilometres_chassis = (
                                ancien_kilometrage
                            )

                            obj_ceramique.kilometres_boite = (
                                ancien_kilometrage_boite
                            )

                            obj_ceramique.kilometres_moteur = (
                                ancien_kilometrage_moteur
                            )

                            obj_ceramique.kilometres_embrayage = (
                                ancien_kilometrage_embrayage
                            )


                            # ---------------------------------------------
                            # Kilométrage_distri
                            # ---------------------------------------------
                            obj_ceramique.kilometrage_ceramique = km

                            # ---------------------------------------------
                            # Variation kilométrique
                            # ---------------------------------------------
                            obj_ceramique.kilometrage_variation = (
                                kilometrage_variation
                            )

                            # =============================================
                            # TECHNICIEN
                            # =============================================
                            obj_ceramique.assign_technicien(
                                request.user
                            )

                            obj_ceramique.tech_last_maintained_by = (
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
                            if obj_ceramique.main_oeuvre_id:

                                main_oeuvre = (
                                    obj_ceramique.main_oeuvre
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

                                obj_ceramique.main_oeuvre = (
                                    main_oeuvre
                                )

                            # ==================================================
                            # SAUVEGARDE obj_ceramique
                            # IMPORTANT :
                            # EN DEHORS DU IF/ELSE MAIN-D'ŒUVRE
                            # ==================================================
                            obj_ceramique.save()

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



                        ACTION_CERAMIQUE = gettext_noop(
                            "Traitement céramique"
                        )

                        UserLog.objects.create(
                            utilisateur=request.user,
                            action=f"{ACTION_CERAMIQUE} - {exemplaire.immatriculation}"
                        )

                        messages.success(request, _("Traitement céramique enregistré avec succès."))


                        return redirect(
                            f"{reverse('ceramique:ceramique_list', kwargs={'exemplaire_id': exemplaire.id})}?saved=1"
                        )


            except Exception as e:
                messages.error(request, _(f"Erreur lors de l'enregistrement : {str(e)}"))

        else:
            messages.error(request, _("Le formulaire contient des erreurs."))
            print(form.errors)
    else:
        ceramique = Ceramique(
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
        ceramique.assign_technicien(request.user)

        form = CeramiqueForm(
            instance=ceramique,
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
            "title": _("Préparation / dégraissage (panel wipe)"),
            "icon": "icons/preparation_ceramique.png",
            "fields": [form[f.name] for f in form if f.name.startswith("preparation_ceramique")],
        },
        {
            "title": _("Revêtement céramique carrosserie"),
            "icon": "icons/ceramique_carrosserie.png",
            "fields": [form[f.name] for f in form if f.name.startswith("ceramique_carrosserie")],
        },
        {
            "title": _("Couche supplémentaire / top coat"),
            "icon": "icons/couche_supplementaire.png",
            "fields": [form[f.name] for f in form if f.name.startswith("couche_supplementaire")],
        },
        {
            "title": _("Céramique jantes / étriers"),
            "icon": "icons/ceramique_jantes.png",
            "fields": [form[f.name] for f in form if f.name.startswith("ceramique_jantes")],
        },
        {
            "title": _("Céramique vitres"),
            "icon": "icons/ceramique_vitres.png",
            "fields": [form[f.name] for f in form if f.name.startswith("ceramique_vitres")],
        },
        {
            "title": _("Céramique plastiques / garnitures"),
            "icon": "icons/ceramique_plastiques.png",
            "fields": [form[f.name] for f in form if f.name.startswith("ceramique_plastiques")],
        },
        {
            "title": _("Céramique optiques"),
            "icon": "icons/ceramique_optiques.png",
            "fields": [form[f.name] for f in form if f.name.startswith("ceramique_optiques")],
        },
        {
            "title": _("Cuisson / séchage infrarouge"),
            "icon": "icons/sechage_infrarouge.png",
            "fields": [form[f.name] for f in form if f.name.startswith("sechage_infrarouge")],
        },
        {
            "title": _("Produit d'entretien (shampoing / spray)"),
            "icon": "icons/entretien_ceramique.png",
            "fields": [form[f.name] for f in form if f.name.startswith("entretien_ceramique")],
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

    return render(request, 'ceramique/ceramique_form.html', {
        "exemplaire": exemplaire,
        "immatriculation": exemplaire.immatriculation,
        "maintenance": maintenance,
        "form": form,
        "sections": sections,
        "now": timezone.now(),
    })






# ------------
# Vue détail obj
# -----------------------------

@never_cache
@login_required
def ceramique_detail_view(request, ceramique_id):
    obj = get_object_or_404(
        Ceramique.objects.select_related("voiture_exemplaire").filter(q_intervention_tenant(request.user)),
        id=ceramique_id
    )

    context = {
        "obj": obj,
        "exemplaire": obj.voiture_exemplaire,
    }
    return render(request, "ceramique/ceramique_detail.html", context)







@login_required
def modifier_ceramique_view(request, ceramique_id):
    tenant = request.user.societe

    obj = get_object_or_404(
        Ceramique.objects.select_related("voiture_exemplaire"),
        id=ceramique_id
    )
    exemplaire = obj.voiture_exemplaire
    # -------------------------
    # POST
    # -------------------------
    if request.method == "POST":
        form = CeramiqueForm(
            request.POST,
            instance=obj,
            user=request.user,
            exemplaire=obj.voiture_exemplaire
        )

        if form.is_valid():

            try:
                with transaction.atomic():

                    # ==================================================
                    # NOUVEAU KILOMÉTRAGE SAISI
                    # ==================================================
                    km = form.cleaned_data.get(
                        "kilometrage_ceramique"
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
                    obj_ceramique = form.save(
                        commit=False
                    )

                    obj_ceramique.voiture_exemplaire = (
                        exemplaire
                    )

                    # ==================================================
                    # ROLLBACK LOCAL
                    # ==================================================
                    obj_ceramique.kilometres_chassis = (
                        rollback_chassis
                    )

                    obj_ceramique.kilometres_moteur = (
                        rollback_moteur
                    )

                    obj_ceramique.kilometres_boite = (
                        rollback_boite
                    )

                    obj_ceramique.kilometres_embrayage = (
                        rollback_embrayage
                    )

                    # ==================================================
                    # NOUVEAU KILOMÉTRAGE
                    # ==================================================
                    obj_ceramique.kilometrage_alte = km

                    # ==================================================
                    # VARIATION
                    # ==================================================
                    if km is not None:
                        obj_ceramique.kilometrage_variation = (
                                km - rollback_chassis
                        )
                    else:
                        obj_ceramique.kilometrage_variation = 0

                    # ==================================================
                    # TECHNICIEN
                    # ==================================================
                    obj_ceramique.assign_technicien(
                        request.user
                    )

                    obj_ceramique.tech_last_maintained_by = (
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
                    obj_ceramique.save()

                    form.save_m2m()



                    ACTION_MODIFICATION_CERAMIQUE = gettext_noop(
                        "Modification du traitement céramique"
                    )

                    UserLog.objects.create(
                        utilisateur=request.user,
                        action=f"{ACTION_MODIFICATION_CERAMIQUE} - {exemplaire.immatriculation}"
                    )

                    messages.success(
                        request,
                        _("Traitement céramique modifié avec succès !")
                    )

                    return redirect(
                        f"{reverse('ceramique:ceramique_detail', kwargs={'ceramique_id': obj.id})}?saved=1"
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
        form = CeramiqueForm(
            instance=obj,
            user=request.user,
            exemplaire=obj.voiture_exemplaire
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
            "title": _("Préparation / dégraissage (panel wipe)"),
            "icon": "icons/preparation_ceramique.png",
            "fields": [form[f.name] for f in form if f.name.startswith("preparation_ceramique")],
        },
        {
            "title": _("Revêtement céramique carrosserie"),
            "icon": "icons/ceramique_carrosserie.png",
            "fields": [form[f.name] for f in form if f.name.startswith("ceramique_carrosserie")],
        },
        {
            "title": _("Couche supplémentaire / top coat"),
            "icon": "icons/couche_supplementaire.png",
            "fields": [form[f.name] for f in form if f.name.startswith("couche_supplementaire")],
        },
        {
            "title": _("Céramique jantes / étriers"),
            "icon": "icons/ceramique_jantes.png",
            "fields": [form[f.name] for f in form if f.name.startswith("ceramique_jantes")],
        },
        {
            "title": _("Céramique vitres"),
            "icon": "icons/ceramique_vitres.png",
            "fields": [form[f.name] for f in form if f.name.startswith("ceramique_vitres")],
        },
        {
            "title": _("Céramique plastiques / garnitures"),
            "icon": "icons/ceramique_plastiques.png",
            "fields": [form[f.name] for f in form if f.name.startswith("ceramique_plastiques")],
        },
        {
            "title": _("Céramique optiques"),
            "icon": "icons/ceramique_optiques.png",
            "fields": [form[f.name] for f in form if f.name.startswith("ceramique_optiques")],
        },
        {
            "title": _("Cuisson / séchage infrarouge"),
            "icon": "icons/sechage_infrarouge.png",
            "fields": [form[f.name] for f in form if f.name.startswith("sechage_infrarouge")],
        },
        {
            "title": _("Produit d'entretien (shampoing / spray)"),
            "icon": "icons/entretien_ceramique.png",
            "fields": [form[f.name] for f in form if f.name.startswith("entretien_ceramique")],
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
        "ceramique/modifier_ceramique.html",
        {
            "form": form,
            "obj": obj,
            "sections": sections,
            "exemplaire": exemplaire,
        }
    )




@never_cache
@login_required
def delete_ceramique_view(request, ceramique_id):

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
    obj = get_object_or_404(
        Ceramique.objects.select_related(
            "voiture_exemplaire",
            "maintenance",
        ),
        id=ceramique_id,
    )

    exemplaire = obj.voiture_exemplaire
    maintenance = obj.maintenance

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
                obj.delete()

                # ==================================================
                # SUPPRESSION MAINTENANCE ASSOCIÉE
                # ==================================================
                if maintenance:
                    maintenance.delete()

                # ==================================================
                # USER LOG
                # ==================================================
                ACTION_SUPPRESSION_ATERNATEUR = gettext_noop(
                    "Suppression du traitement céramique"
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
                _("Traitement céramique supprimé avec succès.")
            )

            return redirect(
                f"{reverse('ceramique:ceramique_list', kwargs={'exemplaire_id': exemplaire.id})}?deleted=1"
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
        "ceramique/delete_ceramique.html",
        {
            "obj": obj,
            "exemplaire": exemplaire,
        }
    )








@login_required
def ceramique_detail_pdf_view(request, pk):
    obj = get_object_or_404(Ceramique, pk=pk)

    rapport = obj.generer_rapport_remplacement()

    html_string = render_to_string(
        "ceramique/ceramique_detail_pdf.html",
        {
            "obj": obj,
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
        obj.voiture_exemplaire.immatriculation
        if obj.voiture_exemplaire
        else "sans_immatriculation"
    )

    # =========================================================
    # TECHNICIEN
    # =========================================================

    technicien = (
            obj.tech_nom_technicien
            or "technicien_inconnu"
    )

    # Nettoyage pour le nom du fichier
    technicien = str(technicien).replace(" ", "_")
    immatriculation = str(immatriculation).replace(" ", "_")

    # =========================================================
    # DATE
    # =========================================================

    date_pdf = (
        obj.date.strftime("%Y-%m-%d")
        if obj.date
        else timezone.now().strftime("%Y-%m-%d")
    )

    # =========================================================
    # TITRE / NOM DU PDF
    # =========================================================

    nom_fichier = (
        f"{_('Traitement céramique')}_{technicien}_{immatriculation}_{date_pdf}.pdf"
    )

    response = HttpResponse(
        pdf,
        content_type="application/pdf",
    )

    response["Content-Disposition"] = (
        f'inline; filename="{nom_fichier}"'
    )

    return response
