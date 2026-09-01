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
from maindoeuvre.models import MainDoeuvre
from maintenance.models import Maintenance
from utilisateurs.models import UserLog
from voiture.voiture_exemplaire.models import VoitureExemplaire
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from weasyprint import HTML
from .forms import TurboForm
from .models import Turbo




@method_decorator([login_required, never_cache], name='dispatch')
class TurboListView(ListView):
    model = Turbo
    template_name = "turbo/turbo_list.html"
    context_object_name = "turbos"


    def get_queryset(self):
        queryset = Turbo.objects.select_related(
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
def turbo_check_view(request, exemplaire_id):
    tenant = request.user.societe
    role = request.user.role

    maintenance = None

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
    # Sections disponibles TOUJOURS
    # =========================
    section_templates = [
        {"title": _("Kilométrage"), "icon": "icons/compteur.png", "filter": "kilo"},
        {"title": _("Jeu dans l'axe"), "icon": "icons/turbo.png", "filter": "jeu_axe"},
        {"title": _("État des turbines"), "icon": "icons/turbine.png", "filter": "turbine"},
        {"title": _("Fuites d'huile"), "icon": "icons/fuite-deau.png", "filter": "fuites"},
        {"title": _("Géométrie Variable"), "icon": "icons/turbine.png", "filter": "geometrie"},
        {"title": _("Turbo"), "icon": "icons/turbo.png", "filter": "turbos"},
        {"title": _("Intercooler"), "icon": "icons/intercooler.png", "filter": "intercooler"},
        {"title": _("Electro-vanne"), "icon": "icons/electrovanne.png", "filter": "electrovanne"},
        {"title": _("Joints"), "icon": "icons/joint.png", "filter": "joints"},
        {"title": _("Etiquette"), "icon": "icons/tag.png", "filter": "tag"},
        {"title": _("Pays"), "icon": "icons/pays.png", "filter": "pays"},
        {"title": _("Remarques"), "icon": "icons/notes.png", "filter": "remarques"},
        {"title": _("Technicien"), "icon": "icons/mecanicien.png", "filter": "tech"},
        {"title": _("Taux horaire"), "icon": "icons/taux.png", "filter": "taux"},
    ]

    # =========================
    # POST
    # =========================
    if request.method == "POST":

        form = TurboForm(
            request.POST,
            user=request.user,
            exemplaire=exemplaire
        )

        if form.is_valid():

            try:

                # ==================================================
                # KILOMÉTRAGE
                # ==================================================
                km = form.cleaned_data.get("kilometres_turbo")

                ancien_kilometrage = (
                        exemplaire.kilometres_chassis or 0
                )

                if km is None:
                    form.add_error(
                        "kilometres_turbo",
                        _("Le kilométrage est obligatoire."),
                    )

                else:
                    km = int(km)

                    if km < ancien_kilometrage:
                        form.add_error(
                            "kilometres_turbo",
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
                                societe=request.user.societe,
                                voiture_exemplaire=exemplaire,
                                immatriculation=exemplaire.immatriculation,
                                date_intervention=timezone.now().date(),
                                kilometres_chassis=exemplaire.kilometres_chassis,
                                kilometres_dernier_entretien=exemplaire.kilometres_dernier_entretien,
                                type_maintenance=Maintenance.TypeMaintenance.TURBO,
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

                            turbo = form.save(commit=False)

                            turbo.voiture_exemplaire = exemplaire
                            turbo.maintenance = maintenance

                            # Snapshot AVANT intervention
                            turbo.kilometres_chassis = (
                                ancien_kilometrage
                            )

                            # Kilométrage du contrôle
                            turbo.kilometres_turbo = km

                            # Variation kilométrage
                            turbo.kilometrage_variation = (
                                kilometrage_variation
                            )

                            # ==================================================
                            # TECHNICIEN
                            # ==================================================
                            turbo.assign_technicien(
                                request.user
                            )

                            turbo.tech_last_maintained_by = (
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
                            if turbo.main_oeuvre_id:

                                main_oeuvre = (
                                    turbo.main_oeuvre
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

                                turbo.main_oeuvre = (
                                    main_oeuvre
                                )

                            # ==================================================
                            # SAUVEGARDE turbo
                            # IMPORTANT :
                            # EN DEHORS DU IF/ELSE MAIN-D'ŒUVRE
                            # ==================================================
                            turbo.save()

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

                        UserLog.objects.create(
                                utilisateur=request.user,
                                action=_("Contrôle du Turbo") + f" - {exemplaire.immatriculation}"
                            )

                        messages.success(
                            request,
                            _("Check turbo enregistré avec succès.")
                        )
                        return redirect("turbo:turbo_list", exemplaire_id=exemplaire.id)

            except Exception as e:
                messages.error(request,_(f"Erreur lors de l'enregistrement : {str(e)}")
                )
        else:
            print("FORM INVALID:", form.errors)
            messages.error(request, _("Formulaire invalide"))

    else:

        turbo = Turbo(
            voiture_exemplaire=exemplaire,
            kilometres_chassis=exemplaire.kilometres_chassis
        )

        turbo.assign_technicien(request.user)

        form = TurboForm(
            instance=turbo,
            user=request.user,
            exemplaire=exemplaire
        )

    # =========================
    # Génération sections
    # =========================
    sections = [
        {
            "title": s["title"],
            "icon": s["icon"],
            "fields": [f for f in form if s["filter"] in f.name]
        }
        for s in section_templates
    ]

    return render(request, 'turbo/turbo_check.html', {
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
def turbo_detail_view(request, turbo_id):
    turbo = get_object_or_404(
        Turbo.objects.select_related("voiture_exemplaire"),
        id=turbo_id
    )

    context = {
        "turbo": turbo,
        "exemplaire": turbo.voiture_exemplaire,
    }
    return render(request, "turbo/turbo_detail.html", context)



@login_required
def modifier_turbo_view(request, turbo_id):
    tenant = request.user.societe

    turbo = get_object_or_404(
        Turbo.objects.select_related("voiture_exemplaire"),
        id=turbo_id
    )
    exemplaire = turbo.voiture_exemplaire
    # -------------------------
    # POST
    # -------------------------
    if request.method == "POST":
        form = TurboForm(
            request.POST,
            instance=turbo,
            user=request.user,
            exemplaire=turbo.voiture_exemplaire
        )

        if form.is_valid():
            form.save()

            UserLog.objects.create(
                utilisateur=request.user,
                action=_("Modification du controle du turbo")+ f" - {exemplaire.immatriculation}"
            )

            messages.success(request, _("Contrôle du turbo modifié avec succès !"))
            return redirect("turbo:turbo_detail", turbo_id=turbo.id)
        else:
            messages.error(request, _("Le formulaire contient des erreurs."))
            print(form.errors)

    # -------------------------
    # GET
    # -------------------------
    else:

        form = TurboForm(
            instance=turbo,
            user=request.user,
            exemplaire=turbo.voiture_exemplaire
        )

    # -------------------------
    # Sections pour le template
    # -------------------------
    section_templates = [
        {"title": _("Kilométrage"), "icon": "icons/compteur.png", "filter": "kilo"},
        {"title": _("Jeu dans l'axe"), "icon": "icons/turbo.png", "filter": "jeu_axe"},
        {"title": _("État des turbines"), "icon": "icons/turbine.png", "filter": "turbine"},
        {"title": _("Fuites d'huile"), "icon": "icons/fuite-deau.png", "filter": "fuites"},
        {"title": _("Géométrie Variable"), "icon": "icons/turbine.png", "filter": "geometrie"},
        {"title": _("Turbo"), "icon": "icons/turbo.png", "filter": "turbos"},
        {"title": _("Intercooler"), "icon": "icons/intercooler.png", "filter": "intercooler"},
        {"title": _("Electro-vanne"), "icon": "icons/electrovanne.png", "filter": "electrovanne"},
        {"title": _("joints"), "icon": "icons/joint.png", "filter": "joints"},
        {"title": _("Etiquette"), "icon": "icons/tag.png", "filter": "tag"},
        {"title": _("Pays"), "icon": "icons/pays.png", "filter": "pays"},
        {"title": _("Remarques"), "icon": "icons/notes.png", "filter": "remarques"},
        {"title": _("Technicien"), "icon": "icons/mecanicien.png", "filter": "tech"},
        {"title": _("Taux horaire"), "icon": "icons/taux.png", "filter": "taux"},

    ]

    sections = [
        {
            "title": s["title"],
            "icon": s["icon"],
            "fields": [f for f in form if s["filter"] in f.name]
        }
        for s in section_templates
    ]

    return render(
        request,
        "turbo/modifier_turbo.html",
        {
            "form": form,
            "turbo": turbo,
            "sections": sections,
            "exemplaire": exemplaire,
        }
    )




@login_required
def turbo_detail_pdf_view(request, pk):
    turbo = get_object_or_404(Turbo, pk=pk)

    rapport = turbo.generer_rapport_remplacement()

    html_string = render_to_string(
        "turbo/turbo_detail_pdf.html",
        {
            "turbo": turbo,
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
        turbo.voiture_exemplaire.immatriculation
        if turbo.voiture_exemplaire
        else "sans_immatriculation"
    )

    technicien = turbo.tech_nom_technicien or "technicien_inconnu"

    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = (
        f'attachment; filename="rapport_turbo_{immatriculation}_{technicien}.pdf"'
    )

    return response