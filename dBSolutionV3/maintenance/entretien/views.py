from django.core.exceptions import ValidationError

from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.db import transaction, models
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import ListView
from maintenance.models import Maintenance
from utilisateurs.models import UserLog
from voiture.voiture_exemplaire.models import VoitureExemplaire
from django.db.models import Q
from django.utils.translation import gettext_lazy as _, gettext_noop
from maintenance.entretien.models import Entretien
from maintenance.entretien.forms import EntretienForm
from utilisateurs.apprentis.models import Apprenti
from utilisateurs.chef_mecanicien.models import ChefMecanicien
from utilisateurs.direction.models import Direction
from utilisateurs.magasinier.models import Magasinier
from utilisateurs.mecanicien.models import Mecanicien
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML



# -----------------------------
# Classe ListView pour entretien
# -----------------------------
@method_decorator([login_required, never_cache], name="dispatch")
class EntretienListView(ListView):
    model = Entretien
    template_name = "entretien/entretien_list.html"
    context_object_name = "entretiens"
    ordering = ["-id"]

    def get_queryset(self):
        queryset = Entretien.objects.select_related(
            "voiture_exemplaire",
            "maintenance",
            "tech_societe",
        )

        societe = getattr(self.request.user, "societe", None)

        if societe:
            queryset = queryset.filter(
                models.Q(tech_societe=societe) |
                models.Q(tech_societe__isnull=True)
            )

        return queryset.order_by(*self.ordering)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        exemplaire_id = self.kwargs.get("exemplaire_id")

        context["exemplaire"] = get_object_or_404(
            VoitureExemplaire,
            id=exemplaire_id
        )

        context["is_checkup_allowed"] = self.request.user.role in [
            "direction",
            "mecanicien",
            "chef_mecanicien",
            "magasinier",
        ]

        return context



#----------------------------
# creation entretien
#----------------------------

