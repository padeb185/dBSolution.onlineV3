from datetime import datetime

from django.core.exceptions import ValidationError

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import ListView
from maintenance.models import Maintenance
from utilisateurs.models import UserLog
from voiture.voiture_exemplaire.models import VoitureExemplaire
from django.db.models import Q
from django.utils.translation import gettext_lazy as _, gettext_noop
from weasyprint import HTML
from .forms import EmbrayageForm
from .models import Embrayage
from django.db import connection, transaction





@method_decorator([login_required, never_cache], name="dispatch")
class EmbrayageListView(ListView):
    model = Embrayage
    template_name = "embrayage/embrayage_list.html"
    context_object_name = "embrayages"


    def get_queryset(self):
        user = self.request.user
        tenant = user.societe

        exemplaire_id = self.kwargs.get("exemplaire_id")

        queryset = Embrayage.objects.select_related(
            "voiture_exemplaire",
            "maintenance",
            "tech_societe",
            "tech_technicien",
        )

        # =========================
        # FILTRE PAR VÉHICULE
        # =========================
        if exemplaire_id:
            queryset = queryset.filter(
                voiture_exemplaire_id=exemplaire_id
            )

        # =========================
        # SÉCURITÉ SOCIÉTÉ
        # =========================
        queryset = queryset.filter(
            Q(voiture_exemplaire__client__societe=tenant)
            |
            Q(
                voiture_exemplaire__client__isnull=True,
                voiture_exemplaire__societe=tenant,
            )
        )

        return queryset.order_by("-id")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        tenant = self.request.user.societe
        exemplaire_id = self.kwargs.get("exemplaire_id")

        if exemplaire_id:
            context["exemplaire"] = get_object_or_404(
                VoitureExemplaire.objects.filter(
                    Q(client__societe=tenant)
                    |
                    Q(
                        client__isnull=True,
                        societe=tenant,
                    )
                ),
                id=exemplaire_id,
            )

        roles_autorises = [
            "mecanicien",
            "apprenti",
            "magasinier",
            "chef_mecanicien",
            "direction",
        ]

        context["is_checkup_allowed"] = (
            self.request.user.role
            in roles_autorises
        )

        return context


