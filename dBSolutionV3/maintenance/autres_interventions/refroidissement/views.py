from django.utils.text import slugify
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
from maintenance.autres_interventions.refroidissement.forms import RefForm
from maintenance.autres_interventions.refroidissement.models import Refroidissement
from maintenance.models import Maintenance
from utilisateurs.models import UserLog
from voiture.voiture_exemplaire.models import VoitureExemplaire
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from weasyprint import HTML





@method_decorator([login_required, never_cache], name='dispatch')
class RefListView(ListView):
    model = Refroidissement
    template_name = "refroidissement/ref_list.html"
    context_object_name = "refroidissements"
    ordering = ["-id"]

    def get_queryset(self):
        queryset = Refroidissement.objects.select_related(
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
def ref_form_view(request, exemplaire_id):
    tenant = request.user.societe
    role = request.user.role
    maintenance = None

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



    exemplaire = get_object_or_404(
        VoitureExemplaire.objects.filter(
            Q(client__societe=tenant)
            | Q(client__isnull=True, societe=tenant)
        ),
        id=exemplaire_id,
    )

    # ==================================================
    # POST
    # ==================================================

    if request.method == "POST":
        form = RefForm(
            request.POST,
            user=request.user,
            exemplaire=exemplaire,
        )

        # Très important :
        # la relation doit exister avant form.is_valid()
        form.instance.voiture_exemplaire = exemplaire
        form.instance.kilometres_chassis = exemplaire.kilometres_chassis
        form.instance._user = request.user

        if form.is_valid():

            try:

                # ==================================================
                # KILOMÉTRAGE
                # ==================================================
                km = form.cleaned_data.get("kilometrage_refroidissement")

                ancien_kilometrage = (
                        exemplaire.kilometres_chassis or 0
                )

                if km is None:
                    form.add_error(
                        "kilometrage_refroidissement",
                        _("Le kilométrage est obligatoire."),
                    )

                else:
                    km = int(km)

                    if km < ancien_kilometrage:
                        form.add_error(
                            "kilometrage_refroidissement",
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

                            maintenance = Maintenance.objects.create(
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
                                    Maintenance.TypeMaintenance.REFROIDISSEMENT
                                ),
                                tag=Maintenance.Tag.JAUNE,
                            )

                            # ------------------------------------------
                            # Affectation du personnel
                            # ------------------------------------------

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

                            # ------------------------------------------
                            # Enregistrement du contrôle
                            # ------------------------------------------

                            refroidissement = form.save(commit=False)

                            refroidissement.voiture_exemplaire = exemplaire
                            refroidissement.maintenance = maintenance

                            # Snapshot AVANT intervention
                            refroidissement.kilometres_chassis = (
                                ancien_kilometrage
                            )

                            # Kilométrage du contrôle
                            refroidissement.kilometrage_refroidissement = km

                            # Variation kilométrage
                            refroidissement.kilometrage_variation = (
                                kilometrage_variation
                            )

                            # ==================================================
                            # TECHNICIEN
                            # ==================================================
                            refroidissement.assign_technicien(
                                request.user
                            )

                            refroidissement.tech_last_maintained_by = (
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
                            if refroidissement.main_oeuvre_id:

                                main_oeuvre = (
                                    refroidissement.main_oeuvre
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

                                refroidissement.main_oeuvre = (
                                    main_oeuvre
                                )

                            # ==================================================
                            # SAUVEGARDE refroidissement
                            # IMPORTANT :
                            # EN DEHORS DU IF/ELSE MAIN-D'ŒUVRE
                            # ==================================================
                            refroidissement.save()

                            form.save_m2m()

                            # ==================================================
                            # MISE À JOUR DU VÉHICULE
                            # ==================================================
                            exemplaire.kilometres_chassis = km

                            exemplaire.save(
                                update_fields=[
                                    "kilometres_chassis",
                                ]
                            )

                            # Nécessaire si le formulaire contient
                            # éventuellement des champs ManyToMany
                            form.save_m2m()

                            UserLog.objects.create(
                                utilisateur=request.user,
                                action=_(
                                    "Contrôle système de refroidissement") + f" - {exemplaire.immatriculation}"
                            )

                        messages.success(
                            request,
                            _(
                                "Contrôle du système de refroidissement "
                                "enregistré avec succès."
                            ),
                        )

                        return redirect(
                            "refroidissement:ref_list",
                            exemplaire_id=exemplaire.id,
                        )

            except ValidationError:
                messages.error(
                    request,
                    _("Le formulaire contient des erreurs."),
                )

            except Exception as e:
                messages.error(
                    request,
                    _(
                        "Erreur lors de l'enregistrement : %(erreur)s"
                    ) % {
                        "erreur": str(e),
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
        ref_instance = Refroidissement(
            voiture_exemplaire=exemplaire,
            kilometres_chassis=exemplaire.kilometres_chassis,
        )

        ref_instance.assign_technicien(request.user)

        form = RefForm(
            instance=ref_instance,
            user=request.user,
            exemplaire=exemplaire,
        )

    # ==================================================
    # SECTIONS DU FORMULAIRE
    # ==================================================

    sections = [
        {
            "title": _("Kilométrage"),
            "icon": "icons/compteur.png",
            "fields": [
                field
                for field in form
                if "kilometrage" in field.name
                   or "kilometres" in field.name
            ],
        },
        {
            "title": _("Presence de fuite"),
            "icon": "icons/fuites-eau.png",
            "fields": [
                field
                for field in form
                if "presence" in field.name
            ],
        },
        {
            "title": _("Pression"),
            "icon": "icons/pression-eau.png",
            "fields": [
                field
                for field in form
                if "pression" in field.name
                   or "pression_" in field.name
            ],
        },
        {
            "title": _("Température"),
            "icon": "icons/temperature-eau.png",
            "fields": [
                field
                for field in form
                if "temperature_" in field.name
            ],
        },
        {
            "title": _("circulation"),
            "icon": "icons/circulation-eau.png",
            "fields": [
                field
                for field in form
                if "circulation" in field.name
            ],
        },
        {
            "title": _("Liquide de refroidissement"),
            "icon": "icons/liquide-ref.png",
            "fields": [
                field
                for field in form
                if "liquide" in field.name
            ],
        },
        {
            "title": _("Purge"),
            "icon": "icons/purge-eau.png",
            "fields": [
                field
                for field in form
                if "purge" in field.name
            ],
        },
        {
            "title": _("Ventilateur"),
            "icon": "icons/ventilateur.png",
            "fields": [
                field
                for field in form
                if "ventilateur_" in field.name
            ],
        },
        {
            "title": _("Radiateur"),
            "icon": "icons/radiateur.png",
            "fields": [
                field
                for field in form
                if "radiateur" in field.name
            ],
        },
        {
            "title": _("Thermostat"),
            "icon": "icons/thermostat.png",
            "fields": [
                field
                for field in form
                if "thermostat" in field.name
            ],
        },
        {
            "title": _("Boitier d'eau"),
            "icon": "icons/boitier-eau.png",
            "fields": [
                field
                for field in form
                if "boitier_eau" in field.name
            ],
        },
        {
            "title": _("Sonde de température"),
            "icon": "icons/sonde-temperature.png",
            "fields": [
                field
                for field in form
                if "sonde_t_" in field.name
            ],
        },
        {
            "title": _("Durites"),
            "icon": "icons/durites.png",
            "fields": [
                field
                for field in form
                if "durites" in field.name
            ],
        },
        {
            "title": _("Chaufferette"),
            "icon": "icons/chaufferette.png",
            "fields": [
                field
                for field in form
                if "chaufferette" in field.name
            ],
        },


        {
            "title": _("Étiquette"),
            "icon": "icons/tag.png",
            "fields": [
                field
                for field in form
                if field.name == "tag"
            ],
        },
        {
            "title": _("Pays"),
            "icon": "icons/pays.png",
            "fields": [
                field
                for field in form
                if field.name == "pays"
            ],
        },
        {
            "title": _("Remarques"),
            "icon": "icons/notes.png",
            "fields": [
                field
                for field in form
                if field.name == "remarques"
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
            "title": _("Taux Horaire"),
            "icon": "icons/taux.png",
            "fields": [
                field
                for field in form
                if "taux_" in field.name
            ],
        },
    ]

    return render(
        request,
        "refroidissement/ref_form.html",
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
def ref_detail_view(request, ref_id):
    ref = get_object_or_404(
        Refroidissement.objects.select_related("voiture_exemplaire"),
        id=ref_id
    )

    context = {
        "ref": ref,
        "exemplaire": ref.voiture_exemplaire,
    }
    return render(request, "refroidissement/ref_detail.html", context)



@login_required
def modifier_ref_view(request, ref_id):
    tenant = request.user.societe

    ref = get_object_or_404(
        Refroidissement.objects.select_related("voiture_exemplaire"),
        id=ref_id
    )
    exemplaire = ref.voiture_exemplaire
    # -------------------------
    # POST
    # -------------------------
    if request.method == "POST":
        form = RefForm(
            request.POST,
            instance=ref,
            user=request.user,
            exemplaire=ref.voiture_exemplaire
        )

        if form.is_valid():
            form.save()

            UserLog.objects.create(
                utilisateur=request.user,
                action=_("Modification du contrôle du refroidissement")+ f" - {exemplaire.immatriculation}"
            )

            messages.success(request, _("Contrôle du système de refroidissement modifié avec succès !"))
            return redirect("refroidissement:ref_detail", ref_id=ref.id)

        else:
            messages.error(request, _("Le formulaire contient des erreurs."))

    # -------------------------
    # GET
    # -------------------------
    else:
        form = RefForm(
            instance=ref,
            user=request.user,
            exemplaire=ref.voiture_exemplaire
        )

    # -------------------------
    # Sections pour le template
    # -------------------------

    sections = [
        {
            "title": _("Kilométrage"),
            "icon": "icons/compteur.png",
            "fields": [
                field
                for field in form
                if "kilometrage" in field.name
                   or "kilometres" in field.name
            ],
        },
        {
            "title": _("Presence de fuite"),
            "icon": "icons/fuites-eau.png",
            "fields": [
                field
                for field in form
                if "presence" in field.name
            ],
        },
        {
            "title": _("Pression"),
            "icon": "icons/pression-eau.png",
            "fields": [
                field
                for field in form
                if "pression" in field.name
                   or "pression_" in field.name
            ],
        },
        {
            "title": _("Température"),
            "icon": "icons/temperature-eau.png",
            "fields": [
                field
                for field in form
                if "temperature_" in field.name
            ],
        },
        {
            "title": _("circulation"),
            "icon": "icons/circulation-eau.png",
            "fields": [
                field
                for field in form
                if "circulation" in field.name
            ],
        },
        {
            "title": _("Liquide de refroidissement"),
            "icon": "icons/liquide-ref.png",
            "fields": [
                field
                for field in form
                if "liquide" in field.name
            ],
        },
        {
            "title": _("Purge"),
            "icon": "icons/purge-eau.png",
            "fields": [
                field
                for field in form
                if "purge" in field.name
            ],
        },
        {
            "title": _("Ventilateur"),
            "icon": "icons/ventilateur.png",
            "fields": [
                field
                for field in form
                if "ventilateur_" in field.name
            ],
        },
        {
            "title": _("Radiateur"),
            "icon": "icons/radiateur.png",
            "fields": [
                field
                for field in form
                if "radiateur" in field.name
            ],
        },
        {
            "title": _("Thermostat"),
            "icon": "icons/thermostat.png",
            "fields": [
                field
                for field in form
                if "thermostat" in field.name
            ],
        },
        {
            "title": _("Boitier d'eau"),
            "icon": "icons/boitier-eau.png",
            "fields": [
                field
                for field in form
                if "boitier_eau" in field.name
            ],
        },
        {
            "title": _("Sonde de température"),
            "icon": "icons/sonde-temperature.png",
            "fields": [
                field
                for field in form
                if "sonde_t_" in field.name
            ],
        },
        {
            "title": _("Durites"),
            "icon": "icons/durites.png",
            "fields": [
                field
                for field in form
                if "durites" in field.name
            ],
        },
        {
            "title": _("Chaufferette"),
            "icon": "icons/chaufferette.png",
            "fields": [
                field
                for field in form
                if "chaufferette" in field.name
            ],
        },

        {
            "title": _("Étiquette"),
            "icon": "icons/tag.png",
            "fields": [
                field
                for field in form
                if field.name == "tag"
            ],
        },
        {
            "title": _("Pays"),
            "icon": "icons/pays.png",
            "fields": [
                field
                for field in form
                if field.name == "pays"
            ],
        },
        {
            "title": _("Remarques"),
            "icon": "icons/notes.png",
            "fields": [
                field
                for field in form
                if field.name == "remarques"
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
            "title": _("Taux Horaire"),
            "icon": "icons/taux.png",
            "fields": [
                field
                for field in form
                if "taux_" in field.name
            ],
        },
    ]

    return render(
        request,
        "refroidissement/modifier_ref.html",
        {
            "form": form,
            "ref": ref,
            "sections": sections,
            "exemplaire": exemplaire,
        }
    )



@never_cache
@login_required
def ref_detail_pdf_view(request, pk):
    tenant = request.user.societe

    ref = get_object_or_404(
        Refroidissement.objects.select_related(
            "voiture_exemplaire",
            "maintenance",
            "tech_technicien",
            "tech_societe",
            "main_oeuvre",
            "main_oeuvre__utilisateur",
        ),
        pk=pk,
    )

    rapport = ref.generer_rapport_remplacement() or {
        "lignes": [],
        "total_general": 0,
    }

    html_string = render_to_string(
        "refroidissement/ref_detail_pdf.html",
        {
            "ref": ref,
            "rapport": rapport,
            "date_export": timezone.now(),
        },
        request=request,
    )

    pdf = HTML(
        string=html_string,
        base_url=request.build_absolute_uri("/"),
    ).write_pdf()

    immatriculation = "vehicule"

    if ref.voiture_exemplaire_id:
        immatriculation = (
            ref.voiture_exemplaire.immatriculation
            or "vehicule"
        )

    technicien = (
        ref.tech_nom_technicien
        or "technicien"
    )

    filename = slugify(
        f"Refroidissement-{immatriculation}-{technicien}"
    )

    response = HttpResponse(
        pdf,
        content_type="application/pdf",
    )

    response["Content-Disposition"] = (
        f'inline; filename="{filename}.pdf"'
    )

    return response