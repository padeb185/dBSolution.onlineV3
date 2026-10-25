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
from maintenance.autres_interventions.preparation_course.sieges_baquets.models import SiegesBaquets
from maintenance.autres_interventions.preparation_course.sieges_baquets.forms import SiegesBaquetsForm
from weasyprint import HTML
from utils.securite import atelier_requis, q_intervention_tenant







@method_decorator([login_required, never_cache], name='dispatch')
class SiegesBaquetsListView(ListView):
    model = SiegesBaquets
    template_name = "pc_sieges/pc_sieges_list.html"
    context_object_name = "pc_sieges_items"
    ordering = ["-id"]

    def get_queryset(self):
        queryset = SiegesBaquets.objects.select_related(
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
def pc_sieges_form_view(request, exemplaire_id):
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

        form = SiegesBaquetsForm(
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

                km = form.cleaned_data.get("kilometrage_pc_sieges")


                if km is None:
                    form.add_error(
                        "kilometrage_pc_sieges",
                        _("Le kilométrage est obligatoire."),
                    )

                else:
                    km = int(km)

                    if km < ancien_kilometrage:
                        form.add_error(
                            "kilometrage_pc_sieges",
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
                                type_maintenance=Maintenance.TypeMaintenance.PC_SIEGES,
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
                            # CONTRÔLE SIÈGES BAQUETS ET HARNAIS
                            # ==================================================
                            pc_sieges_obj = form.save(commit=False)


                            pc_sieges_obj.voiture_exemplaire = (
                                exemplaire
                            )

                            pc_sieges_obj.maintenance = (
                                maintenance
                            )

                            # ---------------------------------------------
                            # Kilométrage AVANT intervention
                            # ---------------------------------------------
                            pc_sieges_obj.kilometres_chassis = (
                                ancien_kilometrage
                            )

                            pc_sieges_obj.kilometres_boite = (
                                ancien_kilometrage_boite
                            )

                            pc_sieges_obj.kilometres_moteur = (
                                ancien_kilometrage_moteur
                            )

                            pc_sieges_obj.kilometres_embrayage = (
                                ancien_kilometrage_embrayage
                            )


                            # ---------------------------------------------
                            # Kilométrage pc_sieges
                            # ---------------------------------------------
                            pc_sieges_obj.kilometrage_pc_sieges = km

                            # ---------------------------------------------
                            # Variation kilométrique
                            # ---------------------------------------------
                            pc_sieges_obj.kilometrage_variation = (
                                kilometrage_variation
                            )

                            # =============================================
                            # TECHNICIEN
                            # =============================================
                            pc_sieges_obj.assign_technicien(
                                request.user
                            )

                            pc_sieges_obj.tech_last_maintained_by = (
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
                            if pc_sieges_obj.main_oeuvre_id:

                                main_oeuvre = (
                                    pc_sieges_obj.main_oeuvre
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

                                pc_sieges_obj.main_oeuvre = (
                                    main_oeuvre
                                )

                            # ==================================================
                            # SAUVEGARDE pc_sieges_obj
                            # IMPORTANT :
                            # EN DEHORS DU IF/ELSE MAIN-D'ŒUVRE
                            # ==================================================
                            pc_sieges_obj.save()

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



                        ACTION_INTERVENTION = gettext_noop(
                            "Intervention : Sièges baquets et harnais"
                        )

                        UserLog.objects.create(
                            utilisateur=request.user,
                            action=f"{ACTION_INTERVENTION} - {exemplaire.immatriculation}"
                        )

                        messages.success(request, _("Intervention enregistrée avec succès."))


                        return redirect(
                            f"{reverse('pc_sieges:pc_sieges_list', kwargs={'exemplaire_id': exemplaire.id})}?saved=1"
                        )


            except Exception as e:
                messages.error(request, _("Erreur lors de l'enregistrement : %(erreur)s") % {"erreur": str(e)})

        else:
            messages.error(request, _("Le formulaire contient des erreurs."))
            print(form.errors)
    else:
        pc_sieges_nouveau = SiegesBaquets(
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
        pc_sieges_nouveau.assign_technicien(request.user)

        form = SiegesBaquetsForm(
            instance=pc_sieges_nouveau,
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
            "title": _("Caractéristiques"),
            "icon": "icons/pc_sieges.png",
            "fields": [form[f.name] for f in form if f.name in {"norme_siege", "date_limite_siege", "norme_harnais", "nombre_points_harnais", "date_limite_harnais"}],
        },
        {
            "title": _("Baquet conducteur"),
            "icon": "icons/pc_sieges.png",
            "fields": [form[f.name] for f in form if f.name == "baquet_conducteur" or f.name.startswith("baquet_conducteur_")],
        },
        {
            "title": _("Baquet passager"),
            "icon": "icons/pc_sieges.png",
            "fields": [form[f.name] for f in form if f.name == "baquet_passager" or f.name.startswith("baquet_passager_")],
        },
        {
            "title": _("Supports / fixations de baquet"),
            "icon": "icons/pc_sieges.png",
            "fields": [form[f.name] for f in form if f.name == "supports_baquet" or f.name.startswith("supports_baquet_")],
        },
        {
            "title": _("Glissières"),
            "icon": "icons/pc_sieges.png",
            "fields": [form[f.name] for f in form if f.name == "glissieres" or f.name.startswith("glissieres_")],
        },
        {
            "title": _("Harnais conducteur"),
            "icon": "icons/pc_sieges.png",
            "fields": [form[f.name] for f in form if f.name == "harnais_conducteur" or f.name.startswith("harnais_conducteur_")],
        },
        {
            "title": _("Harnais passager"),
            "icon": "icons/pc_sieges.png",
            "fields": [form[f.name] for f in form if f.name == "harnais_passager" or f.name.startswith("harnais_passager_")],
        },
        {
            "title": _("Ancrages de harnais"),
            "icon": "icons/pc_sieges.png",
            "fields": [form[f.name] for f in form if f.name == "ancrages_harnais" or f.name.startswith("ancrages_harnais_")],
        },
        {
            "title": _("Filet de fenêtre"),
            "icon": "icons/pc_sieges.png",
            "fields": [form[f.name] for f in form if f.name == "filet_fenetre" or f.name.startswith("filet_fenetre_")],
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

    return render(request, 'pc_sieges/pc_sieges_form.html', {
        "exemplaire": exemplaire,
        "immatriculation": exemplaire.immatriculation,
        "maintenance": maintenance,
        "form": form,
        "sections": sections,
        "now": timezone.now(),
    })






# ------------
# Vue détail pc_sieges
# -----------------------------

@never_cache
@login_required
def pc_sieges_detail_view(request, pc_sieges_id):
    pc_sieges = get_object_or_404(
        SiegesBaquets.objects.select_related("voiture_exemplaire").filter(q_intervention_tenant(request.user)),
        id=pc_sieges_id
    )

    context = {
        "pc_sieges": pc_sieges,
        "exemplaire": pc_sieges.voiture_exemplaire,
    }
    return render(request, "pc_sieges/pc_sieges_detail.html", context)







@login_required
@atelier_requis
def modifier_pc_sieges_view(request, pc_sieges_id):
    tenant = request.user.societe

    pc_sieges = get_object_or_404(
        SiegesBaquets.objects.select_related("voiture_exemplaire"),
        id=pc_sieges_id
    )
    exemplaire = pc_sieges.voiture_exemplaire
    # -------------------------
    # POST
    # -------------------------
    if request.method == "POST":
        form = SiegesBaquetsForm(
            request.POST,
            instance=pc_sieges,
            user=request.user,
            exemplaire=pc_sieges.voiture_exemplaire
        )

        if form.is_valid():

            try:
                with transaction.atomic():

                    # ==================================================
                    # NOUVEAU KILOMÉTRAGE SAISI
                    # ==================================================
                    km = form.cleaned_data.get(
                        "kilometrage_pc_sieges"
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
                    pc_sieges_obj = form.save(
                        commit=False
                    )

                    pc_sieges_obj.voiture_exemplaire = (
                        exemplaire
                    )

                    # ==================================================
                    # ROLLBACK LOCAL
                    # ==================================================
                    pc_sieges_obj.kilometres_chassis = (
                        rollback_chassis
                    )

                    pc_sieges_obj.kilometres_moteur = (
                        rollback_moteur
                    )

                    pc_sieges_obj.kilometres_boite = (
                        rollback_boite
                    )

                    pc_sieges_obj.kilometres_embrayage = (
                        rollback_embrayage
                    )

                    # ==================================================
                    # NOUVEAU KILOMÉTRAGE
                    # ==================================================
                    pc_sieges_obj.kilometrage_pc_sieges = km

                    # ==================================================
                    # VARIATION
                    # ==================================================
                    if km is not None:
                        pc_sieges_obj.kilometrage_variation = (
                                km - rollback_chassis
                        )
                    else:
                        pc_sieges_obj.kilometrage_variation = 0

                    # ==================================================
                    # TECHNICIEN
                    # ==================================================
                    pc_sieges_obj.assign_technicien(
                        request.user
                    )

                    pc_sieges_obj.tech_last_maintained_by = (
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
                    pc_sieges_obj.save()

                    form.save_m2m()



                    ACTION_MODIFICATION_INTERVENTION = gettext_noop(
                        "Modification intervention : Sièges baquets et harnais"
                    )

                    UserLog.objects.create(
                        utilisateur=request.user,
                        action=f"{ACTION_MODIFICATION_INTERVENTION} - {exemplaire.immatriculation}"
                    )

                    messages.success(
                        request,
                        _("Intervention modifiée avec succès !")
                    )

                    return redirect(
                        f"{reverse('pc_sieges:pc_sieges_detail', kwargs={'pc_sieges_id': pc_sieges.id})}?saved=1"
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
        form = SiegesBaquetsForm(
            instance=pc_sieges,
            user=request.user,
            exemplaire=pc_sieges.voiture_exemplaire
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
            "title": _("Caractéristiques"),
            "icon": "icons/pc_sieges.png",
            "fields": [form[f.name] for f in form if f.name in {"norme_siege", "date_limite_siege", "norme_harnais", "nombre_points_harnais", "date_limite_harnais"}],
        },
        {
            "title": _("Baquet conducteur"),
            "icon": "icons/pc_sieges.png",
            "fields": [form[f.name] for f in form if f.name == "baquet_conducteur" or f.name.startswith("baquet_conducteur_")],
        },
        {
            "title": _("Baquet passager"),
            "icon": "icons/pc_sieges.png",
            "fields": [form[f.name] for f in form if f.name == "baquet_passager" or f.name.startswith("baquet_passager_")],
        },
        {
            "title": _("Supports / fixations de baquet"),
            "icon": "icons/pc_sieges.png",
            "fields": [form[f.name] for f in form if f.name == "supports_baquet" or f.name.startswith("supports_baquet_")],
        },
        {
            "title": _("Glissières"),
            "icon": "icons/pc_sieges.png",
            "fields": [form[f.name] for f in form if f.name == "glissieres" or f.name.startswith("glissieres_")],
        },
        {
            "title": _("Harnais conducteur"),
            "icon": "icons/pc_sieges.png",
            "fields": [form[f.name] for f in form if f.name == "harnais_conducteur" or f.name.startswith("harnais_conducteur_")],
        },
        {
            "title": _("Harnais passager"),
            "icon": "icons/pc_sieges.png",
            "fields": [form[f.name] for f in form if f.name == "harnais_passager" or f.name.startswith("harnais_passager_")],
        },
        {
            "title": _("Ancrages de harnais"),
            "icon": "icons/pc_sieges.png",
            "fields": [form[f.name] for f in form if f.name == "ancrages_harnais" or f.name.startswith("ancrages_harnais_")],
        },
        {
            "title": _("Filet de fenêtre"),
            "icon": "icons/pc_sieges.png",
            "fields": [form[f.name] for f in form if f.name == "filet_fenetre" or f.name.startswith("filet_fenetre_")],
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
        "pc_sieges/modifier_pc_sieges.html",
        {
            "form": form,
            "pc_sieges": pc_sieges,
            "sections": sections,
            "exemplaire": exemplaire,
        }
    )




@never_cache
@login_required
def delete_pc_sieges_view(request, pc_sieges_id):

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
    pc_sieges = get_object_or_404(
        SiegesBaquets.objects.select_related(
            "voiture_exemplaire",
            "maintenance",
        ),
        id=pc_sieges_id,
    )

    exemplaire = pc_sieges.voiture_exemplaire
    maintenance = pc_sieges.maintenance

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
                pc_sieges.delete()

                # ==================================================
                # SUPPRESSION MAINTENANCE ASSOCIÉE
                # ==================================================
                if maintenance:
                    maintenance.delete()

                # ==================================================
                # USER LOG
                # ==================================================
                ACTION_SUPPRESSION_ATERNATEUR = gettext_noop(
                    "Suppression de l'intervention : Sièges baquets et harnais"
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
                f"{reverse('pc_sieges:pc_sieges_list', kwargs={'exemplaire_id': exemplaire.id})}?deleted=1"
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
        "pc_sieges/delete_pc_sieges.html",
        {
            "pc_sieges": pc_sieges,
            "exemplaire": exemplaire,
        }
    )








@login_required
def pc_sieges_detail_pdf_view(request, pk):
    pc_sieges = get_object_or_404(SiegesBaquets, pk=pk)

    rapport = pc_sieges.generer_rapport_remplacement()

    html_string = render_to_string(
        "pc_sieges/pc_sieges_detail_pdf.html",
        {
            "pc_sieges": pc_sieges,
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
        pc_sieges.voiture_exemplaire.immatriculation
        if pc_sieges.voiture_exemplaire
        else "sans_immatriculation"
    )

    # =========================================================
    # TECHNICIEN
    # =========================================================

    technicien = (
            pc_sieges.tech_nom_technicien
            or "technicien_inconnu"
    )

    # Nettoyage pour le nom du fichier
    technicien = str(technicien).replace(" ", "_")
    immatriculation = str(immatriculation).replace(" ", "_")

    # =========================================================
    # DATE
    # =========================================================

    date_pdf = (
        pc_sieges.date.strftime("%Y-%m-%d")
        if pc_sieges.date
        else timezone.now().strftime("%Y-%m-%d")
    )

    # =========================================================
    # TITRE / NOM DU PDF
    # =========================================================

    titre_pdf = str(_("Sièges baquets et harnais")).replace(" ", "_").replace("'", "")
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