@never_cache
@login_required
def embrayage_form_view(request, exemplaire_id):

    tenant = request.user.societe
    role = request.user.role

    maintenance = None

    # =========================================================
    # RÉCUPÉRATION DU VÉHICULE
    # =========================================================
    exemplaire = get_object_or_404(
        VoitureExemplaire.objects.filter(
            Q(client__societe=tenant)
            | Q(
                client__isnull=True,
                societe=tenant,
            )
        ),
        id=exemplaire_id,
    )

    # =========================================================
    # CONTRÔLE DES RÔLES
    # =========================================================
    roles_autorises = [
        "mecanicien",
        "apprenti",
        "magasinier",
        "chef_mecanicien",
        "direction",
    ]

    if role not in roles_autorises:
        messages.error(
            request,
            _("Accès refusé."),
        )

        return redirect(
            "utilisateurs:dashboard"
        )

    # =========================================================
    # POST
    # =========================================================
    if request.method == "POST":

        instance_embrayage = Embrayage(
            voiture_exemplaire=exemplaire,
            kilometres_chassis=exemplaire.kilometres_chassis,
        )

        instance_embrayage.assign_technicien(
            request.user
        )

        form = EmbrayageForm(
            request.POST,
            instance=instance_embrayage,
            user=request.user,
            exemplaire=exemplaire,
        )

        # =====================================================
        # FORMULAIRE VALIDE
        # =====================================================
        if form.is_valid():

            try:
                # =====================================================
                # KILOMÉTRAGE (valeurs avant modification)
                # =====================================================
                ancien_kilometrage = exemplaire.kilometres_chassis or 0
                ancien_kilometrage_boite = exemplaire.kilometres_boite or 0
                ancien_kilometrage_moteur = exemplaire.kilometres_moteur or 0
                ancien_kilometrage_embrayage = exemplaire.kilometres_embrayage or 0

                km = form.cleaned_data.get("kilometres_remplacement_embrayage")

                # -----------------------------------------------------
                # Kilométrage obligatoire
                # -----------------------------------------------------
                if km is None:

                    form.add_error(
                        "kilometres_remplacement_embrayage",
                        _("Le kilométrage est obligatoire."),
                    )

                else:
                    km = int(km)

                    # -------------------------------------------------
                    # Vérification kilométrage
                    # -------------------------------------------------
                    if km < ancien_kilometrage:

                        form.add_error(
                            "kilometres_remplacement_embrayage",
                            _(
                                "Le kilométrage du remplacement "
                                "de l'embrayage ne peut pas être "
                                "inférieur au kilométrage actuel "
                                "du véhicule."
                            ),
                        )

                    else:
                        kilometrage_variation = km - ancien_kilometrage

                        # =================================================
                        # TRANSACTION
                        # =================================================
                        with transaction.atomic():

                            # ---------------- VÉHICULE ----------------
                            exemplaire.kilometres_rollback = ancien_kilometrage
                            exemplaire.kilometres_boite_rollback = ancien_kilometrage_boite
                            exemplaire.kilometres_moteur_rollback = ancien_kilometrage_moteur
                            exemplaire.kilometres_embrayage_rollback = ancien_kilometrage_embrayage

                            exemplaire.date_derniere_intervention = (
                                timezone.localtime(timezone.now()).date()
                            )

                            exemplaire.kilometres_chassis = km

                            # Point de départ du nouvel embrayage
                            exemplaire.kilometres_remplacement_embrayage = km

                            # → kilometres_embrayage = km - km = 0
                            exemplaire.update_kilometres()

                            exemplaire.save(
                                update_fields=[
                                    "kilometres_chassis",
                                    "date_derniere_intervention",

                                    "kilometres_rollback",
                                    "kilometres_boite_rollback",
                                    "kilometres_moteur_rollback",
                                    "kilometres_embrayage_rollback",

                                    "kilometres_remplacement_embrayage",

                                    "kilometres_moteur",
                                    "kilometres_boite",
                                    "kilometres_embrayage",
                                    "variation_kilometres",
                                ]
                            )

                            # ---------------- MAINTENANCE ----------------
                            maintenance = Maintenance.objects.create(
                                societe=request.user.societe,
                                voiture_exemplaire=exemplaire,
                                immatriculation=exemplaire.immatriculation,
                                date_intervention=timezone.now().date(),
                                kilometres_chassis=exemplaire.kilometres_chassis,
                                kilometres_dernier_entretien=exemplaire.kilometres_dernier_entretien,
                                type_maintenance=Maintenance.TypeMaintenance.EMBRAYAGE,
                                tag=Maintenance.Tag.JAUNE,
                                tech_technicien=request.user,
                                tech_societe=request.user.societe,
                                tech_nom_technicien=f"{request.user.prenom} {request.user.nom}",
                                tech_role_technicien=request.user.role,
                            )

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

                            # ---------------- EMBRAYAGE ----------------
                            embrayage = form.save(commit=False)  # ← embrayage est défini ICI

                            embrayage.voiture_exemplaire = exemplaire
                            embrayage.maintenance = maintenance

                            # Kilométrages AVANT intervention
                            embrayage.kilometres_chassis = ancien_kilometrage
                            embrayage.kilometres_boite = ancien_kilometrage_boite
                            embrayage.kilometres_moteur = ancien_kilometrage_moteur
                            embrayage.kilometres_embrayage = ancien_kilometrage_embrayage

                            # Kilométrage du remplacement + variation
                            embrayage.kilometres_remplacement_embrayage = km
                            embrayage.kilometrage_embrayage = km  # ← remis : colonne NOT NULL
                            embrayage.kilometrage_variation = kilometrage_variation

                            embrayage.assign_technicien(request.user)
                            embrayage.tech_last_maintained_by = request.user

                            embrayage.save()
                            form.save_m2m()

                            # =============================================
                            # LOG
                            # =============================================
                            ACTION_REMPLACEMENT_EMBRAYAGE = (
                                gettext_noop(
                                    "Remplacement de l'embrayage"
                                )
                            )

                            UserLog.objects.create(
                                utilisateur=request.user,
                                action=(
                                    f"{ACTION_REMPLACEMENT_EMBRAYAGE} - "
                                    f"{exemplaire.immatriculation}"
                                ),
                            )

                        # =================================================
                        # SUCCÈS
                        # =================================================
                        messages.success(
                            request,
                            _(
                                "Le remplacement de l'embrayage "
                                "a été enregistré avec succès."
                            ),
                        )

                        return redirect(
                            f"{reverse('embrayage:embrayage_list', kwargs={'exemplaire_id': exemplaire.id})}?saved=1"
                        )


            except Exception as e:

                messages.error(
                    request,
                    _(
                        "Erreur lors de "
                        "l'enregistrement : "
                        "%(erreur)s"
                    ) % {
                        "erreur": str(e),
                    },
                )

        # =====================================================
        # FORMULAIRE INVALIDE
        # =====================================================
        else:

            messages.error(
                request,
                _(
                    "Le formulaire contient "
                    "des erreurs."
                ),
            )

    # =========================================================
    # GET
    # =========================================================
    else:

        instance_embrayage = Embrayage(
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

        instance_embrayage.assign_technicien(
            request.user
        )

        form = EmbrayageForm(
            instance=instance_embrayage,
            user=request.user,
            exemplaire=exemplaire,
        )

    # =========================================================
    # SECTIONS
    # =========================================================
    sections = [
        {
            "title": _("Kilométrage"),
            "icon": "icons/compteur.png",
            "fields": [
                form[f.name]
                for f in form
                if "kilo" in f.name
            ],
        },
        {
            "title": _("Disque d'embrayage"),
            "icon": "icons/disque-dembrayage.png",
            "fields": [
                form[f.name]
                for f in form
                if "disque_embrayage" in f.name
            ],
        },
        {
            "title": _("Plateau d'embrayage"),
            "icon": "icons/plateau-emb.png",
            "fields": [
                form[f.name]
                for f in form
                if "mecanisme_embrayage" in f.name
            ],
        },
        {
            "title": _("Butée d'embrayage"),
            "icon": "icons/butee-emb.png",
            "fields": [
                form[f.name]
                for f in form
                if "butee_embrayage" in f.name
            ],
        },
        {
            "title": _("Fourchette"),
            "icon": "icons/fourchette-emb.png",
            "fields": [
                form[f.name]
                for f in form
                if "fourchette_embrayage" in f.name
            ],
        },
        {
            "title": _("Guide de la butée d'embrayage"),
            "icon": "icons/guide-emb.png",
            "fields": [
                form[f.name]
                for f in form
                if "guide_butee" in f.name
            ],
        },
        {
            "title": _("Volant Moteur"),
            "icon": "icons/volant-mot.png",
            "fields": [
                form[f.name]
                for f in form
                if "volant_moteur" in f.name
            ],
        },
        {
            "title": _("Joint SPI vilebrequin"),
            "icon": "icons/joint-spi.png",
            "fields": [
                form[f.name]
                for f in form
                if "joint_spi_vilebrequin" in f.name
            ],
        },
        {
            "title": _("Joint SPI boite"),
            "icon": "icons/joint-spi.png",
            "fields": [
                form[f.name]
                for f in form
                if "joint_spi_boite" in f.name
            ],
        },
        {
            "title": _("Liquide de frein"),
            "icon": "icons/liquide_frein.png",
            "fields": [
                form[f.name]
                for f in form
                if "liquide_frein" in f.name
            ],
        },
        {
            "title": _("Etiquette"),
            "icon": "icons/tag.png",
            "fields": [
                form[f.name]
                for f in form
                if "tag" in f.name
            ],
        },
        {
            "title": _("Pays"),
            "icon": "icons/pays.png",
            "fields": [
                form[f.name]
                for f in form
                if "pays" in f.name
            ],
        },
        {
            "title": _("Remarques"),
            "icon": "icons/notes.png",
            "fields": [
                form[f.name]
                for f in form
                if "remarques" in f.name
            ],
        },
        {
            "title": _("Serrage des roues"),
            "icon": "icons/roue.png",
            "fields": [
                form[f.name]
                for f in form
                if "serrage" in f.name
            ],
        },
        {
            "title": _("Technicien"),
            "icon": "icons/mecanicien.png",
            "fields": [
                form[f.name]
                for f in form
                if "tech" in f.name
            ],
        },
        {
            "title": _("Taux horaire"),
            "icon": "icons/taux.png",
            "fields": [
                form[f.name]
                for f in form
                if "taux" in f.name
            ],
        },
    ]

    # =========================================================
    # AFFICHAGE
    # =========================================================
    return render(
        request,
        "embrayage/embrayage_form.html",
        {
            "exemplaire": exemplaire,
            "immatriculation": exemplaire.immatriculation,
            "maintenance": maintenance,
            "form": form,
            "sections": sections,
            "now": timezone.now(),
        },
    )





# ------------
# Vue détail boite
# -----------------------------
@login_required
def embrayage_detail_view(request, embrayage_id):
    embrayage = get_object_or_404(
        Embrayage.objects.select_related("voiture_exemplaire"),
        id=embrayage_id
    )

    context = {
        "embrayage": embrayage,
        "exemplaire": embrayage.voiture_exemplaire,
    }
    return render(request, "embrayage/embrayage_detail.html", context)



@login_required
def modifier_embrayage_view(request, embrayage_id):
    tenant = request.user.societe

    embrayage = get_object_or_404(
        Embrayage.objects.select_related("voiture_exemplaire"),
        id=embrayage_id
    )
    exemplaire = embrayage.voiture_exemplaire

    # -------------------------
    # SÉCURITÉ TENANT
    # -------------------------
    if not (
        (exemplaire.client and exemplaire.client.societe == tenant)
        or (exemplaire.client is None and exemplaire.societe == tenant)
    ):
        messages.error(request, _("Accès refusé"))
        return redirect("utilisateurs:dashboard")

    # -------------------------
    # VALEURS D'AVANT INTERVENTION
    # (à lire AVANT de créer le formulaire : is_valid() modifie l'instance)
    # -------------------------
    avant_chassis = embrayage.kilometres_chassis or 0
    avant_moteur = embrayage.kilometres_moteur or 0
    avant_boite = embrayage.kilometres_boite or 0
    avant_embrayage = embrayage.kilometres_embrayage or 0
    ancien_km_remplacement = embrayage.kilometres_remplacement_embrayage or 0

    # -------------------------
    # POST
    # -------------------------
    if request.method == "POST":
        form = EmbrayageForm(
            request.POST,
            instance=embrayage,
            user=request.user,
            exemplaire=exemplaire
        )

        if form.is_valid():

            try:
                with transaction.atomic():

                    km = form.cleaned_data.get("kilometres_remplacement_embrayage")

                    if km is None:
                        raise ValidationError(
                            _("Le kilométrage du remplacement est obligatoire.")
                        )
                    km = int(km)

                    # form.save(commit=False) gère aussi la main-d'œuvre
                    embrayage = form.save(commit=False)
                    embrayage.voiture_exemplaire = exemplaire

                    # On conserve les valeurs d'avant intervention
                    embrayage.kilometres_chassis = avant_chassis
                    embrayage.kilometres_moteur = avant_moteur
                    embrayage.kilometres_boite = avant_boite
                    embrayage.kilometres_embrayage = avant_embrayage

                    # Colonne NOT NULL : toujours renseignée
                    embrayage.kilometrage_embrayage = km
                    embrayage.kilometres_remplacement_embrayage = km

                    # ==================================================
                    # LE KILOMÉTRAGE DU REMPLACEMENT A CHANGÉ
                    # ==================================================
                    if km != ancien_km_remplacement:

                        if km < avant_chassis:
                            raise ValidationError(
                                _("Le kilométrage ne peut pas être inférieur à %(km)s km.")
                                % {"km": avant_chassis}
                            )

                        # Seul le remplacement pris en compte par le véhicule
                        # peut modifier ses compteurs
                        if (exemplaire.kilometres_remplacement_embrayage or 0) != ancien_km_remplacement:
                            raise ValidationError(
                                _("Seul le dernier remplacement de l'embrayage peut "
                                  "voir son kilométrage modifié.")
                            )

                        # Le châssis ne recule jamais (sinon valeurs négatives)
                        exemplaire.kilometres_chassis = max(
                            exemplaire.kilometres_chassis or 0, km
                        )

                        # Nouveau point de départ de l'embrayage → embrayage = 0
                        exemplaire.kilometres_remplacement_embrayage = km

                        exemplaire.date_derniere_intervention = (
                            timezone.localtime(timezone.now()).date()
                        )

                        exemplaire.update_kilometres()
                        exemplaire.save(update_fields=[
                            "kilometres_chassis",
                            "date_derniere_intervention",
                            "kilometres_remplacement_embrayage",
                            "kilometres_moteur",
                            "kilometres_boite",
                            "kilometres_embrayage",
                            "variation_kilometres",
                        ])

                        embrayage.kilometrage_variation = km - avant_chassis

                    # ==================================================
                    # TECHNICIEN + SAUVEGARDE
                    # ==================================================
                    embrayage.assign_technicien(request.user)
                    embrayage.tech_last_maintained_by = request.user

                    embrayage.save()
                    form.save_m2m()

                ACTION_MODIFICATION_REMPLACEMENT_EMBRAYAGE = gettext_noop(
                    "Modification du remplacement de l'embrayage"
                )

                UserLog.objects.create(
                    utilisateur=request.user,
                    action=f"{ACTION_MODIFICATION_REMPLACEMENT_EMBRAYAGE} - {exemplaire.immatriculation}"
                )

                messages.success(request, _("Remplacement de l'embrayage modifié avec succès !"))

                return redirect(
                    f"{reverse('embrayage:embrayage_detail', kwargs={'embrayage_id': embrayage.id})}?saved=1"
                )

            except ValidationError as e:
                form.add_error(None, e)
                messages.error(request, _("Kilométrage invalide"))

            except Exception as e:
                messages.error(
                    request,
                    _("Erreur lors de la modification : %(error)s") % {"error": str(e)}
                )

        else:
            messages.error(request, _("Le formulaire contient des erreurs."))

    # -------------------------
    # GET
    # -------------------------
    else:
        form = EmbrayageForm(
            instance=embrayage,
            user=request.user,
            exemplaire=embrayage.voiture_exemplaire
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
            "title": _("Disque d'embrayage"),
            "icon": "icons/disque-dembrayage.png",
            "fields": [form[f.name] for f in form if "disque_embrayage" in f.name],
        },
        {
            "title": _("Plateau d'embrayage"),
            "icon": "icons/plateau-emb.png",
            "fields": [form[f.name] for f in form if "mecanisme_embrayage" in f.name],
        },
        {
            "title": _("Butée d'embrayage"),
            "icon": "icons/butee-emb.png",
            "fields": [form[f.name] for f in form if "butee_embrayage" in f.name],
        },
        {
            "title": _("Fourchette"),
            "icon": "icons/fourchette-emb.png",
            "fields": [form[f.name] for f in form if "fourchette_embrayage" in f.name],
        },
        {
            "title": _("Guide de la butée d'embrayage"),
            "icon": "icons/guide-emb.png",
            "fields": [form[f.name] for f in form if "guide_butee" in f.name],
        },
        {
            "title": _("Volant Moteur"),
            "icon": "icons/volant-mot.png",
            "fields": [form[f.name] for f in form if "volant_moteur" in f.name],
        },
        {
            "title": _("Joint SPI vilebrequin"),
            "icon": "icons/joint-spi.png",
            "fields": [form[f.name] for f in form if "joint_spi_vilebrequin" in f.name],
        },
        {
            "title": _("Joint SPI boite"),
            "icon": "icons/joint-spi.png",
            "fields": [form[f.name] for f in form if "joint_spi_boite" in f.name],
        },
        {
            "title": _("Liquide de frein"),
            "icon": "icons/liquide_frein.png",
            "fields": [form[f.name] for f in form if "liquide_frein" in f.name],
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
            "title": _("Taux horaire"),
            "icon": "icons/taux.png",
            "fields": [form[f.name] for f in form if "taux" in f.name],
        },

    ]

    return render(
        request,
        "embrayage/modifier_embrayage.html",
        {
            "form": form,
            "embrayage": embrayage,
            "sections": sections,
            "exemplaire": exemplaire,
        }
    )



