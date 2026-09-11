from django.core.exceptions import ValidationError

from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib import messages
from django.db import models, transaction
from django.db.models import Q
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django_tenants.utils import  schema_context
from maintenance.autres_interventions.echappement.forms import ControleEchappementForm
from maintenance.autres_interventions.echappement.models import Echappement
from maintenance.models import Maintenance
from maintenance.types_maintenances import TYPES_MAINTENANCE
from utilisateurs.models import UserLog
from voiture.voiture_exemplaire.models import VoitureExemplaire
from voiture.voiture_modele.models import VoitureModele
from django.utils.translation import gettext_lazy as _, gettext_noop
from weasyprint import HTML






@never_cache
@login_required
def dashboard_echappement_view(request, exemplaire_id):
    tenant = request.user.societe

    user = request.user
    context = {}

    # 🔹 Récupérer l'exemplaire AVANT
    exemplaire = get_object_or_404(VoitureExemplaire, id=exemplaire_id)

    # --- Sécurité tenant ---
    tenant_schema = getattr(request, 'tenant', None)
    schema_name = tenant_schema.schema_name if tenant_schema else None


    total_echappement = 0

    echappement = []



    if schema_name:
        with schema_context(schema_name):

            # ✅ FILTRAGE PAR EXEMPLAIRE

            echappement = Echappement.objects.filter(voiture_exemplaire=exemplaire)



            # ✅ COUNTS CORRECTS
            total_echappement = echappement.count()


            modeles = VoitureModele.objects.all()
    else:
        modeles = []

    # --- POST ---
    if request.method == "POST":
        type_choisi = request.POST.get("type_maintenance")
        date_intervention = request.POST.get("date_intervention")
        description = request.POST.get("description", "")

        if type_choisi and date_intervention:
            Maintenance.objects.create(
                societe=tenant,
                voiture_exemplaire=exemplaire,
                type_maintenance=type_choisi,
                immatriculation=exemplaire.immatriculation,
                date_intervention=date_intervention,
                description=description
            )
            return redirect(
                'echappement:dashboard_echappement',
                exemplaire_id=exemplaire.id
            )

    # --- CONTEXT ---
    context.update({
        "exemplaire": exemplaire,
        "types_maintenance": TYPES_MAINTENANCE,


        "total_echappement": total_echappement,


        "echappement": echappement,


        "modeles": modeles,

    })

    return render(request, "echappement/dashboard_echappement.html", context)



