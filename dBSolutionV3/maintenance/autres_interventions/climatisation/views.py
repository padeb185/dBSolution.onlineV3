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
from maintenance.models import Maintenance
from utilisateurs.models import UserLog
from voiture.voiture_exemplaire.models import VoitureExemplaire
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from weasyprint import HTML
from .forms import ClimForm
from .models import Climatisation







@method_decorator([login_required, never_cache], name='dispatch')
class ClimListView(ListView):
    model = Climatisation
    template_name = "climatisation/clim_list.html"
    context_object_name = "climatisations"
    ordering = ["-date"]

    def get_queryset(self):
        queryset = Climatisation.objects.select_related(
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
def clim_form_view(request, exemplaire_id):
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
        form = ClimForm(
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
                with transaction.atomic():

                    clim = form.save(commit=False)

                    # =========================
                    # KILOMÉTRAGE
                    # =========================

                    km = form.cleaned_data.get(
                        "kilometrage_clim"
                    )

                    ancien_kilometrage = (
                            exemplaire.kilometres_chassis or 0
                    )

                    kilometrage_variation = 0

                    if km is not None:

                        km = int(km)

                        if km < ancien_kilometrage:
                            raise ValidationError(
                                _(
                                    "Le kilométrage du contrôle "
                                    "ne peut pas être inférieur au kilométrage "
                                    "actuel du véhicule."
                                )
                            )

                        kilometrage_variation = (
                                km - ancien_kilometrage
                        )

                        # Mise à jour véhicule
                        exemplaire.kilometres_chassis = km

                        exemplaire.save(
                            update_fields=[
                                "kilometres_chassis"
                            ]
                        )

                        # 🔗 checkup UNIQUE
                        clim = form.save(commit=False)
                        clim.assign_technicien(request.user)

                        clim.kilometres_chassis = exemplaire.kilometres_chassis
                        clim.kilometrage_clim = km

                    # ------------------------------------------
                    # Création de la maintenance
                    # ------------------------------------------

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
                            Maintenance.TypeMaintenance.CLIMATISATION
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

                    clim.maintenance = maintenance

                    clim.assign_technicien(request.user)

                    clim.kilometrage_clim = km

                    clim.kilometres_chassis = (
                        ancien_kilometrage
                    )

                    clim.kilometrage_variation = (
                        kilometrage_variation
                    )

                    clim.assign_technicien(
                        request.user
                    )

                    clim.tech_last_maintained_by = (
                        request.user
                    )

                    clim.save()
                    # Nécessaire si le formulaire contient
                    # éventuellement des champs ManyToMany
                    form.save_m2m()

                    UserLog.objects.create(
                        utilisateur=request.user,
                        action=_("Contrôle de la climatisation") + f" - {exemplaire.immatriculation}"
                    )

                messages.success(
                    request,
                    _(
                        "Contrôle du système de climatisation "
                        "enregistré avec succès."
                    ),
                )

                return redirect(
                    "climatisation:clim_list",
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
        clim_instance = Climatisation(
            voiture_exemplaire=exemplaire,
            kilometres_chassis=exemplaire.kilometres_chassis,
        )

        clim_instance.assign_technicien(request.user)

        form = ClimForm(
            instance=clim_instance,
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
            "title": _("Gaz"),
            "icon": "icons/bouteille-de-gaz.png",
            "fields": [
                field
                for field in form
                if "type_gaz" in field.name
                or "autre_type_gaz" in field.name
            ],
        },
        {
            "title": _("Poids du gaz"),
            "icon": "icons/poids-gaz.png",
            "fields": [
                field
                for field in form
                if "poids_gaz" in field.name
            ],
        },
        {
            "title": _("Qualité du gaz"),
            "icon": "icons/qualite-gaz.png",
            "fields": [
                field
                for field in form
                if "qualite_gaz" in field.name
                or "purete_gaz" in field.name
            ],
        },
        {
            "title": _("Huile"),
            "icon": "icons/huile-clim.png",
            "fields": [
                field
                for field in form
                if "ajout_huile" in field.name
            ],
        },
        {
            "title": _("Traceur"),
            "icon": "icons/traceur.png",
            "fields": [
                field
                for field in form
                if "traceur" in field.name
            ],
        },
        {
            "title": _("Mise sous vide"),
            "icon": "icons/mise-vide.png",
            "fields": [
                field
                for field in form
                if field.name in [
                    "mise_sous_vide",
                    "mise_sous_vide_quantite",
                    "mise_sous_vide_prix",
                    "duree_mise_sous_vide_minutes",
                    "pression_vide_atteinte",
                    "tenue_du_vide",
                ]
            ],
        },
        {
            "title": _("Contrôle des fuites"),
            "icon": "icons/fuites.png",
            "fields": [
                field
                for field in form
                if "fuite" in field.name
            ],
        },
        {
            "title": _("Tuyaux"),
            "icon": "icons/tuyaux-clim.png",
            "fields": [
                field
                for field in form
                if "tuyaux" in field.name
            ],
        },
        {
            "title": _("Valves"),
            "icon": "icons/valves-clim.png",
            "fields": [
                field
                for field in form
                if "valves" in field.name
            ],
        },
        {
            "title": _("Déshydrateur"),
            "icon": "icons/deshydrateur.png",
            "fields": [
                field
                for field in form
                if "deshydrateur" in field.name
            ],
        },
        {
            "title": _("Condenseur"),
            "icon": "icons/condenseur.png",
            "fields": [
                field
                for field in form
                if "condenseur" in field.name
            ],
        },
        {
            "title": _("Compresseur"),
            "icon": "icons/compresseur.png",
            "fields": [
                field
                for field in form
                if "compresseur" in field.name
            ],
        },
        {
            "title": _("Évaporateur"),
            "icon": "icons/evaporateur.png",
            "fields": [
                field
                for field in form
                if "evaporateur" in field.name
            ],
        },
        {
            "title": _("Recharge de gaz"),
            "icon": "icons/bouteille-de-gaz.png",
            "fields": [
                field
                for field in form
                if "recharge" in field.name
            ],
        },
        {
            "title": _("Pressions de fonctionnement"),
            "icon": "icons/pression-clim.png",
            "fields": [
                field
                for field in form
                if field.name in [
                    "pression_basse",
                    "pression_haute",
                ]
            ],
        },
        {
            "title": _("Température d'air"),
            "icon": "icons/mesure-clim.png",
            "fields": [
                field
                for field in form
                if "temperature_air" in field.name
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
            "title": _("Étiquette"),
            "icon": "icons/tag.png",
            "fields": [
                field
                for field in form
                if field.name == "tag"
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
        "climatisation/clim_form.html",
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
def clim_detail_view(request, climatisation_id):
    clim = get_object_or_404(
        Climatisation.objects.select_related("voiture_exemplaire"),
        id=climatisation_id
    )

    context = {
        "clim": clim,
        "exemplaire": clim.voiture_exemplaire,
    }
    return render(request, "climatisation/clim_detail.html", context)



@login_required
def modifier_clim_view(request, climatisation_id):
    tenant = request.user.societe



    clim = get_object_or_404(
        Climatisation.objects.select_related("voiture_exemplaire"),
        id=climatisation_id
    )
    exemplaire = clim.voiture_exemplaire
    # -------------------------
    # POST
    # -------------------------
    if request.method == "POST":
        form = ClimForm(
            request.POST,
            instance=clim,
            user=request.user,
            exemplaire=clim.voiture_exemplaire
        )

        if form.is_valid():
            form.save()

            UserLog.objects.create(
                utilisateur=request.user,
                action=_("Modification du contrôle de la  climatisation") + f" - {exemplaire.immatriculation}"
            )

            messages.success(request, _("Contrôle du système de climatisation modifié avec succès !"))
            return redirect("climatisation:clim_detail", climatisation_id=clim.id)
        else:
            messages.error(request, _("Le formulaire contient des erreurs."))
            print(form.errors)

    # -------------------------
    # GET
    # -------------------------
    else:
        form = ClimForm(
            instance=clim,
            user=request.user,
            exemplaire=clim.voiture_exemplaire
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
            "title": _("Gaz"),
            "icon": "icons/bouteille-de-gaz.png",
            "fields": [
                field
                for field in form
                if "type_gaz" in field.name
                or "autre_type_gaz" in field.name
            ],
        },
        {
            "title": _("Poids du gaz"),
            "icon": "icons/poids-gaz.png",
            "fields": [
                field
                for field in form
                if "poids_gaz" in field.name
            ],
        },
        {
            "title": _("Qualité du gaz"),
            "icon": "icons/qualite-gaz.png",
            "fields": [
                field
                for field in form
                if "qualite_gaz" in field.name
                or "purete_gaz" in field.name
            ],
        },
        {
            "title": _("Huile"),
            "icon": "icons/huile-clim.png",
            "fields": [
                field
                for field in form
                if "huile" in field.name
            ],
        },
        {
            "title": _("Traceur"),
            "icon": "icons/traceur.png",
            "fields": [
                field
                for field in form
                if "traceur" in field.name
            ],
        },
        {
            "title": _("Mise sous vide"),
            "icon": "icons/mise-vide.png",
            "fields": [
                field
                for field in form
                if field.name in [
                    "mise_sous_vide",
                    "mise_sous_vide_quantite",
                    "mise_sous_vide_prix",
                    "duree_mise_sous_vide_minutes",
                    "pression_vide_atteinte",
                    "tenue_du_vide",
                ]
            ],
        },
        {
            "title": _("Contrôle des fuites"),
            "icon": "icons/fuites.png",
            "fields": [
                field
                for field in form
                if "fuite" in field.name
            ],
        },
        {
            "title": _("Tuyaux"),
            "icon": "icons/tuyaux-clim.png",
            "fields": [
                field
                for field in form
                if "tuyaux" in field.name
            ],
        },
        {
            "title": _("Valves"),
            "icon": "icons/valves-clim.png",
            "fields": [
                field
                for field in form
                if "valves" in field.name
            ],
        },
        {
            "title": _("Déshydrateur"),
            "icon": "icons/deshydrateur.png",
            "fields": [
                field
                for field in form
                if "deshydrateur" in field.name
            ],
        },
        {
            "title": _("Condenseur"),
            "icon": "icons/condenseur.png",
            "fields": [
                field
                for field in form
                if "condenseur" in field.name
            ],
        },
        {
            "title": _("Compresseur"),
            "icon": "icons/compresseur.png",
            "fields": [
                field
                for field in form
                if "compresseur" in field.name
            ],
        },
        {
            "title": _("Évaporateur"),
            "icon": "icons/evaporateur.png",
            "fields": [
                field
                for field in form
                if "evaporateur" in field.name
            ],
        },

        {
            "title": _("Recharge de gaz"),
            "icon": "icons/bouteille-de-gaz.png",
            "fields": [
                field
                for field in form
                if "recharge" in field.name
            ],
        },

        {
            "title": _("Pressions de fonctionnement"),
            "icon": "icons/pression-clim.png",
            "fields": [
                field
                for field in form
                if field.name in [
                    "pression_basse",
                    "pression_haute",
                ]
            ],
        },
        {
            "title": _("Température d'air"),
            "icon": "icons/mesure-clim.png",
            "fields": [
                field
                for field in form
                if "temperature_air" in field.name
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
        "climatisation/modifier_clim.html",
        {
            "form": form,
            "clim": clim,
            "sections": sections,
            "exemplaire": exemplaire,
        }
    )


@never_cache
@login_required
def clim_detail_pdf_view(request, pk):
    tenant = request.user.societe



    climatisation = get_object_or_404(
        Climatisation.objects.select_related(
            "voiture_exemplaire",
            "maintenance",
            "tech_technicien",
            "tech_societe",
            "main_oeuvre",
            "main_oeuvre__utilisateur",
        ),
        pk=pk,
    )

    rapport = climatisation.generer_rapport_remplacement() or {
        "lignes": [],
        "total_general": 0,
    }

    html_string = render_to_string(
        "climatisation/clim_detail_pdf.html",
        {
            "climatisation": climatisation,
            "rapport": rapport,
            "date_export": timezone.now(),
        },
        request=request,
    )

    pdf = HTML(
        string=html_string,
        base_url=request.build_absolute_uri("/"),
    ).write_pdf()

    # =========================================================
    # IMMATRICULATION
    # =========================================================

    immatriculation = (
        climatisation.voiture_exemplaire.immatriculation
        if climatisation.voiture_exemplaire
        else "sans_immatriculation"
    )

    # =========================================================
    # TECHNICIEN
    # =========================================================

    technicien = (
            climatisation.tech_nom_technicien
            or "technicien_inconnu"
    )

    # Nettoyage pour le nom du fichier
    technicien = str(technicien).replace(" ", "_")
    immatriculation = str(immatriculation).replace(" ", "_")

    # =========================================================
    # DATE
    # =========================================================

    date_pdf = (
        climatisation.date.strftime("%Y-%m-%d")
        if climatisation.date
        else timezone.now().strftime("%Y-%m-%d")
    )

    # =========================================================
    # TITRE / NOM DU PDF
    # =========================================================

    nom_fichier = (
        f"{_('Climatisation')}_{technicien}_{immatriculation}_{date_pdf}.pdf"
    )

    response = HttpResponse(
        pdf,
        content_type="application/pdf",
    )

    response["Content-Disposition"] = (
        f'inline; filename="{nom_fichier}"'
    )

    return response