from django.shortcuts import render

# Create your views here.
from django.core.exceptions import ValidationError

from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils import timezone
from django.contrib import messages
from django.db import transaction, models
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import ListView
from maintenance.eclairage.forms import EclairageForm
from maintenance.eclairage.models import Eclairage
from maintenance.models import Maintenance
from utilisateurs.models import UserLog
from voiture.voiture_exemplaire.models import VoitureExemplaire
from django.db.models import Q
from django.utils.translation import gettext_lazy as _, gettext_noop
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from utils.securite import q_intervention_tenant






# -----------------------------
# Classe ListView pour eclairage
# -----------------------------
@method_decorator([login_required, never_cache], name="dispatch")
class EclairageListView(ListView):
    model = Eclairage
    template_name = "eclairage/eclairage_list.html"
    context_object_name = "eclairages"
    ordering = ["-id"]

    def get_queryset(self):
        queryset = Eclairage.objects.select_related(
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
            "apprenti",
        ]

        return context






#----------------------------
# creation eclairage
#----------------------------

@never_cache
@login_required
def eclairage_check_view(request, exemplaire_id):

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

        form = EclairageForm(
            request.POST,
            user=request.user,
            exemplaire=exemplaire,
        )

        if form.is_valid():

            km = form.cleaned_data.get("kilometrage_eclairage")

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
            ancien_kilometrage_embrayage = (
                    exemplaire.kilometres_embrayage or 0
            )

            ancien_kilometrage_dernier_entretien = (
                    exemplaire.kilometres_dernier_entretien or 0
            )

            # =========================
            # VALIDATION KM
            # =========================
            if km is not None:

                km = int(km)

                if km < ancien_kilometrage:

                    form.add_error(
                        "kilometrage_eclairage",
                        _("Le kilométrage ne peut pas diminuer.")
                    )

                    messages.error(
                        request,
                        _("Le kilométrage ne peut pas diminuer.")
                    )

                    return render(
                        request,
                        "eclairage/eclairage_check.html",
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
                    # eclairage
                    # =========================
                    eclairage = form.save(commit=False)

                    eclairage.societe = tenant
                    eclairage.voiture_exemplaire = exemplaire

                    eclairage.kilometres_chassis = (
                        ancien_kilometrage
                    )



                    eclairage.kilometrage_eclairage = km

                    eclairage.kilometrage_variation = (
                        kilometrage_variation
                    )

                    eclairage.assign_technicien(request.user)

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

                        exemplaire.kilometres_embrayage_rollback = (
                            ancien_kilometrage_embrayage
                        )

                        exemplaire.kilometres_entretien_rollback = (
                            ancien_kilometrage_dernier_entretien
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

                        exemplaire.kilometres_dernier_entretien = km

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
                                "kilometres_embrayage",
                                "kilometres_embrayage_rollback",
                                "kilometres_dernier_entretien",
                                "kilometres_entretien_rollback",


                                # Valeurs recalculées
                                "kilometres_moteur",
                                "kilometres_boite",
                                "variation_kilometres",
                            ]
                        )

                    # =========================
                    # MAINTENANCE
                    # =========================
                    # 🔴 maintenance unique
                    maintenance = Maintenance.objects.create(
                        societe=request.user.societe,
                        voiture_exemplaire=exemplaire,
                        immatriculation=exemplaire.immatriculation,
                        date_intervention=timezone.now().date(),
                        kilometres_chassis=exemplaire.kilometres_chassis,
                        kilometres_dernier_entretien=exemplaire.kilometres_dernier_entretien,
                        type_maintenance=Maintenance.TypeMaintenance.ECLAIRAGE,
                        tag=Maintenance.Tag.JAUNE,

                        # 👨‍🔧 utilisateur ayant réalisé la maintenance
                        tech_technicien=request.user,
                        tech_societe=request.user.societe,
                        tech_nom_technicien=f"{request.user.prenom} {request.user.nom}",
                        tech_role_technicien=request.user.role,
                    )

                    # 🔧 Affectation spécifique selon le rôle
                    if role == "mecanicien":
                        maintenance.mecanicien = request.user

                    elif role == "chef_mecanicien":
                        maintenance.chef_mecanicien = request.user

                    elif role == "apprenti":
                        maintenance.apprentis = request.user

                    maintenance.save()

                    # ==================================================
                    # CRÉATION CHECKUP
                    # ==================================================
                    eclairage = form.save(commit=False)

                    eclairage.voiture_exemplaire = exemplaire
                    eclairage.maintenance = maintenance

                    # kilométrage saisi lors du eclairage
                    eclairage.kilometrage_eclairage = km

                    # kilométrage AVANT le eclairage
                    eclairage.kilometres_chassis = (
                        ancien_kilometrage
                    )
                    eclairage.kilometres_boite = (
                        ancien_kilometrage_boite
                    )
                    eclairage.kilometres_moteur = (
                        ancien_kilometrage_moteur
                    )
                    eclairage.kilometres_embrayage = (
                        ancien_kilometrage_embrayage
                    )

                    eclairage.kilometres_dernier_entretien = (
                        ancien_kilometrage_dernier_entretien
                    )

                    # différence entre ancien et nouveau kilométrage
                    eclairage.kilometrage_variation = (
                        kilometrage_variation
                    )

                    # 👨‍🔧 technicien
                    eclairage.assign_technicien(
                        request.user
                    )

                    # 👨‍🔧 dernier technicien maintenance
                    eclairage.tech_last_maintained_by = (
                        request.user
                    )


                    eclairage.maintenance = maintenance

                    eclairage.save()
                    # =========================
                    # MANY TO MANY
                    # =========================
                    form.instance = eclairage
                    form.save_m2m()

                    # =========================
                    # LOG
                    # =========================


                    ACTION_ECLAIRAGE = gettext_noop(
                        "Contrôle de l'éclairage"
                    )

                    UserLog.objects.create(
                        utilisateur=request.user,
                        action=f"{ACTION_ECLAIRAGE} - {exemplaire.immatriculation}"
                    )

                # =========================
                # SUCCÈS
                # =========================
                messages.success(
                    request,
                    _("Contrôle de l'éclairage enregistré avec succès.")
                )

                return redirect(
                    f"{reverse('eclairage:eclairage_list', kwargs={'exemplaire_id': exemplaire.id})}?saved=1"
                )


            except Exception as e:

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

        eclairage = Eclairage(
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
            kilometres_dernier_entretien=(
                    exemplaire.kilometres_dernier_entretien or 0
            ),

        )

        eclairage.assign_technicien(request.user)

        form = EclairageForm(
            instance=eclairage,
            user=request.user,
            exemplaire=exemplaire,
        )

    # =========================
    # TEMPLATE
    # =========================
    return render(
        request,
        "eclairage/eclairage_check.html",
        {
            "exemplaire": exemplaire,
            "immatriculation": exemplaire.immatriculation,
            "maintenance": maintenance,
            "form": form,
            "now": timezone.now(),
        }
    )