@never_cache
@login_required
def entretien_check_view(request, exemplaire_id):

    tenant = request.user.societe
    role = request.user.role

    # =========================
    # VÉHICULE
    # =========================
    exemplaire = get_object_or_404(
        VoitureExemplaire.objects.filter(
            Q(client__societe=tenant) |
            Q(client__isnull=True, societe=tenant)
        ),
        id=exemplaire_id
    )

    # =========================
    # RÔLES
    # =========================
    roles_autorises = [
        "mecanicien",
        "apprenti",
        "magasinier",
        "chef_mecanicien",
        "direction",
    ]

    if role not in roles_autorises:
        messages.error(request, _("Accès refusé"))
        return redirect("utilisateurs:dashboard")

    maintenance = None

    # =========================
    # POST
    # =========================
    if request.method == "POST":

        form = EntretienForm(
            request.POST,
            user=request.user,
            exemplaire=exemplaire,
        )

        if form.is_valid():

            km = form.cleaned_data.get("kilometrage_entretien")

            # Kilométrage AVANT intervention
            ancien_kilometrage = (
                    exemplaire.kilometres_chassis or 0
            )
            ancien_kilometrage_boite = (
                    exemplaire.kilometres_boite or 0
            )

            ancien_kilometrage_moteur = (
                    exemplaire.kilometres_moteur or 0
            )

            # =========================
            # VALIDATION KM
            # =========================
            if km is not None:

                km = int(km)

                if km < ancien_kilometrage:

                    form.add_error(
                        "kilometrage_entretien",
                        _("Le kilométrage ne peut pas diminuer.")
                    )

                    messages.error(
                        request,
                        _("Le kilométrage ne peut pas diminuer.")
                    )

                    return render(
                        request,
                        "entretien/entretien_check.html",
                        {
                            "exemplaire": exemplaire,
                            "immatriculation": exemplaire.immatriculation,
                            "maintenance": maintenance,
                            "form": form,
                            "now": timezone.now(),
                        }
                    )

            try:

                with transaction.atomic():

                    # =========================
                    # VARIATION
                    # =========================
                    kilometrage_variation = 0

                    if km is not None:
                        kilometrage_variation = (
                            km - ancien_kilometrage
                        )

                    # =========================
                    # ENTRETIEN
                    # =========================
                    entretien = form.save(commit=False)

                    entretien.societe = tenant
                    entretien.voiture_exemplaire = exemplaire

                    entretien.kilometres_chassis = (
                        ancien_kilometrage
                    )



                    entretien.kilometrage_entretien = km

                    entretien.kilometrage_variation = (
                        kilometrage_variation
                    )

                    entretien.assign_technicien(request.user)

                    # =========================
                    # MISE À JOUR DU VÉHICULE
                    # =========================

                    if km is not None:
                        # =========================
                        # ROLLBACK AVANT INTERVENTION
                        # =========================

                        exemplaire.kilometres_rollback = (
                            ancien_kilometrage
                        )

                        exemplaire.kilometres_boite_rollback = (
                            ancien_kilometrage_boite
                        )

                        exemplaire.kilometres_moteur_rollback = (
                            ancien_kilometrage_moteur
                        )

                        # =========================
                        # DATE INTERVENTION
                        # =========================

                        exemplaire.date_derniere_intervention = (
                            timezone.localtime(
                                timezone.now()
                            ).date()
                        )

                        # =========================
                        # NOUVEAU KILOMÉTRAGE
                        # =========================

                        exemplaire.kilometres_chassis = km

                        # Recalcule :
                        # - kilometres_moteur
                        # - kilometres_boite
                        # - variation_kilometres
                        exemplaire.update_kilometres()

                        # =========================
                        # UNE SEULE SAUVEGARDE
                        # =========================

                        exemplaire.save(
                            update_fields=[
                                "kilometres_chassis",
                                "date_derniere_intervention",

                                # Rollback
                                "kilometres_rollback",
                                "kilometres_boite_rollback",
                                "kilometres_moteur_rollback",

                                # Valeurs recalculées
                                "kilometres_moteur",
                                "kilometres_boite",
                                "variation_kilometres",
                            ]
                        )

                    # =========================
                    # MAINTENANCE
                    # =========================
                    maintenance = Maintenance(
                        societe=tenant,
                        voiture_exemplaire=exemplaire,
                        immatriculation=exemplaire.immatriculation,
                        date_intervention=timezone.now().date(),

                        kilometres_chassis=(
                            exemplaire.kilometres_chassis
                        ),

                        kilometres_dernier_entretien=(
                            exemplaire.kilometres_dernier_entretien
                        ),

                        type_maintenance=(
                            Maintenance.TypeMaintenance.ENTRETIEN
                        ),

                        tag=Maintenance.Tag.JAUNE,
                    )

                    # =========================
                    # AFFECTATION UTILISATEUR
                    # =========================
                    #
                    # IMPORTANT :
                    # ne pas utiliser systématiquement
                    # Mecanicien.objects.get(id=request.user.id)
                    #
                    # Si tes modèles ont un lien `utilisateur`,
                    # utilise plutôt celui-ci.
                    #

                    # =========================
                    # AFFECTATION DU RÔLE
                    # =========================

                    if role == "mecanicien":
                        maintenance.mecanicien = Mecanicien.objects.filter(
                            pk=request.user.pk
                        ).first()

                    elif role == "chef_mecanicien":
                        maintenance.chef_mecanicien = ChefMecanicien.objects.filter(
                            pk=request.user.pk
                        ).first()

                    elif role == "apprenti":
                        maintenance.apprentis = Apprenti.objects.filter(
                            pk=request.user.pk
                        ).first()

                    elif role == "magasinier":
                        maintenance.magasinier = Magasinier.objects.filter(
                            pk=request.user.pk
                        ).first()

                    elif role == "direction":
                        maintenance.direction = Direction.objects.filter(
                            pk=request.user.pk
                        ).first()

                    maintenance.save()

                    # ==================================================
                    # CRÉATION CHECKUP
                    # ==================================================
                    entretien = form.save(commit=False)

                    entretien.voiture_exemplaire = exemplaire
                    entretien.maintenance = maintenance

                    # kilométrage saisi lors du entretien
                    entretien.kilometrage_entretien = km

                    # kilométrage AVANT le entretien
                    entretien.kilometres_chassis = (
                        ancien_kilometrage
                    )
                    entretien.kilometres_boite = (
                        ancien_kilometrage_boite
                    )
                    entretien.kilometres_moteur = (
                        ancien_kilometrage_moteur
                    )

                    # différence entre ancien et nouveau kilométrage
                    entretien.kilometrage_variation = (
                        kilometrage_variation
                    )

                    # 👨‍🔧 technicien
                    entretien.assign_technicien(
                        request.user
                    )

                    # 👨‍🔧 dernier technicien maintenance
                    entretien.tech_last_maintained_by = (
                        request.user
                    )


                    entretien.maintenance = maintenance

                    entretien.save()
                    # =========================
                    # MANY TO MANY
                    # =========================
                    form.instance = entretien
                    form.save_m2m()

                    # =========================
                    # LOG
                    # =========================


                    ACTION_ENTRETIEN = gettext_noop(
                        "Entretien"
                    )

                    UserLog.objects.create(
                        utilisateur=request.user,
                        action=f"{ACTION_ENTRETIEN} - {exemplaire.immatriculation}"
                    )

                # =========================
                # SUCCÈS
                # =========================
                messages.success(
                    request,
                    _("Entretien enregistré avec succès.")
                )

                return redirect(
                    "entretien:entretien_list",
                    exemplaire_id=exemplaire.id
                )

            except Exception as e:

                # TEMPORAIRE POUR DEBUG
                import traceback
                traceback.print_exc()

                messages.error(
                    request,
                    _("Erreur lors de l'enregistrement : %(erreur)s") % {
                        "erreur": str(e)
                    }
                )

        else:
            messages.error(
                request,
                _("Le formulaire contient des erreurs.")
            )

    # =========================
    # GET
    # =========================
    else:

        entretien = Entretien(
            societe=tenant,
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
        )

        entretien.assign_technicien(request.user)

        form = EntretienForm(
            instance=entretien,
            user=request.user,
            exemplaire=exemplaire,
        )

    # =========================
    # TEMPLATE
    # =========================
    return render(
        request,
        "entretien/entretien_check.html",
        {
            "exemplaire": exemplaire,
            "immatriculation": exemplaire.immatriculation,
            "maintenance": maintenance,
            "form": form,
            "now": timezone.now(),
        }
    )


