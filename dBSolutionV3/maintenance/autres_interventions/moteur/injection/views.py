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
from maintenance.autres_interventions.moteur.injection.forms import InjectionForm
from maintenance.autres_interventions.moteur.injection.models import Injection
from maintenance.models import Maintenance
from utilisateurs.models import UserLog
from voiture.voiture_exemplaire.models import VoitureExemplaire
from django.db.models import Q
from django.utils.translation import gettext_lazy as _, gettext_noop
from django.views.generic import DetailView
from decimal import Decimal
from weasyprint import HTML







@method_decorator([login_required, never_cache], name='dispatch')
class InjectionListView(ListView):
    model = Injection
    template_name = "injection/injection_list.html"
    context_object_name = "injections"
    ordering = ["-id"]

    def get_queryset(self):
        queryset = Injection.objects.select_related(
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
def injection_form_view(request, exemplaire_id):
    tenant = request.user.societe
    role = request.user.role

    maintenance = None

    # ==========================================================
    # EXEMPLAIRE
    # ==========================================================

    exemplaire = get_object_or_404(
        VoitureExemplaire.objects.filter(
            Q(client__societe=tenant)
            | Q(client__isnull=True, societe=tenant)
        ),
        id=exemplaire_id,
    )

    # ==========================================================
    # RÔLES AUTORISÉS
    # ==========================================================

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

    # ==========================================================
    # POST
    # ==========================================================

    if request.method == "POST":

        injection = Injection(
            voiture_exemplaire=exemplaire,
            kilometres_chassis=exemplaire.kilometres_chassis or 0,
        )

        injection.assign_technicien(request.user)

        form = InjectionForm(
            request.POST,
            instance=injection,
            user=request.user,
            exemplaire=exemplaire,
        )

        if form.is_valid():

            try:

                # ==================================================
                # KILOMÉTRAGE
                # ==================================================
                km = form.cleaned_data.get("kilometrage_injection")

                ancien_kilometrage = (
                        exemplaire.kilometres_chassis or 0
                )

                if km is None:
                    form.add_error(
                        "kilometrage_injection",
                        _("Le kilométrage est obligatoire."),
                    )

                else:
                    km = int(km)

                    if km < ancien_kilometrage:
                        form.add_error(
                            "kilometrage_injection",
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

                            # ==================================================
                            # MAINTENANCE
                            # ==================================================

                            maintenance = Maintenance.objects.create(
                                societe=tenant,
                                voiture_exemplaire=exemplaire,
                                immatriculation=exemplaire.immatriculation,
                                date_intervention=timezone.now().date(),
                                kilometres_chassis=(
                                    exemplaire.kilometres_chassis or 0
                                ),
                                kilometres_dernier_entretien=(
                                    exemplaire.kilometres_dernier_entretien
                                ),
                                type_maintenance=(
                                    Maintenance.TypeMaintenance.INJECTION
                                ),
                                tag=Maintenance.Tag.JAUNE,
                            )

                            # ==================================================
                            # RÔLE DANS MAINTENANCE
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

                            # M2M : après sauvegarde de Maintenance
                            if role == "apprenti":
                                maintenance.apprentis.add(request.user)

                            injection = form.save(commit=False)

                            injection.voiture_exemplaire = exemplaire
                            injection.maintenance = maintenance

                            # Snapshot AVANT intervention
                            injection.kilometres_chassis = (
                                ancien_kilometrage
                            )

                            # Kilométrage du contrôle
                            injection.kilometrage_injection = km

                            # Variation kilométrage
                            injection.kilometrage_variation = (
                                kilometrage_variation
                            )

                            # ==================================================
                            # TECHNICIEN
                            # ==================================================
                            injection.assign_technicien(
                                request.user
                            )

                            injection.tech_last_maintained_by = (
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
                            if injection.main_oeuvre_id:

                                main_oeuvre = (
                                    injection.main_oeuvre
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

                                injection.main_oeuvre = (
                                    main_oeuvre
                                )

                            # ==================================================
                            # SAUVEGARDE injection
                            # IMPORTANT :
                            # EN DEHORS DU IF/ELSE MAIN-D'ŒUVRE
                            # ==================================================
                            injection.save()

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

                            # ==================================================
                            # LOG
                            # ==================================================



                            ACTION_SYSTEME_INJECTION = gettext_noop(
                                "Système d'injection"
                            )

                            UserLog.objects.create(
                                utilisateur=request.user,
                                action=f"{ACTION_SYSTEME_INJECTION} - {exemplaire.immatriculation}"
                            )
                    messages.success(
                        request,
                        _(
                            "Check du système d'injection "
                            "enregistré avec succès."
                        ),
                    )

                    return redirect(
                        "injection:injection_list",
                        exemplaire_id=exemplaire.id,
                    )

            except ValueError as e:
                messages.error(
                    request,
                    str(e),
                )

            except Exception as e:
                messages.error(
                    request,
                    _("Erreur lors de l'enregistrement : %(erreur)s")
                    % {
                        "erreur": str(e)
                    },
                )

        else:
            messages.error(
                request,
                _("Le formulaire contient des erreurs."),
            )

            print(form.errors)

    # ==========================================================
    # GET
    # ==========================================================

    else:

        injection = Injection(
            voiture_exemplaire=exemplaire,
            kilometres_chassis=(
                exemplaire.kilometres_chassis or 0
            ),
        )

        injection.assign_technicien(request.user)

        form = InjectionForm(
            instance=injection,
            user=request.user,
            exemplaire=exemplaire,
        )

    # ==========================================================
    # SECTIONS FORMULAIRE
    # ==========================================================

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
            "title": _("Type de carburant"),
            "icon": "icons/pompe-type.png",
            "fields": [
                form[f.name]
                for f in form
                if f.name == "type_carburant"
            ],
        },
        {
            "title": _("Pompe à carburant"),
            "icon": "icons/pompe-a-carburant.png",
            "fields": [
                form[f.name]
                for f in form
                if f.name.startswith("pompe_carburant")
            ],
        },
        {
            "title": _("Pompe haute pression"),
            "icon": "icons/pompe-haute-pression.png",
            "fields": [
                form[f.name]
                for f in form
                if f.name.startswith("pompe_haute_pression")
            ],
        },
        {
            "title": _("Rampe d'injection"),
            "icon": "icons/rampe-injection.png",
            "fields": [
                form[f.name]
                for f in form
                if f.name.startswith("rampe_injection")
            ],
        },
        {
            "title": _("Capteur de pression de rampe"),
            "icon": "icons/capteur-pression.png",
            "fields": [
                form[f.name]
                for f in form
                if (
                        f.name.startswith("capteur_pression_rampe")
                        or f.name == "pression_rampe_bar"
                )
            ],
        },
        {
            "title": _("Tuyaux haute pression"),
            "icon": "icons/tuyaux-haute-pression.png",
            "fields": [
                form[f.name]
                for f in form
                if f.name.startswith("tuyaux_haute_pression")
            ],
        },
        {
            "title": _("Injecteurs"),
            "icon": "icons/injecteurs.png",
            "fields": [
                form[f.name]
                for f in form
                if (
                        f.name.startswith("injecteurs_")
                        or f.name == "nombre_injecteurs"
                )
            ],
        },
        {
            "title": _("Résistance des injecteurs"),
            "icon": "icons/resistance-injecteur.png",
            "fields": [
                form[f.name]
                for f in form
                if (
                        f.name.startswith("injecteur_")
                        and f.name.endswith("_resistance_ohm")
                )
            ],
        },
        {
            "title": _("Nettoyage des injecteurs"),
            "icon": "icons/nettoyage-injecteurs.png",
            "fields": [
                form[f.name]
                for f in form
                if f.name.startswith("nettoyage_injecteurs")
            ],
        },
        {
            "title": _("Connecteurs d'injecteurs"),
            "icon": "icons/connecteur-injecteur.png",
            "fields": [
                form[f.name]
                for f in form
                if f.name.startswith("connecteurs_injecteurs")
            ],
        },
        {
            "title": _("Diagnostic"),
            "icon": "icons/diagnostic.png",
            "fields": [
                form[f.name]
                for f in form
                if f.name in [
                    "diagnostic_effectue",
                    "code_defaut",
                    "resultat_diagnostic",
                ]
            ],
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


    # ==========================================================
    # RENDER
    # ==========================================================

    return render(
        request,
        "injection/injection_form.html",
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
# Vue détail courroie
# -----------------------------
@login_required
def injection_detail_view(request, injection_id):
    injection = get_object_or_404(
        Injection.objects.select_related("voiture_exemplaire"),
        id=injection_id
    )

    context = {
        "injection": injection,
        "exemplaire": injection.voiture_exemplaire,
    }
    return render(request, "injection/injection_detail.html", context)



@login_required
def modifier_injection_view(request, injection_id):
    tenant = request.user.societe

    injection = get_object_or_404(
        Injection.objects.select_related("voiture_exemplaire"),
        id=injection_id
    )
    exemplaire = injection.voiture_exemplaire
    # -------------------------
    # POST
    # -------------------------
    if request.method == "POST":
        form = InjectionForm(
            request.POST,
            instance=injection,
            user=request.user,
            exemplaire=injection.voiture_exemplaire
        )

        if form.is_valid():
            try:
                injection = form.save(commit=False)

                # 🔧 Réaffectation technicien + société
                injection.assign_technicien(request.user)

                injection.save()

                from django.utils.translation import gettext_noop

                ACTION_MODIFICATION_CONTROLE_INJECTION = gettext_noop(
                    "Modification du contrôle de l'injection"
                )

                UserLog.objects.create(
                    utilisateur=request.user,
                    action=f"{ACTION_MODIFICATION_CONTROLE_INJECTION} - {exemplaire.immatriculation}"
                )

                messages.success(
                    request,
                    _("Contrôle de l'injection modifié avec succès !")
                )
                return redirect(
                    "injection:injection_detail",
                    injection_id=injection.id
                )

            except ValidationError as e:
                form.add_error(None, e)
                messages.error(request, _("Kilométrage invalide"))

        else:
            messages.error(request, _("Le formulaire contient des erreurs."))
            print(form.errors)

    # -------------------------
    # GET
    # -------------------------
    else:
        form = InjectionForm(
            instance=injection,
            user=request.user,
            exemplaire=injection.voiture_exemplaire
        )

    # -------------------------
    # Sections pour le template
    # -------------------------
    # --- Génération des champs par section ---
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
            "title": _("Type de carburant"),
            "icon": "icons/pompe-type.png",
            "fields": [
                form[f.name]
                for f in form
                if f.name == "type_carburant"
            ],
        },
        {
            "title": _("Pompe à carburant"),
            "icon": "icons/pompe-a-carburant.png",
            "fields": [
                form[f.name]
                for f in form
                if f.name.startswith("pompe_carburant")
            ],
        },
        {
            "title": _("Pompe haute pression"),
            "icon": "icons/pompe-haute-pression.png",
            "fields": [
                form[f.name]
                for f in form
                if f.name.startswith("pompe_haute_pression")
            ],
        },
        {
            "title": _("Rampe d'injection"),
            "icon": "icons/rampe-injection.png",
            "fields": [
                form[f.name]
                for f in form
                if f.name.startswith("rampe_injection")
            ],
        },
        {
            "title": _("Capteur de pression de rampe"),
            "icon": "icons/capteur-pression.png",
            "fields": [
                form[f.name]
                for f in form
                if (
                        f.name.startswith("capteur_pression_rampe")
                        or f.name == "pression_rampe_bar"
                )
            ],
        },
        {
            "title": _("Tuyaux haute pression"),
            "icon": "icons/tuyaux-haute-pression.png",
            "fields": [
                form[f.name]
                for f in form
                if f.name.startswith("tuyaux_haute_pression")
            ],
        },
        {
            "title": _("Injecteurs"),
            "icon": "icons/injecteurs.png",
            "fields": [
                form[f.name]
                for f in form
                if (
                        f.name.startswith("injecteurs_")
                        or f.name == "nombre_injecteurs"
                )
            ],
        },
        {
            "title": _("Résistance des injecteurs"),
            "icon": "icons/resistance-injecteur.png",
            "fields": [
                form[f.name]
                for f in form
                if (
                        f.name.startswith("injecteur_")
                        and f.name.endswith("_resistance_ohm")
                )
            ],
        },
        {
            "title": _("Nettoyage des injecteurs"),
            "icon": "icons/nettoyage-injecteurs.png",
            "fields": [
                form[f.name]
                for f in form
                if f.name.startswith("nettoyage_injecteurs")
            ],
        },
        {
            "title": _("Connecteurs d'injecteurs"),
            "icon": "icons/connecteur-injecteur.png",
            "fields": [
                form[f.name]
                for f in form
                if f.name.startswith("connecteurs_injecteurs")
            ],
        },
        {
            "title": _("Diagnostic"),
            "icon": "icons/diagnostic.png",
            "fields": [
                form[f.name]
                for f in form
                if f.name in [
                    "diagnostic_effectue",
                    "code_defaut",
                    "resultat_diagnostic",
                ]
            ],
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
        "injection/modifier_injection.html",
        {
            "form": form,
            "injection": injection,
            "sections": sections,
            "exemplaire": exemplaire,
        }
    )


@login_required
def rapport_injection_view(request, pk):
    obj = get_object_or_404(Injection, pk=pk)

    rapport = obj.generer_rapport_remplacement()

    return render(request, "injection/rapport_injection.html", {
        "rapport": rapport,
        "obj": obj
    })





class InjectionRapportDetailView(DetailView):
    model = Injection
    template_name = "injection/rapport_pdf_injection.html"
    context_object_name = "obj"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        obj = self.object

        rapport = obj.generer_rapport_remplacement()

        if not rapport:
            rapport = {"lignes": [], "total_general": Decimal("0")}

        # 🔥 AJOUT DU TAUX TVA DANS CHAQUE LIGNE
        taux_tva = obj.TVA_PIECES.get(obj.pays, 0)

        for ligne in rapport["lignes"]:
            ligne["taux_tva"] = taux_tva

        context["rapport"] = rapport

        return context




@login_required
def injection_detail_pdf_view(request, pk):
    injection = get_object_or_404(Injection, pk=pk)

    rapport = injection.generer_rapport_remplacement()

    html_string = render_to_string(
        "injection/injection_detail_pdf.html",
        {
            "injection": injection,
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
        injection.voiture_exemplaire.immatriculation
        if injection.voiture_exemplaire
        else "sans_immatriculation"
    )

    # =========================================================
    # TECHNICIEN
    # =========================================================

    technicien = (
            injection.tech_nom_technicien
            or "technicien_inconnu"
    )

    # Nettoyage pour le nom du fichier
    technicien = str(technicien).replace(" ", "_")
    immatriculation = str(immatriculation).replace(" ", "_")

    # =========================================================
    # DATE
    # =========================================================

    date_pdf = (
        injection.date.strftime("%Y-%m-%d")
        if injection.date
        else timezone.now().strftime("%Y-%m-%d")
    )

    # =========================================================
    # TITRE / NOM DU PDF
    # =========================================================

    nom_fichier = (
        f"{_('Injection')}_{technicien}_{immatriculation}_{date_pdf}.pdf"
    )

    response = HttpResponse(
        pdf,
        content_type="application/pdf",
    )

    response["Content-Disposition"] = (
        f'inline; filename="{nom_fichier}"'
    )

    return response
