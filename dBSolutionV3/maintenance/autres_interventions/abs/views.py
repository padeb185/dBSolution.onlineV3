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
from maintenance.models import Maintenance
from utilisateurs.models import UserLog
from voiture.voiture_exemplaire.models import VoitureExemplaire
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from decimal import Decimal
from weasyprint import HTML
from .forms import AbsForm
from .models import Abs
from ...checkup_track.models import EtatOKNotOK


@method_decorator([login_required, never_cache], name='dispatch')
class AbsListView(ListView):
    model = Abs
    template_name = "abs/abs_list.html"
    context_object_name = "abss"
    paginate_by = 10
    ordering = ["-id"]

    def get_queryset(self):
        queryset = Abs.objects.select_related(
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
def abs_form_view(request, exemplaire_id):

    tenant = request.user.societe
    role = request.user.role

    maintenance = None  # 👈 important pour éviter UnboundLocalError



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
        form = AbsForm(
            request.POST,
            user=request.user,
            exemplaire=exemplaire
        )

        if form.is_valid():

            try:
                with transaction.atomic():

                    abs = form.save(commit=False)

                    # =========================
                    # KILOMÉTRAGE
                    # =========================

                    km = form.cleaned_data.get(
                        "kilometrage_abs"
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
                                    "Le kilométrage du contrôle du système ABS "
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

                    # 🔴 maintenance unique
                    maintenance = Maintenance.objects.create(
                        societe=request.user.societe,
                        voiture_exemplaire=exemplaire,
                        immatriculation=exemplaire.immatriculation,
                        date_intervention=timezone.now().date(),
                        kilometres_chassis=exemplaire.kilometres_chassis,
                        kilometres_dernier_entretien=exemplaire.kilometres_dernier_entretien,
                        type_maintenance=Maintenance.TypeMaintenance.ABS,
                        tag=Maintenance.Tag.JAUNE,
                    )

                    # 🔧 affectation rôle
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

                    abs.assign_technicien(request.user)

                    abs.kilometrage_abs = km

                    abs.kilometres_chassis = (
                        ancien_kilometrage
                    )

                    abs.kilometrage_variation = (
                        kilometrage_variation
                    )

                    abs.assign_technicien(
                        request.user
                    )

                    abs.tech_last_maintained_by = (
                        request.user
                    )

                    abs.save()

                    UserLog.objects.create(
                        utilisateur=request.user,
                        action=_("Contrôle ABS - %(immatriculation)s") % {
                            "immatriculation": exemplaire.immatriculation
                        }
                    )

                messages.success(request, _("Contrôle du système ABS enregistré avec succès."))
                return redirect(
                    "abs:abs_list",
                    exemplaire_id=exemplaire.id,
                )

            except Exception as e:
                messages.error(request, _(f"Erreur lors de l'enregistrement : {str(e)}"))

        else:
            messages.error(request, _("Le formulaire contient des erreurs."))
    else:
        Abs_qs = Abs(
            voiture_exemplaire=exemplaire,
            kilometres_chassis=exemplaire.kilometres_chassis
        )
        Abs_qs.assign_technicien(request.user)


        form = AbsForm(
            instance=Abs_qs,
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
            "title": _("Pompe du système ABS"),
            "icon": "icons/abs.png",
            "fields": [form[f.name] for f in form if "pompe" in f.name],
        },
        {
            "title": _("Calculateur ABS"),
            "icon": "icons/calculateur.png",
            "fields": [form[f.name] for f in form if "calculateur" in f.name],
        },
        {
            "title": _("Capteur ABS"),
            "icon": "icons/capteurs.png",
            "fields": [form[f.name] for f in form if "capteur" in f.name],
        },
        {
            "title": _("Liquide de frein"),
            "icon": "icons/liquide_frein.png",
            "fields": [form[f.name] for f in form if "liquide" in f.name],
        },
        {
            "title": _("Serrage des roues"),
            "icon": "icons/roue.png",
            "fields": [form[f.name] for f in form if "serrage" in f.name],
        },
        {
            "title": _("Pays"),
            "icon": "icons/pays.png",
            "fields": [form[f.name] for f in form if "pays" in f.name],
        },
        {
            "title": _("Etiquette"),
            "icon": "icons/tag.png",
            "fields": [form[f.name] for f in form if "tag" in f.name],
        },

        {
            "title": _("Remarques"),
            "icon": "icons/notes.png",
            "fields": [form[f.name] for f in form if "remarques" in f.name],
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

    return render(request, 'abs/abs_form.html', {
        "exemplaire": exemplaire,
        "immatriculation": exemplaire.immatriculation,
        "maintenance": maintenance,
        "form": form,
        "sections": sections,
        "now": timezone.now(),
    })


# ------------
# Vue détail boite
# -----------------------------
@login_required
def abs_detail_view(request, abs_id):
    abs = get_object_or_404(
        Abs.objects.select_related("voiture_exemplaire"),
        id=abs_id
    )

    context = {
        "abs": abs,
        "exemplaire": abs.voiture_exemplaire,
    }
    return render(request, "abs/abs_detail.html", context)



@login_required
def modifier_abs_view(request, abs_id):

    tenant = request.user.societe

    abs = get_object_or_404(
        Abs.objects.select_related(
            "voiture_exemplaire"
        ),
        id=abs_id
    )

    exemplaire = abs.voiture_exemplaire

    # =========================
    # POST
    # =========================
    if request.method == "POST":

        form = AbsForm(
            request.POST,
            instance=abs,
            user=request.user,
            exemplaire=exemplaire
        )

        if form.is_valid():

            try:
                with transaction.atomic():

                    abs = form.save(commit=False)

                    # =========================
                    # KILOMÉTRAGE
                    # =========================
                    km = form.cleaned_data.get(
                        "kilometrage_abs"
                    )

                    # Snapshot enregistré lors
                    # de la création de l'intervention
                    ancien_kilometrage = (
                        abs.kilometres_chassis or 0
                    )

                    kilometrage_variation = 0

                    if km is not None:

                        km = int(km)

                        if km < ancien_kilometrage:
                            raise ValidationError(
                                _(
                                    "Le kilométrage du contrôle ABS "
                                    "ne peut pas être inférieur au kilométrage "
                                    "enregistré avant l'intervention."
                                )
                            )

                        kilometrage_variation = (
                            km - ancien_kilometrage
                        )

                    # =========================
                    # ABS
                    # =========================

                    # Kilométrage corrigé de l'intervention
                    abs.kilometrage_abs = km

                    # On conserve le snapshot d'origine
                    abs.kilometres_chassis = (
                        ancien_kilometrage
                    )

                    # Recalcul de la variation
                    abs.kilometrage_variation = (
                        kilometrage_variation
                    )

                    # Technicien
                    abs.assign_technicien(
                        request.user
                    )

                    abs.tech_last_maintained_by = (
                        request.user
                    )

                    abs.save()

                    # =========================
                    # LOG
                    # =========================
                    UserLog.objects.create(
                        utilisateur=request.user,
                        action=_(
                            "Modification contrôle ABS - %(immatriculation)s"
                        ) % {
                            "immatriculation": (
                                exemplaire.immatriculation
                            )
                        }
                    )

                messages.success(
                    request,
                    _(
                        "Contrôle du système ABS modifié avec succès !"
                    )
                )

                return redirect(
                    "abs:abs_detail",
                    abs_id=abs.id
                )

            except ValidationError as e:

                form.add_error(
                    "kilometrage_abs",
                    e
                )

                messages.error(
                    request,
                    _("Kilométrage invalide.")
                )

            except Exception as e:

                messages.error(
                    request,
                    _("Erreur lors de la modification : %(error)s") % {
                        "error": str(e)
                    }
                )

        else:

            messages.error(
                request,
                _("Le formulaire contient des erreurs.")
            )

            print(form.errors)

    # =========================
    # GET
    # =========================
    else:

        form = AbsForm(
            instance=abs,
            user=request.user,
            exemplaire=exemplaire
        )

    # =========================
    # SECTIONS TEMPLATE
    # =========================
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
            "title": _("Pompe du système ABS"),
            "icon": "icons/abs.png",
            "fields": [
                form[f.name]
                for f in form
                if "pompe" in f.name
            ],
        },
        {
            "title": _("Calculateur ABS"),
            "icon": "icons/calculateur.png",
            "fields": [
                form[f.name]
                for f in form
                if "calculateur" in f.name
            ],
        },
        {
            "title": _("Capteur ABS"),
            "icon": "icons/capteurs.png",
            "fields": [
                form[f.name]
                for f in form
                if "capteur" in f.name
            ],
        },
        {
            "title": _("Liquide de frein"),
            "icon": "icons/liquide_frein.png",
            "fields": [
                form[f.name]
                for f in form
                if "liquide" in f.name
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
            "title": _("Pays"),
            "icon": "icons/pays.png",
            "fields": [
                form[f.name]
                for f in form
                if "pays" in f.name
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
            "title": _("Remarques"),
            "icon": "icons/notes.png",
            "fields": [
                form[f.name]
                for f in form
                if "remarques" in f.name
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
        "abs/modifier_abs.html",
        {
            "form": form,
            "abs": abs,
            "sections": sections,
            "exemplaire": exemplaire,
        }
    )


@login_required
def abs_detail_pdf_view(request, pk):
    abs_obj = get_object_or_404(
        Abs.objects.select_related(
            "maintenance",
            "maintenance__voiture_exemplaire",
            "maintenance__tech_technicien",
            "maintenance__tech_societe",
        ),
        pk=pk,
    )

    rapport = abs_obj.generer_rapport_remplacement()

    maintenance = getattr(abs_obj, "maintenance", None)

    vehicule = None
    technicien = None
    date_intervention = None

    if maintenance:
        vehicule = maintenance.voiture_exemplaire
        technicien = maintenance.tech_technicien
        date_intervention = maintenance.date_intervention

    # Sécurités si certaines relations ne sont pas renseignées
    if vehicule is None:
        vehicule = getattr(abs_obj, "voiture_exemplaire", None)

    if technicien is None:
        technicien = getattr(abs_obj, "tech_technicien", None)

    immatriculation = (
        vehicule.immatriculation
        if vehicule
        else "sans_immatriculation"
    )

    nom_technicien = "technicien_inconnu"

    if technicien:
        prenom = getattr(technicien, "prenom", "") or ""
        nom = getattr(technicien, "nom", "") or ""

        nom_technicien = (
            f"{prenom} {nom}".strip()
            or getattr(technicien, "username", None)
            or str(technicien)
        )

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

    html_string = render_to_string(
        "abs/abs_detail_pdf.html",
        {
            "abs": abs_obj,
            "rapport": rapport,
            "maintenance": maintenance,
            "technicien": technicien,
            "date_intervention": date_intervention,
            "vehicule": vehicule,
            "immatriculation": immatriculation,
            "date_export": datetime.now(),
            "societe": getattr(request.user, "societe", None),
        },
        request=request,
    )

    pdf = HTML(
        string=html_string,
        base_url=request.build_absolute_uri("/"),
    ).write_pdf()

    filename = (
        f"rapport_ABS_"
        f"{immatriculation_fichier}_"
        f"{nom_technicien_fichier}.pdf"
    )

    response = HttpResponse(
        pdf,
        content_type="application/pdf",
    )

    response["Content-Disposition"] = (
        f'attachment; filename="{filename}"'
    )

    return response

    # -------------------------
    # RAPPORT
    # -------------------------
def generer_rapport_remplacement(self):
    rapport = []
    total_general = Decimal("0")

    pieces = [
        "pompe_abs",
        "calculateur_abs",
        "capteur_abs",
    ]

    for field_name in pieces:
        valeur = getattr(self, field_name)

        if valeur == EtatOKNotOK.NOT_OK:
            prix = getattr(self, f"{field_name}_prix", Decimal("0"))
            quantite = getattr(self, f"{field_name}_quantite", 0)

            total = prix * quantite
            total_general += total

            rapport.append({
                "champ": self._meta.get_field(field_name).verbose_name,
                "code": field_name,
                "prix": prix,
                "quantite": quantite,
                "total": total,
            })

    return {
        "lignes": rapport,
        "total_general": total_general
    }