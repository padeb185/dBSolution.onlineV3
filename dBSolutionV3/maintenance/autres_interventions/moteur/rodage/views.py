from django.core.exceptions import ValidationError

from django.shortcuts import redirect, render
from django.contrib import messages
from django.db import transaction, models
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import ListView
from maindoeuvre.models import MainDoeuvre
from maintenance.autres_interventions.moteur.rodage.forms import RodageForm
from maintenance.autres_interventions.moteur.rodage.models import Rodage
from maintenance.models import Maintenance
from utilisateurs.models import UserLog
from voiture.voiture_exemplaire.models import VoitureExemplaire
from django.db.models import Q
from django.utils.translation import gettext_lazy as _, gettext_noop
from utilisateurs.apprentis.models import Apprenti
from utilisateurs.chef_mecanicien.models import ChefMecanicien
from utilisateurs.direction.models import Direction
from utilisateurs.magasinier.models import Magasinier
from utilisateurs.mecanicien.models import Mecanicien
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils import timezone
from weasyprint import HTML




# -----------------------------
# Classe ListView pour entretien
# -----------------------------
@method_decorator([login_required, never_cache], name='dispatch')
class RodageListView(ListView):
    model = Rodage
    template_name = "rodage/rodage_list.html"
    context_object_name = "rodages"
    ordering = ["-id"]

    def get_queryset(self):
        queryset = Rodage.objects.select_related(
            "voiture_exemplaire", "maintenance", "tech_societe"
        )

        # Filtrer par société : inclure les objets NULL ou ceux de la société de l'utilisateur
        societe = getattr(self.request.user, "societe", None)
        if societe:
            queryset = queryset.filter(
                models.Q(tech_societe=societe) | models.Q(tech_societe__isnull=True)
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
def rodage_check_view(request, exemplaire_id):

    tenant = request.user.societe
    role = request.user.role

    # 🔎 Récupération exemplaire
    exemplaire = get_object_or_404(
        VoitureExemplaire.objects.filter(
            Q(client__societe=tenant) |
            Q(client__isnull=True, societe=tenant)
        ),
        id=exemplaire_id
    )

    # 🔐 Vérification rôles
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

    maintenance = None

    if request.method == "POST":

        form = RodageForm(
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

                km = form.cleaned_data.get("kilometres_rodage")

                if km is None:
                    form.add_error(
                        "kilometres_rodage",
                        _("Le kilométrage est obligatoire."),
                    )

                else:
                    km = int(km)

                    if km < ancien_kilometrage:
                        form.add_error(
                            "kilometres_rodage",
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

                                    # Valeurs recalculées
                                    "kilometres_moteur",
                                    "kilometres_boite",
                                    "variation_kilometres",
                                ]
                            )


                            # 🔴 Création maintenance UNIQUE
                            maintenance = Maintenance.objects.create(
                                societe=request.user.societe,
                                voiture_exemplaire=exemplaire,
                                immatriculation=exemplaire.immatriculation,
                                date_intervention=timezone.now().date(),
                                kilometres_chassis=exemplaire.kilometres_chassis,
                                kilometres_dernier_entretien=exemplaire.kilometres_dernier_entretien,
                                type_maintenance=Maintenance.TypeMaintenance.RODAGE,
                                tag=Maintenance.Tag.JAUNE,
                            )

                            # 🔧 Affectation rôle
                            if role == "mecanicien":
                                maintenance.mecanicien = Mecanicien.objects.get(id=request.user.id)

                            elif role == "chef_mecanicien":
                                maintenance.chef_mecanicien = ChefMecanicien.objects.get(id=request.user.id)

                            elif role == "apprenti":
                                maintenance.apprentis = Apprenti.objects.get(id=request.user.id)

                            elif role == "magasinier":
                                maintenance.magasinier = Magasinier.objects.get(id=request.user.id)

                            elif role == 'direction':
                                maintenance.direction = Direction.objects.get(id=request.user.id)

                            maintenance.save()

                            # M2M : après sauvegarde de Maintenance
                            if role == "apprenti":
                                maintenance.apprentis.add(request.user)

                            rodage = form.save(commit=False)

                            rodage.voiture_exemplaire = (
                                exemplaire
                            )

                            rodage.maintenance = (
                                maintenance
                            )

                            # ---------------------------------------------
                            # Kilométrage AVANT intervention
                            # ---------------------------------------------
                            rodage.kilometres_chassis = (
                                ancien_kilometrage
                            )

                            rodage.kilometres_boite = (
                                ancien_kilometrage_boite
                            )

                            rodage.kilometres_moteur = (
                                ancien_kilometrage_moteur
                            )

                            # ---------------------------------------------
                            # Kilométrage rodage
                            # ---------------------------------------------
                            rodage.kilometrage_alte = km

                            # ---------------------------------------------
                            # Variation kilométrique
                            # ---------------------------------------------
                            rodage.kilometrage_variation = (
                                kilometrage_variation
                            )

                            # =============================================
                            # TECHNICIEN
                            # =============================================
                            rodage.assign_technicien(
                                request.user
                            )

                            rodage.tech_last_maintained_by = (
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
                            if rodage.main_oeuvre_id:

                                main_oeuvre = (
                                    rodage.main_oeuvre
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

                                rodage.main_oeuvre = (
                                    main_oeuvre
                                )

                            # ==================================================
                            # SAUVEGARDE rodage
                            # IMPORTANT :
                            # EN DEHORS DU IF/ELSE MAIN-D'ŒUVRE
                            # ==================================================
                            rodage.save()

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



                            ACTION_RODAGE = gettext_noop(
                                "Rodage"
                            )

                            UserLog.objects.create(
                                utilisateur=request.user,
                                action=f"{ACTION_RODAGE} - {exemplaire.immatriculation}"
                            )

                    messages.success(request, _("Rodage enregistré avec succès."))
                    return redirect("rodage:rodage_list", exemplaire_id=exemplaire.id)

            except Exception as e:
                messages.error(request, _(f"Erreur lors de l'enregistrement : {str(e)}"))
        else:
            messages.error(request, _("Le formulaire contient des erreurs."))



    else:
        rodage = Rodage(
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

        rodage.assign_technicien(request.user)

        form = RodageForm(
            instance=rodage,
            user=request.user,
            exemplaire=exemplaire

        )


    return render(request, 'rodage/rodage_check.html', {
        "exemplaire": exemplaire,
        "immatriculation": exemplaire.immatriculation,
        "maintenance": maintenance,
        "form": form,
        "now": timezone.now(),
    })



# ------------
# Vue détail entretien
# -----------------------------
@never_cache
@login_required
def rodage_detail_view(request, rodage_id):
    tenant = request.user.societe

    rodage = get_object_or_404(
        Rodage.objects.select_related("voiture_exemplaire"),
        id=rodage_id
    )

    context = {
        "rodage": rodage,
        "exemplaire": rodage.voiture_exemplaire,
    }
    return render(request, "rodage/rodage_detail.html", context)


#---------------------

# Modifier rodage

#---------------------

@login_required
def modifier_rodage_view(request, rodage_id):
    tenant = request.user.societe

    # Récupération de l'entretien avec son exemplaire
    rodage = get_object_or_404(
        Rodage.objects.select_related("voiture_exemplaire"),
        id=rodage_id
    )

    exemplaire = rodage.voiture_exemplaire

    # -------------------------
    # POST
    # -------------------------
    if request.method == "POST":
        form = RodageForm(
            request.POST,
            instance=rodage,
            user=request.user,
            exemplaire=rodage.voiture_exemplaire
        )
        if form.is_valid():

            try:
                with transaction.atomic():

                    # ==================================================
                    # NOUVEAU KILOMÉTRAGE SAISI
                    # ==================================================
                    km = form.cleaned_data.get(
                        "kilometres_rodage"
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
                    rodage = form.save(
                        commit=False
                    )

                    rodage.voiture_exemplaire = (
                        exemplaire
                    )

                    # ==================================================
                    # ROLLBACK LOCAL
                    # ==================================================
                    rodage.kilometres_chassis = (
                        rollback_chassis
                    )

                    rodage.kilometres_moteur = (
                        rollback_moteur
                    )

                    rodage.kilometres_boite = (
                        rollback_boite
                    )

                    # ==================================================
                    # NOUVEAU KILOMÉTRAGE
                    # ==================================================
                    rodage.kilometrage_alte = km

                    # ==================================================
                    # VARIATION
                    # ==================================================
                    if km is not None:
                        rodage.kilometrage_variation = (
                                km - rollback_chassis
                        )
                    else:
                        rodage.kilometrage_variation = 0

                    # ==================================================
                    # TECHNICIEN
                    # ==================================================
                    rodage.assign_technicien(
                        request.user
                    )

                    rodage.tech_last_maintained_by = (
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
                    rodage.save()

                    form.save_m2m()


                    ACTION_MODIFICATION_RODAGE = gettext_noop(
                        "Modification du rodage"
                    )

                    UserLog.objects.create(
                        utilisateur=request.user,
                        action=f"{ACTION_MODIFICATION_RODAGE} - {exemplaire.immatriculation}"
                    )

                    messages.success(request, _("Rodage modifié avec succès !"))
                    return redirect("rodage:rodage_detail", rodage_id=rodage.id)

            except ValidationError as e:
                form.add_error(None, e)
                messages.error(request, _("Kilométrage invalide"))

        else:
            messages.error(request, _("Le formulaire contient des erreurs."))


    # -------------------------
    # GET
    # -------------------------
    else:
        form = RodageForm(
            instance=rodage,
            user=request.user,
            exemplaire=rodage.voiture_exemplaire
        )

    return render(
        request,
        "rodage/modifier_rodage.html",
        {
            "form": form,
            "rodage": rodage,
            "exemplaire": rodage.voiture_exemplaire,
        }
    )






@never_cache
@login_required
def delete_rodage_view(request, rodage_id):

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
    rodage = get_object_or_404(
        Rodage.objects.select_related(
            "voiture_exemplaire",
            "maintenance",
        ),
        id=rodage_id,
    )

    exemplaire = rodage.voiture_exemplaire
    maintenance = rodage.maintenance

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
                rodage.delete()

                # ==================================================
                # SUPPRESSION MAINTENANCE ASSOCIÉE
                # ==================================================
                if maintenance:
                    maintenance.delete()

                # ==================================================
                # USER LOG
                # ==================================================
                ACTION_SUPPRESSION_RODAGE = gettext_noop(
                    "Suppression du contrôle du rodage"
                )

                UserLog.objects.create(
                    utilisateur=request.user,
                    action=(
                        f"{ACTION_SUPPRESSION_RODAGE} - "
                        f"{immatriculation}"
                    )
                )

            messages.success(
                request,
                _("Contrôle du rodage supprimé avec succès.")
            )

            return redirect(
                "rodage:rodage_list",
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
                "rodage:rodage_detail",
                 rodage_id=rodage.id,
            )

    # ==================================================
    # GET → CONFIRMATION
    # ==================================================
    return render(
        request,
        "rodage/delete_rodage.html",
        {
            "rodage": rodage,
            "exemplaire": exemplaire,
        }
    )








@login_required
def rodage_pdf_view(request, rodage_id):
    tenant = request.user.societe

    rodage = get_object_or_404(
        Rodage.objects.select_related(
            "voiture_exemplaire",
            "tech_technicien",
            "tech_societe",
            "main_oeuvre",
            "piece",
        ),
        id=rodage_id,
    )

    rapport = rodage.generer_rapport_remplacement() or {}
    rapport.setdefault("lignes", [])

    # Total des pièces uniquement
    total_pieces = Decimal(str(
        rapport.get("total_general") or 0
    ))

    # Total de la main-d'œuvre
    if rodage.main_oeuvre:
        cout_main_oeuvre = Decimal(str(
            rodage.main_oeuvre.cout_total or 0
        ))
    else:
        cout_main_oeuvre = Decimal("0.00")

    # Total pièces + main-d'œuvre
    total_general_avec_main_oeuvre = (
            total_pieces + cout_main_oeuvre
    )

    rapport.update({
        "total_pieces": total_pieces,
        "cout_main_oeuvre": cout_main_oeuvre,
        "total_general_avec_main_oeuvre": (
            total_general_avec_main_oeuvre
        ),
    })

    html_string = render_to_string(
        "rodage/rodage_pdf.html",
        {
            "rodage": rodage,
            "rapport": rapport,
            "date_export": timezone.now(),
            "societe": request.user.societe,
        }
    )

    pdf = HTML(
        string=html_string,
        base_url=request.build_absolute_uri("/")
    ).write_pdf()

    # =========================================================
    # IMMATRICULATION
    # =========================================================

    immatriculation = (
        rodage.voiture_exemplaire.immatriculation
        if rodage.voiture_exemplaire
        else "sans_immatriculation"
    )

    # =========================================================
    # TECHNICIEN
    # =========================================================

    technicien = (
            rodage.tech_nom_technicien
            or "technicien_inconnu"
    )

    # Nettoyage pour le nom du fichier
    technicien = str(technicien).replace(" ", "_")
    immatriculation = str(immatriculation).replace(" ", "_")

    # =========================================================
    # DATE
    # =========================================================

    date_pdf = (
        rodage.date.strftime("%Y-%m-%d")
        if rodage.date
        else timezone.now().strftime("%Y-%m-%d")
    )

    # =========================================================
    # TITRE / NOM DU PDF
    # =========================================================

    nom_fichier = (
        f"{_('Rodage')}_{technicien}_{immatriculation}_{date_pdf}.pdf"
    )

    response = HttpResponse(
        pdf,
        content_type="application/pdf",
    )

    response["Content-Disposition"] = (
        f'inline; filename="{nom_fichier}"'
    )

    return response