# ------------
# Vue détail eclairage
# -----------------------------
@never_cache
@login_required
def eclairage_detail_view(request, eclairage_id):
    tenant = request.user.societe

    eclairage = get_object_or_404(
        Eclairage.objects.select_related("voiture_exemplaire").filter(q_intervention_tenant(request.user)),
        id=eclairage_id
    )

    context = {
        "eclairage": eclairage,
        "exemplaire": eclairage.voiture_exemplaire,
    }
    return render(request, "eclairage/eclairage_detail.html", context)





# ---------------------
# Modifier eclairage
# ---------------------

@never_cache
@login_required
def modifier_eclairage_view(request, eclairage_id):

    tenant = request.user.societe

    # ==================================================
    # RÉCUPÉRATION eclairage
    # ==================================================
    eclairage = get_object_or_404(
        Eclairage.objects.select_related(
            "voiture_exemplaire",
            "maintenance",
            "tech_societe",
            "tech_technicien",
        ),
        id=eclairage_id,
    )

    # ==================================================
    # VÉHICULE + SÉCURITÉ TENANT
    # ==================================================
    exemplaire = get_object_or_404(
        VoitureExemplaire.objects.filter(
            Q(client__societe=tenant)
            |
            Q(
                client__isnull=True,
                societe=tenant
            )
        ),
        id=eclairage.voiture_exemplaire_id
    )

    # ==================================================
    # KILOMÉTRAGE HISTORIQUE
    #
    # IMPORTANT :
    # Cette valeur correspond au kilométrage AVANT
    # la création de l'eclairage.
    #
    # Elle ne doit jamais être remplacée pendant
    # une modification.
    # ==================================================
    km_reference = (
        eclairage.kilometres_chassis or 0
    )

    # ==================================================
    # POST
    # ==================================================
    if request.method == "POST":

        form = EclairageForm(
            request.POST,
            instance=eclairage,
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
                        "kilometrage_eclairage"
                    )

                    if km is not None:
                        km = int(km)

                    # ==================================================
                    # KILOMÉTRAGE ACTUEL DU VÉHICULE
                    #
                    # Utilisé uniquement pour la validation.
                    # Ce n'est PAS un nouveau rollback.
                    # ==================================================
                    km_actuel_chassis = (
                        exemplaire.kilometres_chassis or 0
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

                        # ----------------------------------------------
                        # Lors d'une modification d'un eclairage,
                        # on autorise une valeur >= au kilométrage
                        # historique avant cet eclairage.
                        #
                        # Exemple :
                        #
                        # avant eclairage : 100000
                        # création        : 105000
                        # modification    : 103000
                        #
                        # 103000 reste valide car >= 100000.
                        # ----------------------------------------------
                        if km < km_reference:
                            raise ValidationError(
                                _(
                                    "Le kilométrage ne peut pas être "
                                    "inférieur à %(km)s km."
                                ) % {
                                    "km": km_reference
                                }
                            )

                    # ==================================================
                    # eclairage
                    # ==================================================
                    eclairage = form.save(
                        commit=False
                    )

                    eclairage.voiture_exemplaire = (
                        exemplaire
                    )

                    # ==================================================
                    # IMPORTANT : ROLLBACK
                    #
                    # NE PAS modifier les champs suivants :
                    #
                    # eclairage.kilometres_chassis
                    # eclairage.kilometres_moteur
                    # eclairage.kilometres_boite
                    # eclairage.kilometres_embrayage
                    # eclairage.kilometres_dernier_eclairage
                    #
                    # Ils contiennent l'état du véhicule AVANT
                    # la création initiale de cet eclairage.
                    # ==================================================

                    # ==================================================
                    # NOUVEAU KILOMÉTRAGE eclairage
                    # ==================================================
                    eclairage.kilometrage_eclairage = (
                        km
                    )

                    # ==================================================
                    # VARIATION
                    #
                    # Toujours calculée depuis le kilométrage
                    # historique avant création.
                    # ==================================================
                    if km is not None:

                        eclairage.kilometrage_variation = (
                            km - km_reference
                        )

                    else:

                        eclairage.kilometrage_variation = 0

                    # ==================================================
                    # TECHNICIEN
                    # ==================================================
                    eclairage.assign_technicien(
                        request.user
                    )

                    eclairage.tech_last_maintained_by = (
                        request.user
                    )

                    # ==================================================
                    # MISE À JOUR DU VÉHICULE
                    # ==================================================
                    if km is not None:

                        # ----------------------------------------------
                        # CHÂSSIS
                        # ----------------------------------------------
                        exemplaire.kilometres_chassis = (
                            km
                        )

                        # ----------------------------------------------
                        # DERNIER ENTRETIEN
                        #
                        # Le kilométrage actuellement saisi devient
                        # le dernier kilométrage d'entretien du véhicule.
                        # ----------------------------------------------
                        exemplaire.kilometres_dernier_entretien = (
                            km
                        )

                        # ----------------------------------------------
                        # DATE DERNIÈRE INTERVENTION
                        # ----------------------------------------------
                        exemplaire.date_derniere_intervention = (
                            timezone.localtime(
                                timezone.now()
                            ).date()
                        )

                        # ----------------------------------------------
                        # RECALCUL MOTEUR / BOÎTE
                        #
                        # Si save() de VoitureExemplaire appelle déjà
                        # update_kilometres(), ne pas l'appeler ici
                        # une deuxième fois.
                        # ----------------------------------------------
                        exemplaire.save()

                    # ==================================================
                    # SAUVEGARDE ENTRETIEN
                    #
                    # ATTENTION :
                    # Entretien.save() ne doit PAS réécrire les champs
                    # historiques kilometres_* depuis l'exemplaire.
                    # ==================================================
                    eclairage.save()

                    # ==================================================
                    # MANY TO MANY
                    # ==================================================
                    form.save_m2m()

                    # ==================================================
                    # MAINTENANCE ASSOCIÉE
                    # ==================================================
                    if eclairage.maintenance:

                        maintenance = (
                            eclairage.maintenance
                        )

                        if km is not None:

                            maintenance.kilometres_chassis = (
                                km
                            )

                            # Le dernier eclairage de la maintenance
                            # correspond également au nouveau km.
                            maintenance.kilometres_dernier_entretien = (
                                km
                            )

                            maintenance.save(
                                update_fields=[
                                    "kilometres_chassis",
                                    "kilometres_dernier_entretien",
                                ]
                            )

                    # ==================================================
                    # LOG
                    # ==================================================
                    ACTION_MODIFICATION_eclairage = (
                        gettext_noop(
                            "Modification du contrôle de l'eclairage"
                        )
                    )

                    UserLog.objects.create(
                        utilisateur=request.user,
                        action=(
                            f"{ACTION_MODIFICATION_eclairage} - "
                            f"{exemplaire.immatriculation}"
                        )
                    )

                # ==================================================
                # SUCCÈS
                # ==================================================
                messages.success(
                    request,
                    _(
                        "Contrôle de l'éclairage modifié avec succès !"
                    )
                )

                return redirect(
                    f"{reverse('eclairage:eclairage_detail', kwargs={'eclairage_id': eclairage.id})}?saved=1"
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
                _(
                    "Le formulaire contient des erreurs."
                )
            )

    # ==================================================
    # GET
    # ==================================================
    else:

        form = EclairageForm(
            instance=eclairage,
            user=request.user,
            exemplaire=exemplaire,
        )

    # ==================================================
    # TEMPLATE
    # ==================================================
    return render(
        request,
        "eclairage/modifier_eclairage.html",
        {
            "form": form,
            "eclairage": eclairage,
            "exemplaire": exemplaire,
            "km_reference": km_reference,
        }
    )


@never_cache
@login_required
def delete_eclairage_view(request, eclairage_id):

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
    # RÉCUPÉRATION eclairage
    # ==================================================
    eclairage = get_object_or_404(
        Eclairage.objects.select_related(
            "voiture_exemplaire",
            "maintenance",
        ),
        id=eclairage_id,
    )

    exemplaire = eclairage.voiture_exemplaire
    maintenance = eclairage.maintenance

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
                exemplaire_id = exemplaire.id

                # ==================================================
                # VALEURS HISTORIQUES
                #
                # Ces valeurs correspondent à l'état du véhicule
                # AVANT la création de cet eclairage.
                # ==================================================

                ancien_km_chassis = (
                    eclairage.kilometres_chassis or 0
                )

                ancien_km_boite = (
                    eclairage.kilometres_boite or 0
                )

                ancien_km_moteur = (
                    eclairage.kilometres_moteur or 0
                )

                ancien_km_embrayage = (
                    eclairage.kilometres_embrayage or 0
                )

                ancien_km_dernier_entretien = (
                        exemplaire.kilometres_entretien_rollback or 0
                )

                # ==================================================
                # RESTAURATION DU VÉHICULE
                # ==================================================

                exemplaire.kilometres_chassis = (
                    ancien_km_chassis
                )

                exemplaire.kilometres_boite = (
                    ancien_km_boite
                )

                exemplaire.kilometres_moteur = (
                    ancien_km_moteur
                )

                exemplaire.kilometres_embrayage = (
                    ancien_km_embrayage
                )

                exemplaire.kilometres_dernier_entretien = (
                    ancien_km_dernier_entretien
                )

                # ==================================================
                # SAUVEGARDE DIRECTE
                #
                # IMPORTANT :
                # update_fields empêche de sauvegarder inutilement
                # d'autres champs.
                # ==================================================

                exemplaire.save(
                    update_fields=[
                        "kilometres_chassis",
                        "kilometres_boite",
                        "kilometres_moteur",
                        "kilometres_embrayage",
                        "kilometres_dernier_entretien",
                    ]
                )

                # ==================================================
                # SUPPRESSION eclairage
                # ==================================================

                eclairage.delete()

                # ==================================================
                # SUPPRESSION MAINTENANCE ASSOCIÉE
                # ==================================================

                if maintenance:
                    maintenance.delete()

                # ==================================================
                # USER LOG
                # ==================================================

                ACTION_SUPPRESSION_eclairage = gettext_noop(
                    "Suppression du contrôle de l'éclairage"
                )
                UserLog.objects.create(
                    utilisateur=request.user,
                    action=(
                        f"{ACTION_SUPPRESSION_eclairage} - "
                        f"{immatriculation}"
                    )
                )

            # ==================================================
            # SUCCÈS
            # ==================================================

            messages.success(
                request,
                _("Contrôle de l'éclairage supprimé avec succès.")
            )

            return redirect(
                f"{reverse('eclairage:eclairage_list', kwargs={'exemplaire_id': exemplaire.id})}?deleted=1"
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
                "eclairage:eclairage_detail",
                eclairage_id=eclairage.id,
            )

    # ==================================================
    # GET → CONFIRMATION
    # ==================================================

    return render(
        request,
        "eclairage/delete_eclairage.html",
        {
            "eclairage": eclairage,
            "exemplaire": exemplaire,
        }
    )






@login_required
def eclairage_pdf_view(request, eclairage_id):
    tenant = request.user.societe

    eclairage = get_object_or_404(
        Eclairage.objects.select_related(
            "voiture_exemplaire",
            "tech_technicien",
            "tech_societe",
            "main_oeuvre",
        ),
        id=eclairage_id
    )

    rapport = eclairage.generer_rapport_remplacement()

    html_string = render_to_string(
        "eclairage/eclairage_detail_pdf.html",
        {
            "eclairage": eclairage,
            "objet": eclairage,
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
        eclairage.voiture_exemplaire.immatriculation
        if eclairage.voiture_exemplaire
        else "sans_immatriculation"
    )

    # =========================================================
    # TECHNICIEN
    # =========================================================

    technicien = (
        eclairage.tech_nom_technicien
        or "technicien_inconnu"
    )

    # Nettoyage pour le nom du fichier
    technicien = str(technicien).replace(" ", "_")
    immatriculation = str(immatriculation).replace(" ", "_")

    # =========================================================
    # DATE
    # =========================================================

    date_pdf = (
        eclairage.date.strftime("%Y-%m-%d")
        if eclairage.date
        else timezone.now().strftime("%Y-%m-%d")
    )

    # =========================================================
    # TITRE / NOM DU PDF
    # =========================================================

    nom_fichier = (
        f"Eclairage_{technicien}_{immatriculation}_{date_pdf}.pdf"
    )

    response = HttpResponse(
        pdf,
        content_type="application/pdf",
    )

    response["Content-Disposition"] = (
        f'inline; filename="{nom_fichier}"'
    )

    return response