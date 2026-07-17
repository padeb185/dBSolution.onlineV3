from datetime import datetime
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
from django_tenants.utils import tenant_context
from maintenance.models import Maintenance
from utilisateurs.models import UserLog
from voiture.voiture_exemplaire.models import VoitureExemplaire
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
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

    with tenant_context(tenant):

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
                    with transaction.atomic():

                        controle_alternateur = form.save(commit=False)

                        km = form.cleaned_data.get("kilometrage_alte")

                        if km is not None:
                            km = int(km)
                            ancien_km = exemplaire.kilometres_chassis or 0

                            if km < ancien_km:
                                form.add_error(
                                    "kilometrage_alte",
                                    _(
                                        "Le kilométrage ne peut pas diminuer."
                                    ),
                                )

                                raise ValueError(
                                    "kilometrage_invalide"
                                )

                            exemplaire.kilometres_chassis = km
                            exemplaire.date_derniere_intervention = (
                                timezone.now().date()
                            )

                            exemplaire.update_kilometres()
                            exemplaire.save()

                        # Liaison avec le véhicule
                        controle_alternateur.voiture_exemplaire = exemplaire
                        controle_alternateur.kilometres_chassis = (
                            exemplaire.kilometres_chassis
                        )

                        if km is not None:
                            controle_alternateur.kilometrage_alte = km

                        # ==================================================
                        # MAINTENANCE
                        # ==================================================
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
                                Maintenance.TypeMaintenance.ALTERNATEUR
                            ),
                            tag=Maintenance.Tag.JAUNE,
                        )

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
                        controle_alternateur.maintenance = maintenance
                        controle_alternateur.assign_technicien(
                            request.user
                        )
                        controle_alternateur.save()

                        form.save_m2m()

                        UserLog.objects.create(
                            utilisateur=request.user,
                            action=_(
                                "Alternateur - %(immatriculation)s"
                            )
                            % {
                                "immatriculation": (
                                    exemplaire.immatriculation
                                )
                            },
                        )

                    messages.success(
                        request,
                        _(
                            "Check alternateur enregistré avec succès."
                        ),
                    )

                    return redirect(
                        "alternateur:alternateur_detail",
                        controle_alternateur.pk,
                    )

                except ValueError as erreur:
                    if str(erreur) != "kilometrage_invalide":
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

                print(form.errors)

        # ==================================================
        # GET
        # ==================================================
        else:
            controle_alternateur_initial = Alternateur(
                voiture_exemplaire=exemplaire,
                kilometres_chassis=exemplaire.kilometres_chassis,
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
                "icon": "icons/mecanicien.png",
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

    with tenant_context(tenant):
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
                form.save()

                UserLog.objects.create(
                    utilisateur=request.user,
                    action=_("Modification alternateur - %(immatriculation)s") % {
                        "immatriculation": exemplaire.immatriculation
                    }
                )

                messages.success(request, _("Contrôle de l'alternateur modifié avec succès !"))
                return redirect("alternateur:modifier_alternateur", alternateur_id=alternateur.id)
            else:
                messages.error(request, _("Le formulaire contient des erreurs."))
                print(form.errors)

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
                "title": _("Technicien"),
                "icon": "icons/mecanicien.png",
                "fields": [form[f.name] for f in form if "tech" in f.name],
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

    immatriculation = (
        alternateur.voiture_exemplaire.immatriculation
        if alternateur.voiture_exemplaire
        else "sans_immatriculation"
    )

    technicien = alternateur.tech_nom_technicien or "technicien_inconnu"

    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = (
        f'attachment; filename="rapport_alternateur_{immatriculation}_{technicien}.pdf"'
    )

    return response