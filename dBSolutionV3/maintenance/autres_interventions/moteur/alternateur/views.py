from datetime import datetime

from django.core.exceptions import ValidationError

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
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
from weasyprint import HTML
from .forms import AlternateurForm
from .models import Alternateur








@method_decorator([login_required, never_cache], name='dispatch')
class AlternateurListView(ListView):
    model = Alternateur
    template_name = "alternateur/alternateur_list.html"
    context_object_name = "alternateurs"
    ordering = ["-date"]

    def get_queryset(self):
        queryset = Alternateur.objects.select_related(
            "voiture_exemplaire",
            "maintenance",
            "tech_societe",
            "main_oeuvre"
        )

        societe = getattr(self.request.user, "societe", None)
        if societe:
            queryset = queryset.filter(
                models.Q(tech_societe=societe) | models.Q(tech_societe__isnull=True)
            )

        return queryset.order_by("-date")

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
def alternateur_check_view(request, exemplaire_id):
    tenant = request.user.societe
    role = request.user.role

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

    # ==================================================
    # VÉHICULE
    # ==================================================
    exemplaire = get_object_or_404(
        VoitureExemplaire.objects.filter(
            Q(client__societe=tenant)
            | Q(client__isnull=True, societe=tenant)
        ),
        id=exemplaire_id,
    )

    maintenance = None

    # ==================================================
    # POST
    # ==================================================
    if request.method == "POST":

        form = AlternateurForm(
            request.POST,
            user=request.user,
            exemplaire=exemplaire,
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

                km = form.cleaned_data.get("kilometrage_alte")

                if km is None:
                    form.add_error(
                        "kilometrage_alte",
                        _("Le kilométrage est obligatoire."),
                    )

                else:
                    km = int(km)

                    if km < ancien_kilometrage:
                        form.add_error(
                            "kilometrage_alte",
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

                            # ==================================================
                            # MAINTENANCE
                            # ==================================================
                            maintenance = Maintenance(
                                societe=tenant,
                                voiture_exemplaire=exemplaire,
                                immatriculation=exemplaire.immatriculation,
                                date_intervention=timezone.now().date(),

                                # Snapshot avant intervention
                                kilometres_chassis=ancien_kilometrage,

                                kilometres_dernier_entretien=(
                                    exemplaire.kilometres_dernier_entretien
                                ),

                                type_maintenance=(
                                    Maintenance.TypeMaintenance.ALTERNATEUR
                                ),

                                tag=Maintenance.Tag.JAUNE,
                            )

                            # ==================================================
                            # TECHNICIEN MAINTENANCE
                            # ==================================================
                            if role == "mecanicien":
                                maintenance.mecanicien = request.user

                            elif role == "chef_mecanicien":
                                maintenance.chef_mecanicien = request.user

                            elif role == "magasinier":
                                maintenance.magasinier = request.user

                            elif role == "direction":
                                maintenance.direction = request.user

                            maintenance.save()

                            if role == "apprenti":
                                maintenance.apprentis.add(request.user)

                            # ==================================================
                            # CONTRÔLE ALTERNATEUR
                            # ==================================================
                            alternateur = form.save(commit=False)

                            alternateur.voiture_exemplaire = (
                                exemplaire
                            )

                            alternateur.maintenance = (
                                maintenance
                            )

                            # ---------------------------------------------
                            # Kilométrage AVANT intervention
                            # ---------------------------------------------
                            alternateur.kilometres_chassis = (
                                ancien_kilometrage
                            )

                            alternateur.kilometres_boite = (
                                ancien_kilometrage_boite
                            )

                            alternateur.kilometres_moteur = (
                                ancien_kilometrage_moteur
                            )

                            # ---------------------------------------------
                            # Kilométrage alternateur
                            # ---------------------------------------------
                            alternateur.kilometrage_alte = km

                            # ---------------------------------------------
                            # Variation kilométrique
                            # ---------------------------------------------
                            alternateur.kilometrage_variation = (
                                kilometrage_variation
                            )

                            # =============================================
                            # TECHNICIEN
                            # =============================================
                            alternateur.assign_technicien(
                                request.user
                            )

                            alternateur.tech_last_maintained_by = (
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
                            if alternateur.main_oeuvre_id:

                                main_oeuvre = (
                                    alternateur.main_oeuvre
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

                                alternateur.main_oeuvre = (
                                    main_oeuvre
                                )

                            # ==================================================
                            # SAUVEGARDE ALTERNATEUR
                            # IMPORTANT :
                            # EN DEHORS DU IF/ELSE MAIN-D'ŒUVRE
                            # ==================================================
                            alternateur.save()

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

                            # ==================================================
                            # LOG
                            # ==================================================


                            ACTION_CONTROLE_ALTERNATEUR = gettext_noop(
                                "Contrôle de l'alternateur"
                            )

                            UserLog.objects.create(
                                utilisateur=request.user,
                                action=f"{ACTION_CONTROLE_ALTERNATEUR} - {exemplaire.immatriculation}"
                            )

                        # ==================================================
                        # SUCCÈS
                        # ==================================================
                        messages.success(
                            request,
                            _(
                                "Check alternateur enregistré avec succès."
                            ),
                        )

                        return redirect(
                            "alternateur:alternateur_list",
                            exemplaire_id=exemplaire.id,
                        )

            except ValueError as erreur:
                messages.error(
                    request,
                    _(
                        "Erreur lors de l'enregistrement : "
                        "%(erreur)s"
                    )
                    % {
                        "erreur": str(erreur),
                    },
                )

            except Exception as erreur:
                messages.error(
                    request,
                    _(
                        "Erreur lors de l'enregistrement : "
                        "%(erreur)s"
                    )
                    % {
                        "erreur": str(erreur),
                    },
                )

        else:
            messages.error(
                request,
                _("Le formulaire contient des erreurs."),
            )

    # ==================================================
    # GET
    # ==================================================
    else:

        controle_alternateur_initial = Alternateur(
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

        controle_alternateur_initial.assign_technicien(
            request.user
        )

        form = AlternateurForm(
            instance=controle_alternateur_initial,
            user=request.user,
            exemplaire=exemplaire,
        )

    # ==================================================
    # SECTIONS
    # ==================================================
    sections = [
        {
            "title": _("Kilométrage"),
            "icon": "icons/compteur.png",
            "fields": [
                field
                for field in form
                if "kilo" in field.name
            ],
        },

        {
            "title": _("Diagnostic"),
            "icon": "icons/diagnostic.png",
            "fields": [
                field
                for field in form
                if "diagnostic" in field.name
            ],
        },

        {
            "title": _("Alternateur"),
            "icon": "icons/alternateur.png",
            "fields": [
                field
                for field in form
                if "alternateur" in field.name
            ],
        },

        {
            "title": _("Courroie d'accessoires"),
            "icon": "icons/courroie-daccessoires.png",
            "fields": [
                field
                for field in form
                if "courroie_accessoires" in field.name
            ],
        },

        {
            "title": _("Étiquette"),
            "icon": "icons/tag.png",
            "fields": [
                field
                for field in form
                if "tag" in field.name
            ],
        },

        {
            "title": _("Pays"),
            "icon": "icons/pays.png",
            "fields": [
                field
                for field in form
                if "pays" in field.name
            ],
        },

        {
            "title": _("Remarques"),
            "icon": "icons/notes.png",
            "fields": [
                field
                for field in form
                if "remarques" in field.name
            ],
        },
        {
            "title": _("Serrage des roues"),
            "icon": "icons/roue.png",
            "fields": [form[f.name] for f in form if "serrage" in f.name],
        },

        {
            "title": _("Technicien"),
            "icon": "icons/mecanicien.png",
            "fields": [
                field
                for field in form
                if "tech_" in field.name
            ],
        },

        {
            "title": _("Main-d'œuvre"),
            "icon": "icons/taux.png",
            "fields": [
                field
                for field in form
                if field.name == "taux_horaire"
            ],
        },
    ]

    # ==================================================
    # RENDER
    # ==================================================
    return render(
        request,
        "alternateur/alternateur_check.html",
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
def alternateur_detail_view(request, alternateur_id):
    alternateur= get_object_or_404(
        Alternateur.objects.select_related("voiture_exemplaire"),
        id=alternateur_id
    )

    context = {
        "alternateur": alternateur,
        "exemplaire": alternateur.voiture_exemplaire,
    }
    return render(request, "alternateur/alternateur_detail.html", context)



@login_required
def modifier_alternateur_view(request, alternateur_id):
    tenant = request.user.societe


    # Récupération de l'admission avec son exemplaire
    alternateur = get_object_or_404(
        Alternateur.objects.select_related("voiture_exemplaire"),
        id=alternateur_id
    )
    exemplaire = alternateur.voiture_exemplaire
    # -------------------------
    # POST
    # -------------------------
    if request.method == "POST":
        form = AlternateurForm(
            request.POST,
            instance=alternateur,
            user=request.user,
            exemplaire=alternateur.voiture_exemplaire
        )

        if form.is_valid():

            try:
                with transaction.atomic():

                    # ==================================================
                    # NOUVEAU KILOMÉTRAGE SAISI
                    # ==================================================
                    km = form.cleaned_data.get(
                        "kilometrage_alte"
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
                    alternateur = form.save(
                        commit=False
                    )

                    alternateur.voiture_exemplaire = (
                        exemplaire
                    )

                    # ==================================================
                    # ROLLBACK LOCAL
                    # ==================================================
                    alternateur.kilometres_chassis = (
                        rollback_chassis
                    )

                    alternateur.kilometres_moteur = (
                        rollback_moteur
                    )

                    alternateur.kilometres_boite = (
                        rollback_boite
                    )

                    # ==================================================
                    # NOUVEAU KILOMÉTRAGE
                    # ==================================================
                    alternateur.kilometrage_alte = km

                    # ==================================================
                    # VARIATION
                    # ==================================================
                    if km is not None:
                        alternateur.kilometrage_variation = (
                                km - rollback_chassis
                        )
                    else:
                        alternateur.kilometrage_variation = 0

                    # ==================================================
                    # TECHNICIEN
                    # ==================================================
                    alternateur.assign_technicien(
                        request.user
                    )

                    alternateur.tech_last_maintained_by = (
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
                    alternateur.save()

                    form.save_m2m()

                    ACTION_MODIFICATION_CONTROLE_ALTERNATEUR = gettext_noop(
                        "Modification du contrôle de l'alternateur"
                    )

                    UserLog.objects.create(
                        utilisateur=request.user,
                        action=f"{ACTION_MODIFICATION_CONTROLE_ALTERNATEUR} - {exemplaire.immatriculation}"
                    )

                    messages.success(request, _("Contrôle de l'alternateur modifié avec succès !"))
                    return redirect("alternateur:alternateur_detail", alternateur_id=alternateur.id)


            except Exception as e:

                messages.error(
                    request,
                    _(
                        "Erreur lors de la modification : "
                        "%(erreur)s"
                    ) % {
                        "erreur": str(e)
                    },
                )


        else:
            messages.error(request, _("Le formulaire contient des erreurs."))

    # -------------------------
    # GET
    # -------------------------
    else:
        form = AlternateurForm(
            instance=alternateur,
            user=request.user,
            exemplaire=alternateur.voiture_exemplaire
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
            "title": _("Diagnostic"),
            "icon": "icons/diagnostic.png",
            "fields": [form[f.name] for f in form if "diagnostic" in f.name],
        },
        {
            "title": _("Alternateur"),
            "icon": "icons/alternateur.png",
            "fields": [form[f.name] for f in form if "alternateur" in f.name],
        },
        {
            "title": _("Courroie d'accessoires"),
            "icon": "icons/courroie-daccessoires.png",
            "fields": [form[f.name] for f in form if "courroie_accessoires" in f.name],
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
        "alternateur/modifier_alternateur.html",
        {
            "form": form,
            "alternateur": alternateur,
            "sections": sections,
            "exemplaire": exemplaire,
        }
    )




@never_cache
@login_required
def delete_alternateur_view(request, alternateur_id):

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
    alternateur = get_object_or_404(
        Alternateur.objects.select_related(
            "voiture_exemplaire",
            "maintenance",
        ),
        id=alternateur_id,
    )

    exemplaire = alternateur.voiture_exemplaire
    maintenance = alternateur.maintenance

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
                alternateur.delete()

                # ==================================================
                # SUPPRESSION MAINTENANCE ASSOCIÉE
                # ==================================================
                if maintenance:
                    maintenance.delete()

                # ==================================================
                # USER LOG
                # ==================================================
                ACTION_SUPPRESSION_ATERNATEUR = gettext_noop(
                    "Suppression du contrôle de l'alternateur"
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
                _("Contrôle de l'alternateur supprimé avec succès.")
            )

            return redirect(
                "alternateur:alternateur_list",
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
                "alternateur:alternateur_detail",
                 alternateur_id=alternateur.id,
            )

    # ==================================================
    # GET → CONFIRMATION
    # ==================================================
    return render(
        request,
        "alternateur/delete_alternateur.html",
        {
            "alternateur": alternateur,
            "exemplaire": exemplaire,
        }
    )








@login_required
def alternateur_detail_pdf_view(request, pk):
    alternateur = get_object_or_404(Alternateur, pk=pk)

    rapport = alternateur.generer_rapport_remplacement()

    html_string = render_to_string(
        "alternateur/alternateur_detail_pdf.html",
        {
            "alternateur": alternateur,
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
        alternateur.voiture_exemplaire.immatriculation
        if alternateur.voiture_exemplaire
        else "sans_immatriculation"
    )

    # =========================================================
    # TECHNICIEN
    # =========================================================

    technicien = (
            alternateur.tech_nom_technicien
            or "technicien_inconnu"
    )

    # Nettoyage pour le nom du fichier
    technicien = str(technicien).replace(" ", "_")
    immatriculation = str(immatriculation).replace(" ", "_")

    # =========================================================
    # DATE
    # =========================================================

    date_pdf = (
        alternateur.date.strftime("%Y-%m-%d")
        if alternateur.date
        else timezone.now().strftime("%Y-%m-%d")
    )

    # =========================================================
    # TITRE / NOM DU PDF
    # =========================================================

    nom_fichier = (
        f"{_('Alternateur')}_{technicien}_{immatriculation}_{date_pdf}.pdf"
    )

    response = HttpResponse(
        pdf,
        content_type="application/pdf",
    )

    response["Content-Disposition"] = (
        f'inline; filename="{nom_fichier}"'
    )

    return response