@never_cache
@login_required
def delete_embrayage_view(request, embrayage_id):

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
    embrayage = get_object_or_404(
        Embrayage.objects.select_related(
            "voiture_exemplaire",
            "maintenance",
        ),
        id=embrayage_id,
    )

    exemplaire = embrayage.voiture_exemplaire
    maintenance = embrayage.maintenance

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

                exemplaire.kilometres_chassis = kilometrage_rollback
                exemplaire.kilometres_remplacement_embrayage = max(
                    0, kilometrage_rollback - kilometrage_rollback_embrayage
                )
                exemplaire.update_kilometres()
                exemplaire.save(update_fields=[
                    "kilometres_chassis", "kilometres_remplacement_embrayage",
                    "kilometres_moteur", "kilometres_boite", "kilometres_embrayage",
                    "variation_kilometres",
                ])

                # ==================================================
                # SUPPRESSION CHECKUP
                # ==================================================
                embrayage.delete()

                # ==================================================
                # SUPPRESSION MAINTENANCE ASSOCIÉE
                # ==================================================
                if maintenance:
                    maintenance.delete()

                # ==================================================
                # USER LOG
                # ==================================================
                ACTION_SUPPRESSION_EMBRAYAGE = gettext_noop(
                    "Suppression du contrôle de l'embrayage"
                )

                UserLog.objects.create(
                    utilisateur=request.user,
                    action=(
                        f"{ACTION_SUPPRESSION_EMBRAYAGE} - "
                        f"{immatriculation}"
                    )
                )

            messages.success(
                request,
                _("Contrôle de l'embrayage supprimé avec succès.")
            )

            return redirect(
                "embrayage:embrayage_list",
                exemplaire_id=exemplaire.id
            )

        except Exception as e:

            messages.error(
                request,
                _("Erreur lors de la suppression : %(erreur)s")
                % {
                    "erreur": str(e)
                }
            )

            return redirect(
                "embrayage:embrayage_detail",
                 embrayage_id=embrayage.id,
            )

    # ==================================================
    # GET → CONFIRMATION
    # ==================================================
    return render(
        request,
        "embrayage/delete_embrayage.html",
        {
            "embrayage": embrayage,
            "exemplaire": exemplaire,
        }
    )