# -----------------------------
# Classe ListView pour Echappement
# -----------------------------
@method_decorator([login_required, never_cache], name='dispatch')
class EchappementListView(ListView):
    model = Echappement   # ✅ ICI
    template_name = "echappement/echappement_list.html"
    context_object_name = "echappements"
    ordering = ["-id"]

    def get_queryset(self):
        queryset = Echappement.objects.select_related(
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
def echappement_check_view(request, exemplaire_id):

    tenant = request.user.societe
    role = request.user.role

    maintenance = None

    # =========================================================
    # RÉCUPÉRATION DU VÉHICULE
    # =========================================================

    exemplaire = get_object_or_404(
        VoitureExemplaire.objects.filter(
            Q(client__societe=tenant)
            | Q(client__isnull=True, societe=tenant)
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

        # Instance liée au véhicule avant validation du formulaire
        instance_echappement = Echappement(
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

        instance_echappement.assign_technicien(
            request.user
        )

        form = ControleEchappementForm(
            request.POST,
            instance=instance_echappement,
            user=request.user,
            exemplaire=exemplaire,
        )

        # =====================================================
        # FORMULAIRE VALIDE
        # =====================================================

        if form.is_valid():

            try:

                # =====================================================
                # KILOMÉTRAGE
                # =====================================================
                # ✅ On conserve le kilométrage précédent
                ancien_kilometrage = (
                        exemplaire.kilometres_chassis or 0
                )
                ancien_kilometrage_boite = (
                        exemplaire.kilometres_boite or 0
                )

                ancien_kilometrage_moteur = (
                        exemplaire.kilometres_moteur or 0
                )

                km = form.cleaned_data.get(
                    "kilometrage_echappement"
                )



                # -----------------------------------------------------
                # Kilométrage obligatoire
                # -----------------------------------------------------

                if km is None:

                    form.add_error(
                        "kilometrage_echappement",
                        _(
                            "Le kilométrage est obligatoire."
                        ),
                    )

                else:

                    km = int(km)

                    # -------------------------------------------------
                    # Vérification du kilométrage
                    # -------------------------------------------------

                    if km < ancien_kilometrage:

                        form.add_error(
                            "kilometrage_echappement",
                            _(
                                "Le kilométrage du contrôle de "
                                "l'échappement ne peut pas être "
                                "inférieur au kilométrage actuel "
                                "du véhicule."
                            ),
                        )

                    else:

                        kilometrage_variation = (
                                km - ancien_kilometrage
                        )


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

                        # =================================================
                        # TRANSACTION
                        # =================================================

                        with transaction.atomic():

                            # =============================================
                            # CRÉATION MAINTENANCE
                            # =============================================

                            maintenance = (
                                Maintenance.objects.create(
                                    societe=tenant,
                                    voiture_exemplaire=(
                                        exemplaire
                                    ),
                                    immatriculation=(
                                        exemplaire.immatriculation
                                    ),
                                    date_intervention=(
                                        timezone.localdate()
                                    ),
                                    kilometres_chassis=km,
                                    kilometres_dernier_entretien=(
                                        exemplaire
                                        .kilometres_dernier_entretien
                                    ),
                                    type_maintenance=(
                                        Maintenance
                                        .TypeMaintenance
                                        .ECHAPPEMENT
                                    ),
                                    tag=(
                                        Maintenance.Tag.JAUNE
                                    ),
                                )
                            )

                            # =============================================
                            # ATTRIBUTION DU PERSONNEL
                            # =============================================

                            if role == "mecanicien":

                                maintenance.mecanicien = (
                                    request.user
                                )

                            elif role == "chef_mecanicien":

                                maintenance.chef_mecanicien = (
                                    request.user
                                )

                            elif role == "magasinier":

                                maintenance.magasinier = (
                                    request.user
                                )

                            elif role == "direction":

                                maintenance.direction = (
                                    request.user
                                )

                            maintenance.save()

                            # ---------------------------------------------
                            # APPRENTI
                            # ---------------------------------------------

                            if role == "apprenti":
                                maintenance.apprentis.add(
                                    request.user
                                )

                            # =============================================
                            # CRÉATION DU CONTRÔLE ÉCHAPPEMENT
                            # =============================================

                            echappement = form.save(
                                commit=False
                            )

                            echappement.voiture_exemplaire = (
                                exemplaire
                            )

                            echappement.maintenance = (
                                maintenance
                            )

                            # ---------------------------------------------
                            # Kilométrage AVANT intervention
                            # ---------------------------------------------

                            echappement.kilometres_chassis = (
                                ancien_kilometrage
                            )

                            # ---------------------------------------------
                            # Kilométrage du contrôle échappement
                            # ---------------------------------------------

                            echappement.kilometrage_echappement = (
                                km
                            )

                            # ---------------------------------------------
                            # Variation kilométrique
                            # ---------------------------------------------

                            echappement.kilometrage_variation = (
                                kilometrage_variation
                            )


                            echappement.assign_technicien(
                                request.user
                            )

                            echappement.tech_last_maintained_by = (
                                request.user
                            )

                            echappement.kilometres_boite = (
                                ancien_kilometrage_boite
                            )
                            echappement.kilometres_moteur = (
                                ancien_kilometrage_moteur
                            )

                            # différence entre ancien et nouveau kilométrage
                            echappement.kilometrage_variation = (
                                kilometrage_variation
                            )

                            # 👨‍🔧 technicien
                            echappement.assign_technicien(request.user)

                            # 👨‍🔧 dernier technicien maintenance
                            echappement.tech_last_maintained_by = request.user

                            echappement.save()
                            form.save_m2m()


                            # =============================================
                            # LOG
                            # =============================================

                            ACTION_CONTROLE_ECHAPPEMENT = (
                                gettext_noop(
                                    "Contrôle de l'échappement"
                                )
                            )

                            UserLog.objects.create(
                                utilisateur=request.user,
                                action=(
                                    f"{ACTION_CONTROLE_ECHAPPEMENT} - "
                                    f"{exemplaire.immatriculation}"
                                ),
                            )

                        # =================================================
                        # SUCCÈS
                        # =================================================

                        messages.success(
                            request,
                            _(
                                "Le contrôle de l'échappement "
                                "a été enregistré avec succès."
                            ),
                        )

                        return redirect(
                            "echappement:echappement_list",
                            exemplaire_id=(
                                exemplaire.id
                            ),
                        )

            except Exception as e:

                messages.error(
                    request,
                    _(
                        "Erreur lors de l'enregistrement : "
                        "%(erreur)s"
                    )
                    % {
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
                    "Le formulaire contient des erreurs."
                ),
            )

    # =========================================================
    # GET
    # =========================================================

    else:

        instance_echappement = Echappement(
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

        instance_echappement.assign_technicien(
            request.user
        )

        form = ControleEchappementForm(
            instance=instance_echappement,
            user=request.user,
            exemplaire=exemplaire,
        )

    # =========================================================
    # AFFICHAGE
    # =========================================================

    return render(
        request,
        "echappement/echappement_check.html",
        {
            "exemplaire": exemplaire,
            "immatriculation": exemplaire.immatriculation,
            "maintenance": maintenance,
            "form": form,
            "now": timezone.now(),
        },
    )


# ------------
# Vue détail echappement
# -----------------------------
@login_required
def echappement_detail_view(request,echappement_id):
   echappement = get_object_or_404(
        Echappement.objects.select_related("voiture_exemplaire"),
        id=echappement_id
    )

   context = {
        "echappement":echappement,
        "exemplaire":echappement.voiture_exemplaire,
    }
   return render(request, "echappement/echappement_detail.html", context)



@login_required
def modifier_echappement_view(request, echappement_id):
    tenant = request.user.societe

    # Récupération du contrôle échappement avec son exemplaire
    echappement = get_object_or_404(
        Echappement.objects.select_related("voiture_exemplaire"),
        id=echappement_id,
    )

    exemplaire = echappement.voiture_exemplaire

    # -------------------------
    # POST
    # -------------------------
    if request.method == "POST":

        form = ControleEchappementForm(
            request.POST,
            instance=echappement,
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
                        "kilometrage_echappement"
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
                    echappement = form.save(
                        commit=False
                    )

                    echappement.voiture_exemplaire = (
                        exemplaire
                    )

                    # ==================================================
                    # ROLLBACK LOCAL
                    # ==================================================
                    echappement.kilometres_chassis = (
                        rollback_chassis
                    )

                    echappement.kilometres_moteur = (
                        rollback_moteur
                    )

                    echappement.kilometres_boite = (
                        rollback_boite
                    )

                    # ==================================================
                    # NOUVEAU KILOMÉTRAGE
                    # ==================================================
                    echappement.kilometrage_echappement = km

                    # ==================================================
                    # VARIATION
                    # ==================================================
                    if km is not None:
                        echappement.kilometrage_variation = (
                            km - rollback_chassis
                        )
                    else:
                        echappement.kilometrage_variation = 0

                    # ==================================================
                    # TECHNICIEN
                    # ==================================================
                    echappement.assign_technicien(
                        request.user
                    )

                    echappement.tech_last_maintained_by = (
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
                    echappement.save()

                    form.save_m2m()

                # ==================================================
                # USER LOG
                # ==================================================
                ACTION_MODIFICATION_CONTROLE_ECHAPPEMENT = gettext_noop(
                    "Modification contrôle de l'échappement"
                )

                UserLog.objects.create(
                    utilisateur=request.user,
                    action=(
                        f"{ACTION_MODIFICATION_CONTROLE_ECHAPPEMENT} - "
                        f"{exemplaire.immatriculation}"
                    )
                )

                # ==================================================
                # SUCCÈS
                # ==================================================
                messages.success(
                    request,
                    _(
                        "Checkup de l'échappement "
                        "modifié avec succès !"
                    ),
                )

                return redirect(
                    "echappement:echappement_detail",
                    echappement_id=echappement.id,
                )

            except ValidationError as e:

                form.add_error(
                    "kilometrage_echappement",
                    e
                )

                messages.error(
                    request,
                    _("Kilométrage invalide.")
                )

            except Exception as e:

                messages.error(
                    request,
                    _(
                        "Erreur lors de la modification : "
                        "%(error)s"
                    ) % {
                        "error": str(e)
                    }
                )

        else:

            messages.error(
                request,
                _("Le formulaire contient des erreurs.")
            )

    # -------------------------
    # GET
    # -------------------------
    else:

        form = ControleEchappementForm(
            instance=echappement,
            user=request.user,
            exemplaire=exemplaire,
        )

    # -------------------------
    # RENDER
    # -------------------------
    return render(
        request,
        "echappement/modifier_echappement.html",
        {
            "form": form,
            "echappement": echappement,
            "exemplaire": exemplaire,
        },
    )



@never_cache
@login_required
def delete_echappement_view(request, echappement_id):

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
    echappement = get_object_or_404(
        Echappement.objects.select_related(
            "voiture_exemplaire",
            "maintenance",
        ),
        id=echappement_id,
    )

    exemplaire = echappement.voiture_exemplaire
    maintenance = echappement.maintenance

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
                echappement.delete()

                # ==================================================
                # SUPPRESSION MAINTENANCE ASSOCIÉE
                # ==================================================
                if maintenance:
                    maintenance.delete()

                # ==================================================
                # USER LOG
                # ==================================================
                ACTION_SUPPRESSION_ECHAPPEMENT = gettext_noop(
                    "Suppression du contrôle de l'échappement"
                )

                UserLog.objects.create(
                    utilisateur=request.user,
                    action=(
                        f"{ACTION_SUPPRESSION_ECHAPPEMENT} - "
                        f"{immatriculation}"
                    )
                )

            messages.success(
                request,
                _("Contrôle de l'échappement supprimé avec succès.")
            )

            return redirect(
                "echappement:echappement_list",
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
                "echappement:echappement_detail",
                 echappement_id=echappement.id,
            )

    # ==================================================
    # GET → CONFIRMATION
    # ==================================================
    return render(
        request,
        "echappement/delete_echappement.html",
        {
            "echappement": echappement,
            "exemplaire": exemplaire,
        }
    )








@login_required
def echappement_check_pdf_view(request, pk):
    echappement = get_object_or_404(
        Echappement.objects.select_related(
            "voiture_exemplaire",
            "tech_technicien",
            "tech_societe",
            "societe",
            "main_oeuvre",
        ),
        pk=pk,
    )

    rapport = echappement.generer_rapport_remplacement()

    html_string = render_to_string(
        "echappement/echappement_check_pdf.html",
        {
            "echappement": echappement,
            "rapport": rapport,
            "date_export": timezone.now(),
            "societe": request.user.societe,
        },
        request=request,
    )

    pdf = HTML(
        string=html_string,
        base_url=request.build_absolute_uri("/"),
    ).write_pdf()

    voiture = echappement.voiture_exemplaire

    # Immatriculation
    if voiture and voiture.immatriculation:
        immatriculation = voiture.immatriculation
    elif getattr(echappement, "immatriculation", None):
        immatriculation = echappement.immatriculation
    else:
        immatriculation = "sans_immatriculation"

    # Technicien
    if echappement.tech_technicien:
        technicien = str(echappement.tech_technicien)
    elif getattr(echappement, "tech_nom_technicien", None):
        technicien = echappement.tech_nom_technicien
    else:
        technicien = "technicien_inconnu"

        # =========================================================
        # IMMATRICULATION
        # =========================================================

    immatriculation = (
        echappement.voiture_exemplaire.immatriculation
        if echappement.voiture_exemplaire
        else "sans_immatriculation"
    )

    # =========================================================
    # TECHNICIEN
    # =========================================================

    technicien = (
            echappement.tech_nom_technicien
            or "technicien_inconnu"
    )

    # Nettoyage pour le nom du fichier
    technicien = str(technicien).replace(" ", "_")
    immatriculation = str(immatriculation).replace(" ", "_")

    # =========================================================
    # DATE
    # =========================================================

    date_pdf = (
        echappement.date.strftime("%Y-%m-%d")
        if echappement.date
        else timezone.now().strftime("%Y-%m-%d")
    )

    # =========================================================
    # TITRE / NOM DU PDF
    # =========================================================

    nom_fichier = (
        f"{_('Echappement')}_{technicien}_{immatriculation}_{date_pdf}.pdf"
    )

    response = HttpResponse(
        pdf,
        content_type="application/pdf",
    )

    response["Content-Disposition"] = (
        f'inline; filename="{nom_fichier}"'
    )

    return response