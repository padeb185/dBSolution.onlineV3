from decimal import Decimal
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.db import models, transaction
from maindoeuvre.models import MainDoeuvre
from utilisateurs.models import UserLog
from django.contrib import messages
from maintenance.models import Maintenance
from .forms import RemplacementMoteurForm
from django.utils.translation import gettext_lazy as _, gettext_noop
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.db.models import Q, F
from .models import RemplacementMoteur
from voiture.voiture_exemplaire.models import VoitureExemplaire
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.translation import gettext as _
from weasyprint import HTML, pdf


@method_decorator([login_required, never_cache], name="dispatch")
class RemplacementMoteurListView(ListView):
    model = RemplacementMoteur
    template_name = "remplacement_moteur/remplacement_moteur_list.html"
    context_object_name = "remplacements"



    def get_queryset(self):
        queryset = RemplacementMoteur.objects.select_related(
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
def remplacement_moteur_form_view(request, exemplaire_id):

    tenant = request.user.societe
    role = request.user.role

    # ==========================================================
    # EXEMPLAIRE
    # ==========================================================
    exemplaire = get_object_or_404(
        VoitureExemplaire.objects.filter(
            Q(client__societe=tenant)
            | Q(
                client__isnull=True,
                societe=tenant
            )
        ),
        id=exemplaire_id
    )

    # ==========================================================
    # DROITS
    # ==========================================================
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
            _("Accès refusé")
        )

        return redirect(
            "utilisateurs:dashboard"
        )

    remplacement_moteur = None

    # ==========================================================
    # POST
    # ==========================================================
    if request.method == "POST":

        form = RemplacementMoteurForm(
            request.POST,
            user=request.user,
            exemplaire=exemplaire
        )

        if form.is_valid():

            try:
                with transaction.atomic():

                    # ==================================================
                    # VALEURS AVANT MODIFICATION
                    # ==================================================
                    ancien_km_chassis = (
                        exemplaire.kilometres_chassis
                        or 0
                    )
                    ancien_kilometrage = (
                            exemplaire.kilometres_chassis or 0
                    )
                    ancien_km_moteur = (
                        exemplaire.kilometres_moteur
                        or 0
                    )
                    ancien_kilometrage_moteur = (
                            exemplaire.kilometres_moteur
                            or 0
                    )
                    ancien_kilometrage_boite = (
                            exemplaire.kilometres_boite or 0
                    )
                    # ==================================================
                    # NOUVEAU KILOMÉTRAGE
                    # ==================================================
                    nouveau_km = (
                        form.cleaned_data.get(
                            "kilometres_remplacement"
                        )
                    )

                    # ==================================================
                    # VALIDATION SUPPLÉMENTAIRE
                    # ==================================================
                    if (
                        nouveau_km is not None
                        and nouveau_km < ancien_km_chassis
                    ):
                        form.add_error(
                            "kilometres_remplacement",
                            _(
                                "Le kilométrage ne peut pas être "
                                "inférieur au dernier kilométrage."
                            )
                        )

                        raise ValidationError(
                            _(
                                "Le kilométrage ne peut pas être "
                                "inférieur au dernier kilométrage."
                            )
                        )

                    else:
                        kilometrage_variation = (
                                nouveau_km - ancien_kilometrage
                        )

                    exemplaire.kilometres_rollback = (
                        ancien_kilometrage
                    )

                    exemplaire.kilometres_boite_rollback = (
                        ancien_kilometrage_boite
                    )

                    # ==========================================================
                    # ROLLBACK KILOMÉTRAGE MOTEUR
                    #
                    # Dès qu'un kilométrage de remplacement est introduit,
                    # on mémorise UNE SEULE FOIS le kilométrage moteur actuel.
                    # ==========================================================
                    if nouveau_km is not None:

                        if exemplaire.kilometres_moteur_rollback is None:
                            exemplaire.kilometres_moteur_rollback = (
                                ancien_kilometrage_moteur
                            )

                    exemplaire.date_derniere_intervention = (
                        timezone.localtime(
                            timezone.now()
                        ).date()
                    )

                    # =============================================
                    # NOUVEAU KILOMÉTRAGE
                    # =============================================
                    exemplaire.kilometres_chassis = nouveau_km

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
                    maintenance = Maintenance.objects.create(
                        societe=request.user.societe,
                        voiture_exemplaire=exemplaire,
                        immatriculation=(
                            exemplaire.immatriculation
                        ),
                        date_intervention=(
                            timezone.now().date()
                        ),

                        # Ancienne valeur avant le contrôle
                        kilometres_chassis=(
                            ancien_km_chassis
                        ),

                        kilometres_dernier_entretien=(
                            exemplaire.kilometres_dernier_entretien
                        ),

                        type_maintenance=(
                            Maintenance.TypeMaintenance.REMPLACEMENT_MOTEUR
                        ),

                        tag=Maintenance.Tag.JAUNE,
                    )

                    # ==================================================
                    # UTILISATEUR / RÔLE SUR MAINTENANCE
                    # ==================================================
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

                    # M2M après sauvegarde
                    if role == "apprenti":
                        maintenance.apprentis.add(
                            request.user
                        )

                    # ==================================================
                    # PRÉPARATION DU REMPLACEMENT MOTEUR
                    # ==================================================
                    form.instance.voiture_exemplaire = (
                        exemplaire
                    )

                    # Si ton modèle RemplacementMoteur
                    # possède bien le champ maintenance
                    if hasattr(
                        form.instance,
                        "maintenance"
                    ):
                        form.instance.maintenance = (
                            maintenance
                        )

                    # ==================================================
                    # IMPORTANT
                    #
                    # Une seule sauvegarde du formulaire.
                    #
                    # RemplacementMoteurForm.save() doit :
                    #
                    # ancien chassis = exemplaire.kilometres_chassis
                    # ancien moteur  = exemplaire.kilometres_moteur
                    #
                    # différence =
                    # nouveau km - ancien chassis
                    #
                    # nouveau moteur =
                    # ancien moteur + différence
                    #
                    # puis mettre à jour l'exemplaire.
                    # ==================================================

                    remplacement_moteur = form.save(commit=False)

                    remplacement_moteur.voiture_exemplaire = (
                        exemplaire
                    )

                    remplacement_moteur.maintenance = (
                        maintenance
                    )

                    # ---------------------------------------------
                    # Kilométrage AVANT intervention
                    # ---------------------------------------------
                    remplacement_moteur.kilometres_chassis = (
                        ancien_kilometrage
                    )

                    remplacement_moteur.kilometres_boite = (
                        ancien_kilometrage_boite
                    )

                    remplacement_moteur.kilometres_moteur = (
                        ancien_kilometrage_moteur
                    )

                    # ---------------------------------------------
                    # Kilométrage remplacement_moteur
                    # ---------------------------------------------
                    remplacement_moteur.kilometrage_remplacement_moteur = nouveau_km

                    # ---------------------------------------------
                    # Variation kilométrique
                    # ---------------------------------------------
                    remplacement_moteur.kilometrage_variation = (
                        kilometrage_variation
                    )

                    # =============================================
                    # TECHNICIEN
                    # =============================================
                    remplacement_moteur.assign_technicien(
                        request.user
                    )

                    remplacement_moteur.tech_last_maintained_by = (
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
                    if remplacement_moteur.main_oeuvre_id:

                        main_oeuvre = (
                            remplacement_moteur.main_oeuvre
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

                        remplacement_moteur.main_oeuvre = (
                            main_oeuvre
                        )

                    # ==================================================
                    # SAUVEGARDE remplacement_moteur
                    # IMPORTANT :
                    # EN DEHORS DU IF/ELSE MAIN-D'ŒUVRE
                    # ==================================================
                    remplacement_moteur.save()

                    form.save_m2m()



                    # ==================================================
                    # LOG
                    # ==================================================
                    ACTION_REMPLACEMENT_MOTEUR = (
                        gettext_noop(
                            "Remplacement moteur"
                        )
                    )

                    UserLog.objects.create(
                        utilisateur=request.user,
                        action=(
                            f"{ACTION_REMPLACEMENT_MOTEUR} - "
                            f"{exemplaire.immatriculation}"
                        )
                    )

                    # ==================================================
                    # RAFRAÎCHIR L'EXEMPLAIRE
                    # ==================================================
                    exemplaire.refresh_from_db()

                # ======================================================
                # SUCCESS
                # ======================================================
                messages.success(
                    request,
                    _(
                        "Remplacement du moteur "
                        "enregistré avec succès"
                    )
                )

                return redirect(
                    "remplacement_moteur:"
                    "remplacement_moteur_list",
                    exemplaire_id=exemplaire.id
                )

            except ValidationError:
                # Les erreurs sont déjà ajoutées au formulaire
                pass

            except Exception as e:

                messages.error(
                    request,
                    str(e)
                )

        else:

            messages.error(
                request,
                _(
                    "Veuillez corriger les erreurs "
                    "du formulaire"
                )
            )

            print(form.errors)

    # ==========================================================
    # GET
    # ==========================================================
    else:

        # ------------------------------------------------------
        # IMPORTANT
        #
        # kilometres_moteur vient de :
        # exemplaire.kilometres_moteur
        #
        # et PAS de :
        # exemplaire.kilometres_chassis
        # ------------------------------------------------------
        remplacement_moteur = RemplacementMoteur(
            voiture_exemplaire=exemplaire,

            kilometres_chassis=(
                exemplaire.kilometres_chassis
                or 0
            ),

            kilometres_moteur=(
                exemplaire.kilometres_moteur
                or 0
            ),
            kilometres_boite=(
                    exemplaire.kilometres_boite or 0
            ),
        )

        remplacement_moteur.assign_technicien(
            request.user
        )

        form = RemplacementMoteurForm(
            instance=remplacement_moteur,
            user=request.user,
            exemplaire=exemplaire
        )

    # ==========================================================
    # SECTIONS
    # ==========================================================
    sections = [
        {
            "title": _("Kilométrage"),
            "icon": "icons/compteur.png",
            "fields": [
                form[f.name]
                for f in form
                if "kilometres" in f.name
            ],
        },

        {
            "title": _("Remplacement du moteur"),
            "icon": "icons/engine.png",
            "fields": [
                form[f.name]
                for f in form
                if "moteurs" in f.name
            ],
        },

        {
            "title": _("Huile moteur"),
            "icon": "icons/huile-moteur.png",
            "fields": [
                form[f.name]
                for f in form
                if "niveau" in f.name
            ],
        },

        {
            "title": _("Liquide de refroidissement"),
            "icon": "icons/anti-gel.png",
            "fields": [
                form[f.name]
                for f in form
                if "refroidissement" in f.name
            ],
        },

        {
            "title": _(
                "Remise à Zéro des kilomètres moteurs"
            ),
            "icon": "icons/km.png",
            "fields": [
                form[f.name]
                for f in form
                if "remplacement_effectue" in f.name
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

    # ==========================================================
    # RENDER
    # ==========================================================
    return render(
        request,
        "remplacement_moteur/"
        "remplacement_moteur_form.html",
        {
            "remplacement_moteur": (
                remplacement_moteur
            ),
            "exemplaire": exemplaire,
            "form": form,
            "sections": sections,
            "now": timezone.now(),
        }
    )

@login_required
def remplacement_moteur_detail_view(request, remplacement_moteur_id):
    remplacement_moteur = get_object_or_404(
        RemplacementMoteur.objects.select_related("voiture_exemplaire"),
        id=remplacement_moteur_id
    )

    context = {
        "remplacement_moteur": remplacement_moteur,
        "exemplaire": remplacement_moteur.voiture_exemplaire,
    }
    return render(request, "remplacement_moteur/remplacement_moteur_detail.html", context)





@login_required
def modifier_remplacement_moteur_view(request, remplacement_moteur_id):
    tenant = request.user.societe

    # ==========================================================
    # REMPLACEMENT MOTEUR EXISTANT
    # ==========================================================
    remplacement_moteur = get_object_or_404(
        RemplacementMoteur.objects.select_related(
            "voiture_exemplaire"
        ),
        id=remplacement_moteur_id
    )

    exemplaire = remplacement_moteur.voiture_exemplaire

    # ==========================================================
    # SÉCURITÉ TENANT
    # ==========================================================
    if (
        exemplaire.client
        and exemplaire.client.societe != tenant
    ):
        messages.error(request, _("Accès refusé"))
        return redirect("utilisateurs:dashboard")

    # ==========================================================
    # KILOMÉTRAGE MOTEUR DE RÉFÉRENCE
    #
    # Cette valeur vient de remplacement_moteur_form_view
    # et ne doit PAS être recalculée lors d'une modification.
    # ==========================================================
    km_moteur_reference = remplacement_moteur.kilometres_moteur_rollback

    # ==========================================================
    # POST
    # ==========================================================
    if request.method == "POST":

        form = RemplacementMoteurForm(
            request.POST,
            instance=remplacement_moteur,
            user=request.user,
            exemplaire=exemplaire,
        )

        if form.is_valid():
            try:
                with transaction.atomic():

                    remplacement = form.save(commit=False)

                    # --------------------------------------------------
                    # On conserve le kilométrage moteur enregistré
                    # lors de la création
                    # --------------------------------------------------
                    remplacement.kilometres_moteur = km_moteur_reference

                    remplacement.save()
                    form.save_m2m()

                    # --------------------------------------------------
                    # LOG
                    # --------------------------------------------------
                    ACTION_MODIFICATION_REMPLACEMENT_MOTEUR = gettext_noop(
                        "Modification du remplacement moteur"
                    )

                    UserLog.objects.create(
                        utilisateur=request.user,
                        action=(
                            f"{ACTION_MODIFICATION_REMPLACEMENT_MOTEUR}"
                            f" - {exemplaire.immatriculation}"
                        )
                    )

                    messages.success(
                        request,
                        _("Remplacement du moteur modifié avec succès !")
                    )

                    return redirect(
                        "remplacement_moteur:remplacement_moteur_detail",
                        remplacement_moteur_id=remplacement.id
                    )

            except ValidationError as e:
                form.add_error(None, e)
                messages.error(
                    request,
                    _("Kilométrage invalide")
                )

        else:
            messages.error(
                request,
                _("Le formulaire contient des erreurs.")
            )

    # ==========================================================
    # GET
    # ==========================================================
    else:
        form = RemplacementMoteurForm(
            instance=remplacement_moteur,
            user=request.user,
            exemplaire=exemplaire,
        )

    # ==========================================================
    # SECTIONS
    # ==========================================================
    sections = [
        {
            "title": _("Kilométrage"),
            "icon": "icons/compteur.png",
            "fields": [
                form[f.name]
                for f in form
                if "kilometres" in f.name
            ],
        },
        {
            "title": _("Remplacement du moteur"),
            "icon": "icons/engine.png",
            "fields": [
                form[f.name]
                for f in form
                if "moteurs" in f.name
            ],
        },
        {
            "title": _("Huile moteur"),
            "icon": "icons/huile-moteur.png",
            "fields": [
                form[f.name]
                for f in form
                if "niveau" in f.name
            ],
        },
        {
            "title": _("Liquide de refroidissement"),
            "icon": "icons/anti-gel.png",
            "fields": [
                form[f.name]
                for f in form
                if "refroidissement" in f.name
            ],
        },
        {
            "title": _("Remise à Zéro des kilomètres moteurs"),
            "icon": "icons/km.png",
            "fields": [
                form[f.name]
                for f in form
                if "remplacement_effectue" in f.name
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

    return render(
        request,
        "remplacement_moteur/modifier_remplacement_moteur.html",
        {
            "remplacement_moteur": remplacement_moteur,
            "form": form,
            "sections": sections,
            "exemplaire": exemplaire,
            "km_moteur_reference": km_moteur_reference,
        }
    )





@login_required
def remplacement_moteur_pdf_view(request, remplacement_moteur_id):
    tenant = request.user.societe


    remplacement = get_object_or_404(
        RemplacementMoteur.objects.select_related(
            "voiture_exemplaire",
            "voiture_exemplaire__voiture_marque",
            "voiture_exemplaire__voiture_modele",
            "maintenance",
            "tech_technicien",
            "tech_societe",
            "main_oeuvre",
            "main_oeuvre__utilisateur",
        ),
        pk=remplacement_moteur_id,
    )

    # Rapport des pièces et produits
    rapport = remplacement.generer_rapport_remplacement()

    lignes_rapport = rapport.get("lignes", [])
    total_pieces_produits = rapport.get(
        "total_general",
        Decimal("0.00"),
    )

    # Main-d'œuvre
    cout_main_oeuvre = remplacement.cout_main_oeuvre
    total_general = remplacement.total_general_avec_main_oeuvre

    html_string = render_to_string(
        "remplacement_moteur/remplacement_moteur_pdf.html",
        {
            "remplacement": remplacement,
            "rapport": rapport,
            "lignes_rapport": lignes_rapport,

            # Compatibilité avec les templates utilisant pieces_utilisees
            "pieces_utilisees": lignes_rapport,

            "total_pieces": total_pieces_produits,
            "total_pieces_produits": total_pieces_produits,
            "cout_main_oeuvre": cout_main_oeuvre,
            "total_general": total_general,

            "maintenance": remplacement.maintenance,
            "vehicule": remplacement.voiture_exemplaire,
            "societe": tenant,
            "date_export": timezone.now(),
        },
        request=request,
    )

    pdf = HTML(
        string=html_string,
        base_url=request.build_absolute_uri("/"),
    ).write_pdf()

    vehicule = remplacement.voiture_exemplaire

    # =========================================================
    # IMMATRICULATION
    # =========================================================

    immatriculation = (
        remplacement.voiture_exemplaire.immatriculation
        if remplacement.voiture_exemplaire
        else "sans_immatriculation"
    )

    # =========================================================
    # TECHNICIEN
    # =========================================================

    technicien = (
            remplacement.tech_nom_technicien
            or "technicien_inconnu"
    )

    # Nettoyage pour le nom du fichier
    technicien = str(technicien).replace(" ", "_")
    immatriculation = str(immatriculation).replace(" ", "_")

    # =========================================================
    # DATE
    # =========================================================

    date_pdf = (
        remplacement.date.strftime("%Y-%m-%d")
        if remplacement.date
        else timezone.now().strftime("%Y-%m-%d")
    )

    # =========================================================
    # TITRE / NOM DU PDF
    # =========================================================

    nom_fichier = (
        f"{_('Remplacement moteur')}_{technicien}_{immatriculation}_{date_pdf}.pdf"
    )

    response = HttpResponse(
        pdf,
        content_type="application/pdf",
    )

    response["Content-Disposition"] = (
        f'inline; filename="{nom_fichier}"'
    )

    return response