@login_required
def embrayage_detail_pdf_view(request, pk):
    embrayage = get_object_or_404(
        Embrayage.objects.select_related(
            "maintenance",
            "maintenance__voiture_exemplaire",
            "maintenance__tech_technicien",
            "maintenance__tech_societe",
            "voiture_exemplaire",
            "tech_technicien",
            "tech_societe",
            "main_oeuvre",
        ),
        pk=pk,
    )

    # -------------------------
    # RAPPORT
    # -------------------------
    rapport = embrayage.generer_rapport_remplacement()

    # -------------------------
    # MAINTENANCE
    # -------------------------
    maintenance = getattr(
        embrayage,
        "maintenance",
        None,
    )

    vehicule = None
    technicien = None
    date_intervention = None

    if maintenance:
        vehicule = getattr(
            maintenance,
            "voiture_exemplaire",
            None,
        )

        technicien = getattr(
            maintenance,
            "tech_technicien",
            None,
        )

        date_intervention = getattr(
            maintenance,
            "date_intervention",
            None,
        )

    # -------------------------
    # FALLBACK SUR EMBRAYAGE
    # -------------------------
    if vehicule is None:
        vehicule = getattr(
            embrayage,
            "voiture_exemplaire",
            None,
        )

    if technicien is None:
        technicien = getattr(
            embrayage,
            "tech_technicien",
            None,
        )

    if date_intervention is None:
        date_intervention = getattr(
            embrayage,
            "date",
            None,
        )

    # -------------------------
    # IMMATRICULATION
    # -------------------------
    if vehicule:
        immatriculation = getattr(
            vehicule,
            "immatriculation",
            "sans_immatriculation",
        )
    else:
        immatriculation = getattr(
            embrayage,
            "immatriculation",
            "sans_immatriculation",
        )

    # -------------------------
    # TECHNICIEN
    # -------------------------
    nom_technicien = "technicien_inconnu"

    if technicien:
        prenom = getattr(
            technicien,
            "prenom",
            "",
        ) or ""

        nom = getattr(
            technicien,
            "nom",
            "",
        ) or ""

        nom_technicien = (
            f"{prenom} {nom}".strip()
            or getattr(
                technicien,
                "username",
                None,
            )
            or str(technicien)
        )

    # -------------------------
    # NOM DE FICHIER
    # -------------------------
    nom_technicien_fichier = (
        str(nom_technicien)
        .strip()
        .replace(" ", "_")
        .replace("/", "-")
        .replace("\\", "-")
        .replace(",", "")
    )

    immatriculation_fichier = (
        str(immatriculation)
        .strip()
        .replace(" ", "_")
        .replace("/", "-")
        .replace("\\", "-")
        .replace(",", "")
    )

    # -------------------------
    # TEMPLATE HTML
    # -------------------------
    html_string = render_to_string(
        "embrayage/embrayage_detail_pdf.html",
        {
            "embrayage": embrayage,
            "rapport": rapport,
            "maintenance": maintenance,
            "technicien": technicien,
            "date_intervention": date_intervention,
            "vehicule": vehicule,
            "immatriculation": immatriculation,
            "date_export": datetime.now(),
            "societe": getattr(
                request.user,
                "societe",
                None,
            ),
        },
        request=request,
    )

    # -------------------------
    # GÉNÉRATION PDF
    # -------------------------
    pdf = HTML(
        string=html_string,
        base_url=request.build_absolute_uri("/"),
    ).write_pdf()

    # =========================================================
    # IMMATRICULATION
    # =========================================================

    immatriculation = (
        embrayage.voiture_exemplaire.immatriculation
        if embrayage.voiture_exemplaire
        else "sans_immatriculation"
    )

    # =========================================================
    # TECHNICIEN
    # =========================================================

    technicien = (
            embrayage.tech_nom_technicien
            or "technicien_inconnu"
    )

    # Nettoyage pour le nom du fichier
    technicien = str(technicien).replace(" ", "_")
    immatriculation = str(immatriculation).replace(" ", "_")

    # =========================================================
    # DATE
    # =========================================================

    date_pdf = (
        embrayage.date.strftime("%Y-%m-%d")
        if embrayage.date
        else timezone.now().strftime("%Y-%m-%d")
    )

    # =========================================================
    # TITRE / NOM DU PDF
    # =========================================================

    nom_fichier = (
        f"{_('Embrayage')}_{technicien}_{immatriculation}_{date_pdf}.pdf"
    )

    response = HttpResponse(
        pdf,
        content_type="application/pdf",
    )

    response["Content-Disposition"] = (
        f'inline; filename="{nom_fichier}"'
    )

    return response