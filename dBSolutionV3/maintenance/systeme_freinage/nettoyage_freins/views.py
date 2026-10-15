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
from maintenance.systeme_freinage.nettoyage_freins.models import NettoyageFreins
from maintenance.systeme_freinage.nettoyage_freins.forms import NettoyageFreinsForm
from weasyprint import HTML
from utils.securite import q_intervention_tenant







@method_decorator([login_required, never_cache], name='dispatch')
class NettoyageFreinsListView(ListView):
    model = NettoyageFreins
    template_name = "nettoyage_freins/nettoyage_freins_list.html"
    context_object_name = "nettoyage_freins_items"
    ordering = ["-id"]

    def get_queryset(self):
        queryset = NettoyageFreins.objects.select_related(
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
def nettoyage_freins_form_view(request, exemplaire_id):
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

        form = NettoyageFreinsForm(
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

                km = form.cleaned_data.get("kilometrage_nettoyage_freins")


                if km is None:
                    form.add_error(
                        "kilometrage_nettoyage_freins",
                        _("Le kilométrage est obligatoire."),
                    )

                else:
                    km = int(km)

                    if km < ancien_kilometrage:
                        form.add_error(
                            "kilometrage_nettoyage_freins",
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
                                type_maintenance=Maintenance.TypeMaintenance.NETTOYAGE_FREINS,
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
                            # CONTRÔLE COURROIE DISTRIBUTION
                            # ==================================================
                            nettoyage_freins_distri = form.save(commit=False)


                            nettoyage_freins_distri.voiture_exemplaire = (
                                exemplaire
                            )

                            nettoyage_freins_distri.maintenance = (
                                maintenance
                            )

                            # ---------------------------------------------
                            # Kilométrage AVANT intervention
                            # ---------------------------------------------
                            nettoyage_freins_distri.kilometres_chassis = (
                                ancien_kilometrage
                            )

                            nettoyage_freins_distri.kilometres_boite = (
                                ancien_kilometrage_boite
                            )

                            nettoyage_freins_distri.kilometres_moteur = (
                                ancien_kilometrage_moteur
                            )

                            nettoyage_freins_distri.kilometres_embrayage = (
                                ancien_kilometrage_embrayage
                            )


                            # ---------------------------------------------
                            # Kilométrage nettoyage des freins_distri
                            # ---------------------------------------------
                            nettoyage_freins_distri.kilometrage_nettoyage_freins = km

                            # ---------------------------------------------
                            # Variation kilométrique
                            # ---------------------------------------------
                            nettoyage_freins_distri.kilometrage_variation = (
                                kilometrage_variation
                            )

                            # =============================================
                            # TECHNICIEN
                            # =============================================
                            nettoyage_freins_distri.assign_technicien(
                                request.user
                            )

                            nettoyage_freins_distri.tech_last_maintained_by = (
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
                            if nettoyage_freins_distri.main_oeuvre_id:

                                main_oeuvre = (
                                    nettoyage_freins_distri.main_oeuvre
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

                                nettoyage_freins_distri.main_oeuvre = (
                                    main_oeuvre
                                )

                            # ==================================================
                            # SAUVEGARDE nettoyage_freins_distri
                            # IMPORTANT :
                            # EN DEHORS DU IF/ELSE MAIN-D'ŒUVRE
                            # ==================================================
                            nettoyage_freins_distri.save()

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



                        ACTION_NETTOYAGE_FREINS = gettext_noop(
                            "Nettoyage des freins"
                        )

                        UserLog.objects.create(
                            utilisateur=request.user,
                            action=f"{ACTION_NETTOYAGE_FREINS} - {exemplaire.immatriculation}"
                        )

                        messages.success(request, _("Intervention nettoyage des freins enregistrée avec succès."))


                        return redirect(
                            f"{reverse('nettoyage_freins:nettoyage_freins_list', kwargs={'exemplaire_id': exemplaire.id})}?saved=1"
                        )


            except Exception as e:
                messages.error(request, _(f"Erreur lors de l'enregistrement : {str(e)}"))

        else:
            messages.error(request, _("Le formulaire contient des erreurs."))
            print(form.errors)
    else:
        nettoyage_freins = NettoyageFreins(
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
        nettoyage_freins.assign_technicien(request.user)

        form = NettoyageFreinsForm(
            instance=nettoyage_freins,
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
            "title": _("Contrôles et mesures"),
            "icon": "icons/freins_nettoyage.png",
            "fields": [form[f.name] for f in form if f.name.startswith("controle_")],
        },
        {
            "title": _("Disques avant"),
            "icon": "icons/disque-de-frein.png",
            "fields": [form[f.name] for f in form if f.name == "disques_avant" or f.name.startswith("disques_avant_")],
        },
        {
            "title": _("Plaquettes avant"),
            "icon": "icons/plaquettes-de-frein.png",
            "fields": [form[f.name] for f in form if f.name == "plaquettes_avant" or f.name.startswith("plaquettes_avant_")],
        },
        {
            "title": _("Étriers avant"),
            "icon": "icons/etrier.png",
            "fields": [form[f.name] for f in form if f.name == "etriers_avant" or f.name.startswith("etriers_avant_")],
        },
        {
            "title": _("Disques arrière"),
            "icon": "icons/disque-de-frein.png",
            "fields": [form[f.name] for f in form if f.name == "disques_arriere" or f.name.startswith("disques_arriere_")],
        },
        {
            "title": _("Plaquettes arrière"),
            "icon": "icons/plaquettes-de-frein.png",
            "fields": [form[f.name] for f in form if f.name == "plaquettes_arriere" or f.name.startswith("plaquettes_arriere_")],
        },
        {
            "title": _("Étriers arrière"),
            "icon": "icons/etrier.png",
            "fields": [form[f.name] for f in form if f.name == "etriers_arriere" or f.name.startswith("etriers_arriere_")],
        },
        {
            "title": _("Tambours arrière"),
            "icon": "icons/boite-tambour.png",
            "fields": [form[f.name] for f in form if f.name == "tambours_arriere" or f.name.startswith("tambours_arriere_")],
        },
        {
            "title": _("Glissières / colonnettes d'étriers"),
            "icon": "icons/visserie.png",
            "fields": [form[f.name] for f in form if f.name == "glissieres" or f.name.startswith("glissieres_")],
        },
        {
            "title": _("Ressorts / clips anti-bruit"),
            "icon": "icons/visserie.png",
            "fields": [form[f.name] for f in form if f.name == "ressorts_anti_bruit" or f.name.startswith("ressorts_anti_bruit_")],
        },
        {
            "title": _("Soufflets / cache-poussière"),
            "icon": "icons/joint.png",
            "fields": [form[f.name] for f in form if f.name == "cache_poussiere" or f.name.startswith("cache_poussiere_")],
        },
        {
            "title": _("Nettoyant freins"),
            "icon": "icons/freins_nettoyage.png",
            "fields": [form[f.name] for f in form if f.name == "nettoyant_freins" or f.name.startswith("nettoyant_freins_")],
        },
        {
            "title": _("Graisse spéciale freins"),
            "icon": "icons/cardan-graisse.png",
            "fields": [form[f.name] for f in form if f.name == "graisse_freins" or f.name.startswith("graisse_freins_")],
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
            "fields": [form[f.name] for f in form if f.name.startswith("tech_")],
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

    return render(request, 'nettoyage_freins/nettoyage_freins_form.html', {
        "exemplaire": exemplaire,
        "immatriculation": exemplaire.immatriculation,
        "maintenance": maintenance,
        "form": form,
        "sections": sections,
        "now": timezone.now(),
    })






# ------------
# Vue détail nettoyage_freins
# -----------------------------

@never_cache
@login_required
def nettoyage_freins_detail_view(request, nettoyage_freins_id):
    nettoyage_freins = get_object_or_404(
        NettoyageFreins.objects.select_related("voiture_exemplaire").filter(q_intervention_tenant(request.user)),
        id=nettoyage_freins_id
    )

    context = {
        "nettoyage_freins": nettoyage_freins,
        "exemplaire": nettoyage_freins.voiture_exemplaire,
    }
    return render(request, "nettoyage_freins/nettoyage_freins_detail.html", context)







@login_required
def modifier_nettoyage_freins_view(request, nettoyage_freins_id):
    tenant = request.user.societe

    nettoyage_freins = get_object_or_404(
        NettoyageFreins.objects.select_related("voiture_exemplaire"),
        id=nettoyage_freins_id
    )
    exemplaire = nettoyage_freins.voiture_exemplaire
    # -------------------------
    # POST
    # -------------------------
    if request.method == "POST":
        form = NettoyageFreinsForm(
            request.POST,
            instance=nettoyage_freins,
            user=request.user,
            exemplaire=nettoyage_freins.voiture_exemplaire
        )

        if form.is_valid():

            try:
                with transaction.atomic():

                    # ==================================================
                    # NOUVEAU KILOMÉTRAGE SAISI
                    # ==================================================
                    km = form.cleaned_data.get(
                        "kilometrage_nettoyage_freins"
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
                    nettoyage_freins_distri = form.save(
                        commit=False
                    )

                    nettoyage_freins_distri.voiture_exemplaire = (
                        exemplaire
                    )

                    # ==================================================
                    # ROLLBACK LOCAL
                    # ==================================================
                    nettoyage_freins_distri.kilometres_chassis = (
                        rollback_chassis
                    )

                    nettoyage_freins_distri.kilometres_moteur = (
                        rollback_moteur
                    )

                    nettoyage_freins_distri.kilometres_boite = (
                        rollback_boite
                    )

                    nettoyage_freins_distri.kilometres_embrayage = (
                        rollback_embrayage
                    )

                    # ==================================================
                    # NOUVEAU KILOMÉTRAGE
                    # ==================================================
                    nettoyage_freins_distri.kilometrage_nettoyage_freins = km

                    # ==================================================
                    # VARIATION
                    # ==================================================
                    if km is not None:
                        nettoyage_freins_distri.kilometrage_variation = (
                                km - rollback_chassis
                        )
                    else:
                        nettoyage_freins_distri.kilometrage_variation = 0

                    # ==================================================
                    # TECHNICIEN
                    # ==================================================
                    nettoyage_freins_distri.assign_technicien(
                        request.user
                    )

                    nettoyage_freins_distri.tech_last_maintained_by = (
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
                    nettoyage_freins_distri.save()

                    form.save_m2m()



                    ACTION_MODIFICATION_NETTOYAGE_FREINS = gettext_noop(
                        "Modification nettoyage des freins"
                    )

                    UserLog.objects.create(
                        utilisateur=request.user,
                        action=f"{ACTION_MODIFICATION_NETTOYAGE_FREINS} - {exemplaire.immatriculation}"
                    )

                    messages.success(
                        request,
                        _("Intervention nettoyage des freins modifiée avec succès !")
                    )

                    return redirect(
                        f"{reverse('nettoyage_freins:nettoyage_freins_detail', kwargs={'nettoyage_freins_id': nettoyage_freins.id})}?saved=1"
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
        form = NettoyageFreinsForm(
            instance=nettoyage_freins,
            user=request.user,
            exemplaire=nettoyage_freins.voiture_exemplaire
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
            "title": _("Contrôles et mesures"),
            "icon": "icons/freins_nettoyage.png",
            "fields": [form[f.name] for f in form if f.name.startswith("controle_")],
        },
        {
            "title": _("Disques avant"),
            "icon": "icons/disque-de-frein.png",
            "fields": [form[f.name] for f in form if f.name == "disques_avant" or f.name.startswith("disques_avant_")],
        },
        {
            "title": _("Plaquettes avant"),
            "icon": "icons/plaquettes-de-frein.png",
            "fields": [form[f.name] for f in form if f.name == "plaquettes_avant" or f.name.startswith("plaquettes_avant_")],
        },
        {
            "title": _("Étriers avant"),
            "icon": "icons/etrier.png",
            "fields": [form[f.name] for f in form if f.name == "etriers_avant" or f.name.startswith("etriers_avant_")],
        },
        {
            "title": _("Disques arrière"),
            "icon": "icons/disque-de-frein.png",
            "fields": [form[f.name] for f in form if f.name == "disques_arriere" or f.name.startswith("disques_arriere_")],
        },
        {
            "title": _("Plaquettes arrière"),
            "icon": "icons/plaquettes-de-frein.png",
            "fields": [form[f.name] for f in form if f.name == "plaquettes_arriere" or f.name.startswith("plaquettes_arriere_")],
        },
        {
            "title": _("Étriers arrière"),
            "icon": "icons/etrier.png",
            "fields": [form[f.name] for f in form if f.name == "etriers_arriere" or f.name.startswith("etriers_arriere_")],
        },
        {
            "title": _("Tambours arrière"),
            "icon": "icons/boite-tambour.png",
            "fields": [form[f.name] for f in form if f.name == "tambours_arriere" or f.name.startswith("tambours_arriere_")],
        },
        {
            "title": _("Glissières / colonnettes d'étriers"),
            "icon": "icons/visserie.png",
            "fields": [form[f.name] for f in form if f.name == "glissieres" or f.name.startswith("glissieres_")],
        },
        {
            "title": _("Ressorts / clips anti-bruit"),
            "icon": "icons/visserie.png",
            "fields": [form[f.name] for f in form if f.name == "ressorts_anti_bruit" or f.name.startswith("ressorts_anti_bruit_")],
        },
        {
            "title": _("Soufflets / cache-poussière"),
            "icon": "icons/joint.png",
            "fields": [form[f.name] for f in form if f.name == "cache_poussiere" or f.name.startswith("cache_poussiere_")],
        },
        {
            "title": _("Nettoyant freins"),
            "icon": "icons/freins_nettoyage.png",
            "fields": [form[f.name] for f in form if f.name == "nettoyant_freins" or f.name.startswith("nettoyant_freins_")],
        },
        {
            "title": _("Graisse spéciale freins"),
            "icon": "icons/cardan-graisse.png",
            "fields": [form[f.name] for f in form if f.name == "graisse_freins" or f.name.startswith("graisse_freins_")],
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
            "fields": [form[f.name] for f in form if f.name.startswith("tech_")],
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
        "nettoyage_freins/modifier_nettoyage_freins.html",
        {
            "form": form,
            "nettoyage_freins": nettoyage_freins,
            "sections": sections,
            "exemplaire": exemplaire,
        }
    )




@never_cache
@login_required
def delete_nettoyage_freins_view(request, nettoyage_freins_id):

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
    nettoyage_freins = get_object_or_404(
        NettoyageFreins.objects.select_related(
            "voiture_exemplaire",
            "maintenance",
        ),
        id=nettoyage_freins_id,
    )

    exemplaire = nettoyage_freins.voiture_exemplaire
    maintenance = nettoyage_freins.maintenance

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
                nettoyage_freins.delete()

                # ==================================================
                # SUPPRESSION MAINTENANCE ASSOCIÉE
                # ==================================================
                if maintenance:
                    maintenance.delete()

                # ==================================================
                # USER LOG
                # ==================================================
                ACTION_SUPPRESSION_ATERNATEUR = gettext_noop(
                    "Suppression du contrôle du nettoyage des freins"
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
                _("Contrôle du nettoyage des freins supprimé avec succès.")
            )

            return redirect(
                f"{reverse('nettoyage_freins:nettoyage_freins_list', kwargs={'exemplaire_id': exemplaire.id})}?deleted=1"
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
        "nettoyage_freins/delete_nettoyage_freins.html",
        {
            "nettoyage_freins": nettoyage_freins,
            "exemplaire": exemplaire,
        }
    )








@login_required
def nettoyage_freins_detail_pdf_view(request, pk):
    nettoyage_freins = get_object_or_404(NettoyageFreins, pk=pk)

    rapport = nettoyage_freins.generer_rapport_remplacement()

    html_string = render_to_string(
        "nettoyage_freins/nettoyage_freins_detail_pdf.html",
        {
            "nettoyage_freins": nettoyage_freins,
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
        nettoyage_freins.voiture_exemplaire.immatriculation
        if nettoyage_freins.voiture_exemplaire
        else "sans_immatriculation"
    )

    # =========================================================
    # TECHNICIEN
    # =========================================================

    technicien = (
            nettoyage_freins.tech_nom_technicien
            or "technicien_inconnu"
    )

    # Nettoyage pour le nom du fichier
    technicien = str(technicien).replace(" ", "_")
    immatriculation = str(immatriculation).replace(" ", "_")

    # =========================================================
    # DATE
    # =========================================================

    date_pdf = (
        nettoyage_freins.date.strftime("%Y-%m-%d")
        if nettoyage_freins.date
        else timezone.now().strftime("%Y-%m-%d")
    )

    # =========================================================
    # TITRE / NOM DU PDF
    # =========================================================

    nom_fichier = (
        f"{_('Nettoyage des freins')}_{technicien}_{immatriculation}_{date_pdf}.pdf"
    )

    response = HttpResponse(
        pdf,
        content_type="application/pdf",
    )

    response["Content-Disposition"] = (
        f'inline; filename="{nom_fichier}"'
    )

    return response