# ------------
# Vue détail entretien
# -----------------------------
@never_cache
@login_required
def entretien_detail_view(request, entretien_id):
    tenant = request.user.societe

    entretien = get_object_or_404(
        Entretien.objects.select_related("voiture_exemplaire"),
        id=entretien_id
    )

    context = {
        "entretien": entretien,
        "exemplaire": entretien.voiture_exemplaire,
    }
    return render(request, "entretien/entretien_detail.html", context)


#---------------------

# Modifier entretien

#---------------------
@never_cache
@login_required
def modifier_entretien_view(request, entretien_id):

    tenant = request.user.societe

    # =========================
    # RÉCUPÉRATION ENTRETIEN
    # =========================
    entretien = get_object_or_404(
        Entretien.objects.select_related(
            "voiture_exemplaire",
            "maintenance",
            "tech_societe",
            "tech_technicien",
        ),
        id=entretien_id,
    )

    # =========================
    # VÉHICULE
    # =========================
    exemplaire = get_object_or_404(
        VoitureExemplaire.objects.filter(
            Q(client__societe=tenant) |
            Q(client__isnull=True, societe=tenant)
        ),
        id=entretien.voiture_exemplaire_id
    )

    # =========================
    # KILOMÉTRAGE DE RÉFÉRENCE
    # =========================
    # Kilométrage historique avant cet entretien
    km_reference = entretien.kilometres_chassis or 0

    # =========================
    # POST
    # =========================
    if request.method == "POST":

        form = EntretienForm(
            request.POST,
            instance=entretien,
            user=request.user,
            exemplaire=exemplaire,
        )

        if form.is_valid():

            try:

                with transaction.atomic():

                    # ==================================================
                    # NOUVEAU KILOMÉTRAGE SAISI
                    # ==================================================
                    km = form.cleaned_data.get(
                        "kilometrage_entretien"
                    )

                    if km is not None:
                        km = int(km)

                    # ==================================================
                    # VALEURS LOCALES ACTUELLES
                    #
                    # Ces valeurs deviennent le rollback
                    # de CETTE modification.
                    #
                    # On ne reprend PAS les anciens rollback
                    # du controle total ou du checkup piste initial.
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
                    # CHECKUP TRACK
                    # ==================================================
                    entretien = form.save(
                        commit=False
                    )

                    entretien.voiture_exemplaire = (
                        exemplaire
                    )

                    # ==================================================
                    # ROLLBACK LOCAL
                    # ==================================================
                    entretien.kilometres_chassis = (
                        rollback_chassis
                    )

                    entretien.kilometres_moteur = (
                        rollback_moteur
                    )

                    entretien.kilometres_boite = (
                        rollback_boite
                    )

                    # ==================================================
                    # NOUVEAU KILOMÉTRAGE CHECKUP PISTE
                    # ==================================================
                    entretien.kilometrage_entretien = (
                        km
                    )

                    # ==================================================
                    # VARIATION
                    # ==================================================
                    if km is not None:

                        entretien.kilometrage_variation = (
                                km - rollback_chassis
                        )

                    else:

                        entretien.kilometrage_variation = 0

                    # ==================================================
                    # TECHNICIEN
                    # ==================================================
                    entretien.assign_technicien(
                        request.user
                    )

                    entretien.tech_last_maintained_by = (
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

                        # ----------------------------------------------
                        # IMPORTANT
                        #
                        # Le save() du véhicule doit appeler
                        # update_kilometres().
                        #
                        # On ne touche PAS directement à :
                        #
                        # kilometres_moteur
                        # kilometres_boite
                        #
                        # Ils doivent être recalculés.
                        # ----------------------------------------------
                        exemplaire.save()

                    # ==================================================
                    # SAUVEGARDE CHECKUP TRACK
                    # ==================================================
                    entretien.save()

                    form.save_m2m()

                    # ==================================================
                    # MAINTENANCE ASSOCIÉE
                    # ==================================================
                    if entretien.maintenance:

                        maintenance = (
                            entretien.maintenance
                        )

                        if km is not None:
                            maintenance.kilometres_chassis = km

                            maintenance.save(
                                update_fields=[
                                    "kilometres_chassis"
                                ]
                            )

                        # =========================
                        # LOG
                        # =========================


                        ACTION_MODIFICATION_ENTRETIEN = gettext_noop(
                            "Modification de l'entretien"
                        )

                        UserLog.objects.create(
                            utilisateur=request.user,
                            action=f"{ACTION_MODIFICATION_ENTRETIEN} - {exemplaire.immatriculation}"
                        )

                    # =========================
                    # SUCCÈS
                    # =========================
                    messages.success(
                        request,
                        _("Entretien modifié avec succès !")
                    )

                    return redirect(
                        "entretien:entretien_detail",
                        entretien_id=entretien.id
                    )

            except Exception as e:

                import traceback
                traceback.print_exc()

                messages.error(
                    request,
                    _(
                        "Erreur lors de la modification : "
                        "%(erreur)s"
                    ) % {
                        "erreur": str(e)
                    }
                )

        else:

            messages.error(
                request,
                _("Le formulaire contient des erreurs.")
            )

    # =========================
    # GET
    # =========================
    else:

        form = EntretienForm(
            instance=entretien,
            user=request.user,
            exemplaire=exemplaire,
        )

    # =========================
    # TEMPLATE
    # =========================
    return render(
        request,
        "entretien/modifier_entretien.html",
        {
            "form": form,
            "entretien": entretien,
            "exemplaire": exemplaire,
            "km_reference": km_reference,
        }
    )




@never_cache
@login_required
def delete_entretien_view(request, entretien_id):

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
    entretien = get_object_or_404(
        Entretien.objects.select_related(
            "voiture_exemplaire",
            "maintenance",
        ),
        id=entretien_id,
    )

    exemplaire = entretien.voiture_exemplaire
    maintenance = entretien.maintenance

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

                exemplaire.kilometres_chassis = (
                    kilometrage_rollback
                )
                exemplaire.kilometres_boite = (
                    kilometrage_rollback_boite
                )
                exemplaire.kilometres_moteur = (
                    kilometrage_rollback_moteur
                )

                exemplaire.save(
                    update_fields=[
                        "kilometres_chassis",
                        "kilometres_boite",
                        "kilometres_moteur"
                    ]
                )

                # ==================================================
                # SUPPRESSION CHECKUP
                # ==================================================
                entretien.delete()

                # ==================================================
                # SUPPRESSION MAINTENANCE ASSOCIÉE
                # ==================================================
                if maintenance:
                    maintenance.delete()

                # ==================================================
                # USER LOG
                # ==================================================
                ACTION_SUPPRESSION_ENTRETIEN = gettext_noop(
                    "Suppression de l'entretien"
                )

                UserLog.objects.create(
                    utilisateur=request.user,
                    action=(
                        f"{ACTION_SUPPRESSION_ENTRETIEN} - "
                        f"{immatriculation}"
                    )
                )

            messages.success(
                request,
                _("Entretien supprimé avec succès.")
            )

            return redirect(
                "entretien:entretien_list",
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
                "entretien:entretien_detail",
                 entretien_id=entretien.id,
            )

    # ==================================================
    # GET → CONFIRMATION
    # ==================================================
    return render(
        request,
        "entretien/delete_entretien.html",
        {
            "entretien": entretien,
            "exemplaire": exemplaire,
        }
    )







@login_required
def entretien_pdf_view(request, entretien_id):
    tenant = request.user.societe

    entretien = get_object_or_404(
        Entretien.objects.select_related(
            "voiture_exemplaire",
            "tech_technicien",
            "tech_societe",
            "main_oeuvre",
            "piece",
        ),
        id=entretien_id
    )

    rapport = entretien.generer_rapport_remplacement()

    html_string = render_to_string(
        "entretien/entretien_detail_pdf.html",
        {
            "entretien": entretien,
            "objet": entretien,
            "rapport": rapport,
            "pieces_utilisees": rapport.get("lignes", []),
            "total_pieces": rapport.get("total_general", 0),
            "date_export": timezone.now(),
            "societe": tenant,
        },
        request=request,
    )

    pdf = HTML(
        string=html_string,
        base_url=request.build_absolute_uri("/")
    ).write_pdf()

    # =========================================================
    # IMMATRICULATION
    # =========================================================

    immatriculation = (
        entretien.voiture_exemplaire.immatriculation
        if entretien.voiture_exemplaire
        else "sans_immatriculation"
    )

    # =========================================================
    # TECHNICIEN
    # =========================================================

    technicien = (
        entretien.tech_nom_technicien
        or "technicien_inconnu"
    )

    # Nettoyage pour le nom du fichier
    technicien = str(technicien).replace(" ", "_")
    immatriculation = str(immatriculation).replace(" ", "_")

    # =========================================================
    # DATE
    # =========================================================

    date_pdf = (
        entretien.date.strftime("%Y-%m-%d")
        if entretien.date
        else timezone.now().strftime("%Y-%m-%d")
    )

    # =========================================================
    # TITRE / NOM DU PDF
    # =========================================================

    nom_fichier = (
        f"Entretien_{technicien}_{immatriculation}_{date_pdf}.pdf"
    )

    response = HttpResponse(
        pdf,
        content_type="application/pdf",
    )

    response["Content-Disposition"] = (
        f'inline; filename="{nom_fichier}"'
    )

    return response