from decimal import Decimal, ROUND_HALF_UP
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils import timezone
from django.contrib import messages
from django.db import transaction
from maindoeuvre.models import MainDoeuvre
from maintenance.models import Maintenance
from utilisateurs.models import UserLog
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from weasyprint import HTML
from .forms import AdmissionForm
from django.contrib.auth.decorators import login_required
from django.db import models
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import ListView
from voiture.voiture_exemplaire.models import VoitureExemplaire
from .models import Admission





@method_decorator([login_required, never_cache], name="dispatch")
class AdmissionListView(ListView):
    model = Admission
    template_name = "admission/admission_list.html"
    context_object_name = "admissions"
    ordering = ["-date"]

    def get_queryset(self):
        queryset = Admission.objects.select_related(
            "voiture_exemplaire",
            "maintenance",
            "tech_societe",
        )

        societe = getattr(self.request.user, "societe", None)

        if societe:
            queryset = queryset.filter(
                models.Q(tech_societe=societe)
                | models.Q(tech_societe__isnull=True)
            )

        return queryset.order_by("-date")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        exemplaire_id = self.kwargs.get("exemplaire_id")

        if exemplaire_id:
            context["exemplaire"] = VoitureExemplaire.objects.get(
                id=exemplaire_id
            )

        roles_autorises = [
            "mecanicien",
            "apprenti",
            "magasinier",
            "chef_mecanicien",
            "direction",
        ]

        context["is_checkup_allowed"] = (
            self.request.user.role in roles_autorises
        )

        return context





@never_cache
@login_required
def admission_check_view(request, exemplaire_id):

    tenant = request.user.societe
    role = request.user.role

    maintenance = None
    admission = None

    # =========================================================
    # RÉCUPÉRATION DE L'EXEMPLAIRE
    # =========================================================
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

    # =========================================================
    # RÔLES AUTORISÉS
    # =========================================================
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

    # =========================================================
    # POST
    # =========================================================
    if request.method == "POST":

        # Instance liée au véhicule AVANT le formulaire
        admission_instance = Admission(
            voiture_exemplaire=exemplaire,
            kilometres_chassis=(
                exemplaire.kilometres_chassis
            ),
        )

        admission_instance.assign_technicien(
            request.user
        )

        form = AdmissionForm(
            request.POST,
            instance=admission_instance,
            user=request.user,
            exemplaire=exemplaire,
        )

        if form.is_valid():

            try:
                # =================================================
                # KILOMÉTRAGE
                # =================================================
                km = form.cleaned_data.get(
                    "kilometrage_admission"
                )

                ancien_kilometrage = (
                    exemplaire.kilometres_chassis
                    or 0
                )

                if km is None:
                    form.add_error(
                        "kilometrage_admission",
                        _(
                            "Le kilométrage est obligatoire."
                        ),
                    )

                else:
                    km = int(km)

                    if km < ancien_kilometrage:
                        form.add_error(
                            "kilometrage_admission",
                            _(
                                "Le kilométrage du contrôle "
                                "de l'admission ne peut pas être "
                                "inférieur au kilométrage actuel "
                                "du véhicule."
                            ),
                        )

                    else:
                        kilometrage_variation = (
                            km - ancien_kilometrage
                        )

                        # =========================================
                        # TRANSACTION
                        # =========================================
                        with transaction.atomic():

                            # =====================================
                            # MAINTENANCE
                            # =====================================
                            maintenance = (
                                Maintenance.objects.create(
                                    societe=tenant,
                                    voiture_exemplaire=exemplaire,
                                    immatriculation=(
                                        exemplaire.immatriculation
                                    ),
                                    date_intervention=(
                                        timezone.localdate()
                                    ),
                                    kilometres_chassis=km,
                                    kilometres_dernier_entretien=(
                                        exemplaire
                                        .kilometres_dernier_entretien
                                        or 0
                                    ),
                                    type_maintenance=(
                                        Maintenance
                                        .TypeMaintenance
                                        .ADMISSION
                                    ),
                                    tag=(
                                        Maintenance.Tag.JAUNE
                                    ),
                                )
                            )

                            # =====================================
                            # PERSONNEL
                            # =====================================
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

                            # Maintenance déjà créée par
                            # objects.create(), mais nécessaire
                            # après modification du personnel.
                            maintenance.save()

                            # ManyToMany APRÈS sauvegarde
                            if role == "apprenti":
                                maintenance.apprentis.add(
                                    request.user
                                )

                            # =====================================
                            # ADMISSION
                            # =====================================
                            admission = form.save(
                                commit=False
                            )

                            admission.voiture_exemplaire = (
                                exemplaire
                            )

                            admission.maintenance = (
                                maintenance
                            )

                            # Snapshot AVANT intervention
                            admission.kilometres_chassis = (
                                ancien_kilometrage
                            )

                            # Kilométrage du contrôle
                            admission.kilometrage_admission = (
                                km
                            )

                            # Variation
                            admission.kilometrage_variation = (
                                kilometrage_variation
                            )

                            admission.assign_technicien(
                                request.user
                            )

                            admission.tech_last_maintained_by = (
                                request.user
                            )

                            # =====================================
                            # MAIN D'ŒUVRE
                            # =====================================
                            heures = (
                                form.cleaned_data.get(
                                    "temps_heures"
                                )
                                or 0
                            )

                            minutes = (
                                form.cleaned_data.get(
                                    "temps_minutes"
                                )
                                or 0
                            )

                            total_minutes = (
                                heures * 60
                                + minutes
                            )

                            taux_horaire = (
                                form.cleaned_data.get(
                                    "taux_horaire"
                                )
                                or 0
                            )

                            if admission.main_oeuvre_id:

                                main_oeuvre = (
                                    admission.main_oeuvre
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

                            else:
                                main_oeuvre = (
                                    MainDoeuvre.objects.create(
                                        utilisateur=request.user,
                                        temps_minutes=(
                                            total_minutes
                                        ),
                                        taux_horaire=(
                                            taux_horaire
                                        ),
                                    )
                                )

                                admission.main_oeuvre = (
                                    main_oeuvre
                                )

                            # =====================================
                            # SAUVEGARDE ADMISSION
                            # =====================================
                            admission.save()

                            form.save_m2m()

                            # =====================================
                            # MISE À JOUR DU VÉHICULE
                            # =====================================
                            exemplaire.kilometres_chassis = (
                                km
                            )

                            exemplaire.save(
                                update_fields=[
                                    "kilometres_chassis"
                                ]
                            )

                            # =====================================
                            # LOG
                            # =====================================
                            from django.utils.translation import gettext_noop

                            ACTION_CONTROLE_ADMISSION = gettext_noop(
                                "Contrôle de l'admission"
                            )

                            UserLog.objects.create(
                                utilisateur=request.user,
                                action=f"{ACTION_CONTROLE_ADMISSION} - {exemplaire.immatriculation}"
                            )

                        messages.success(
                            request,
                            _(
                                "Contrôle de l'admission "
                                "enregistré avec succès."
                            ),
                        )

                        return redirect(
                            "admission:admission_list",
                            exemplaire_id=(
                                exemplaire.id
                            ),
                        )

            except Exception as e:
                messages.error(
                    request,
                    _(
                        "Erreur lors de "
                        "l'enregistrement : %(erreur)s"
                    ) % {
                        "erreur": str(e)
                    },
                )

        else:
            print(
                "FORM ADMISSION INVALID:",
                form.errors
            )

            messages.error(
                request,
                _(
                    "Le formulaire contient "
                    "des erreurs."
                ),
            )

    # =========================================================
    # GET
    # =========================================================
    else:
        admission = Admission(
            voiture_exemplaire=exemplaire,
            kilometres_chassis=(
                exemplaire.kilometres_chassis
            ),
        )

        admission.assign_technicien(
            request.user
        )

        form = AdmissionForm(
            instance=admission,
            user=request.user,
            exemplaire=exemplaire,
        )

    # =========================================================
    # SECTIONS
    # =========================================================
    section_templates = [
        {
            "title": _("Kilométrage"),
            "icon": "icons/compteur.png",
            "filter": "kilo",
        },
        {
            "title": _("Filtre à air"),
            "icon": "icons/filtre-a-air.png",
            "filter": "filtre_air_pc",
        },
        {
            "title": _("Boitier de Filtre à air"),
            "icon": "icons/filtre-a-air.png",
            "filter": "boitier",
        },
        {
            "title": _("Débitmètre"),
            "icon": "icons/capteurs.png",
            "filter": "debitmetre",
        },
        {
            "title": _("Capteur MAP"),
            "icon": "icons/capteurs.png",
            "filter": "capteur_map",
        },
        {
            "title": _("Capteur de temperature d'air"),
            "icon": "icons/capteurs.png",
            "filter": "capteur_temperature",
        },
        {
            "title": _("Boitier papillon"),
            "icon": "icons/boitier_papillon.png",
            "filter": "corps_papillon",
        },
        {
            "title": _("Collecteur d'admission"),
            "icon": "icons/admission.png",
            "filter": "collecteur",
        },
        {
            "title": _("Turbo"),
            "icon": "icons/turbo.png",
            "filter": "turbo",
        },
        {
            "title": _("Intercooler"),
            "icon": "icons/intercooler.png",
            "filter": "intercooler",
        },
        {
            "title": _("Vanne EGR"),
            "icon": "icons/vanne.png",
            "filter": "vanne_",
        },
        {
            "title": _("Durites d'admission"),
            "icon": "icons/durite.png",
            "filter": "durites_admission",
        },
        {
            "title": _("Joints"),
            "icon": "icons/joint_admission.png",
            "filter": "joints_admission",
        },
        {
            "title": _("Etiquette"),
            "icon": "icons/tag.png",
            "filter": "tag",
        },
        {
            "title": _("Pays"),
            "icon": "icons/pays.png",
            "filter": "pays",
        },

        {
            "title": _("Remarques"),
            "icon": "icons/notes.png",
            "filter": "remarques",
        },
        {
            "title": _("Serrage des roues"),
            "icon": "icons/roue.png",
            "filter": "serrage",
        },
        {
            "title": _("Technicien"),
            "icon": "icons/mecanicien.png",
            "filter": "tech",
        },
        {
            "title": _("Main d'oeuvre"),
            "icon": "icons/taux.png",
            "filter": "taux_",
        },
    ]

    sections = [
        {
            "title": section["title"],
            "icon": section["icon"],
            "fields": [
                field
                for field in form
                if section["filter"] in field.name
            ],
        }
        for section in section_templates
    ]

    # =========================================================
    # RENDER
    # =========================================================
    return render(
        request,
        "admission/admission_check.html",
        {
            "exemplaire": exemplaire,
            "immatriculation": (
                exemplaire.immatriculation
            ),
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
def admission_detail_view(request, admission_id):
    admission = get_object_or_404(
        Admission.objects.select_related("voiture_exemplaire"),
        id=admission_id
    )

    context = {
        "admission": admission,
        "exemplaire": admission.voiture_exemplaire,
    }
    return render(request, "admission/admission_detail.html", context)


@login_required
@never_cache
def modifier_admission_view(request, admission_id):

    tenant = request.user.societe

    # =========================================================
    # RÉCUPÉRATION DE L'ADMISSION
    # =========================================================
    admission = get_object_or_404(
        Admission.objects.select_related(
            "voiture_exemplaire",
            "maintenance",
            "main_oeuvre",
        ).filter(
            Q(
                voiture_exemplaire__client__societe=tenant
            )
            |
            Q(
                voiture_exemplaire__client__isnull=True,
                voiture_exemplaire__societe=tenant,
            )
        ),
        id=admission_id,
    )

    exemplaire = admission.voiture_exemplaire

    # =========================================================
    # IMPORTANT
    # Kilométrage enregistré lors du contrôle Admission
    # =========================================================
    kilometrage_admission_enregistre = (
        admission.kilometrage_admission
        or admission.kilometres_chassis
        or 0
    )

    # =========================================================
    # POST
    # =========================================================
    if request.method == "POST":

        form = AdmissionForm(
            request.POST,
            instance=admission,
            user=request.user,
            exemplaire=exemplaire,
        )

        if form.is_valid():

            try:
                with transaction.atomic():

                    # =============================================
                    # NOUVEAU KILOMÉTRAGE SAISI
                    # =============================================
                    km = form.cleaned_data.get(
                        "kilometrage_admission"
                    )

                    if km is None:

                        form.add_error(
                            "kilometrage_admission",
                            _("Le kilométrage est obligatoire."),
                        )

                    else:

                        km = int(km)

                        # =========================================
                        # COMPARAISON AVEC LE KM ADMISSION ENREGISTRÉ
                        # PAS AVEC kilometres_chassis
                        # =========================================
                        if km < kilometrage_admission_enregistre:

                            form.add_error(
                                "kilometrage_admission",
                                _(
                                    "Le kilométrage du contrôle "
                                    "de l'admission ne peut pas être "
                                    "inférieur au kilométrage "
                                    "précédemment enregistré."
                                ),
                            )

                        else:

                            # =====================================
                            # ADMISSION
                            # =====================================
                            admission = form.save(
                                commit=False
                            )

                            admission.voiture_exemplaire = (
                                exemplaire
                            )

                            admission.kilometrage_admission = (
                                km
                            )

                            admission.assign_technicien(
                                request.user
                            )

                            admission.tech_last_maintained_by = (
                                request.user
                            )

                            # ATTENTION :
                            # on ne modifie PAS ici
                            # admission.kilometres_chassis
                            #
                            # Il reste le snapshot historique
                            # du kilométrage avant intervention.

                            admission.save()

                            form.save_m2m()

                            # =====================================
                            # VEHICULE
                            # =====================================
                            kilometrage_vehicule_actuel = (
                                exemplaire.kilometres_chassis
                                or 0
                            )

                            # On ne fait jamais redescendre
                            # le kilométrage du véhicule
                            if km >= kilometrage_vehicule_actuel:

                                exemplaire.kilometres_chassis = (
                                    km
                                )

                                exemplaire.save(
                                    update_fields=[
                                        "kilometres_chassis"
                                    ]
                                )

                            # =====================================
                            # MAINTENANCE
                            # =====================================
                            if admission.maintenance_id:

                                maintenance = (
                                    admission.maintenance
                                )

                                maintenance.voiture_exemplaire = (
                                    exemplaire
                                )

                                maintenance.immatriculation = (
                                    exemplaire.immatriculation
                                )

                                maintenance.kilometres_chassis = (
                                    km
                                )

                                maintenance.type_maintenance = (
                                    Maintenance
                                    .TypeMaintenance
                                    .ADMISSION
                                )

                                maintenance.save(
                                    update_fields=[
                                        "voiture_exemplaire",
                                        "immatriculation",
                                        "kilometres_chassis",
                                        "type_maintenance",
                                    ]
                                )

                            # =====================================
                            # LOG
                            # =====================================
                            from django.utils.translation import gettext_noop

                            ACTION_MODIFICATION_CONTROLE_ADMISSION = gettext_noop(
                                "Modification du contrôle de l'admission"
                            )

                            UserLog.objects.create(
                                utilisateur=request.user,
                                action=f"{ACTION_MODIFICATION_CONTROLE_ADMISSION} - {exemplaire.immatriculation}"
                            )

                    if not form.errors:

                        messages.success(
                            request,
                            _(
                                "Contrôle de l'admission "
                                "modifié avec succès !"
                            ),
                        )

                        return redirect(
                            "admission:admission_detail",
                            admission_id=admission.id,
                        )

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
            messages.error(
                request,
                _("Le formulaire contient des erreurs."),
            )

    # =========================================================
    # GET
    # =========================================================
    else:

        form = AdmissionForm(
            instance=admission,
            user=request.user,
            exemplaire=exemplaire,
        )

        # =====================================================
        # IMPORTANT :
        # en modification, le champ kilometres_chassis affiché
        # doit montrer le kilometrage_admission enregistré
        # =====================================================
        if "kilometres_chassis" in form.fields:

            form.fields[
                "kilometres_chassis"
            ].initial = (
                kilometrage_admission_enregistre
            )

        # Le champ admission garde également
        # sa valeur enregistrée
        if "kilometrage_admission" in form.fields:

            form.fields[
                "kilometrage_admission"
            ].initial = (
                kilometrage_admission_enregistre
            )

    # =========================================================
    # SECTIONS
    # =========================================================
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
            "title": _("Filtre à air"),
            "icon": "icons/filtre-a-air.png",
            "fields": [
                form[f.name]
                for f in form
                if "filtre_air_p" in f.name
            ],
        },
        {
            "title": _("Boitier de Filtre à air"),
            "icon": "icons/filtre-a-air.png",
            "fields": [
                form[f.name]
                for f in form
                if "boitier" in f.name
            ],
        },
        {
            "title": _("Débitmètre"),
            "icon": "icons/capteurs.png",
            "fields": [
                form[f.name]
                for f in form
                if "debitmetre" in f.name
            ],
        },
        {
            "title": _("Capteur MAP"),
            "icon": "icons/capteurs.png",
            "fields": [
                form[f.name]
                for f in form
                if "capteur_map" in f.name
            ],
        },
        {
            "title": _("Capteur de température d'air"),
            "icon": "icons/capteurs.png",
            "fields": [
                form[f.name]
                for f in form
                if "capteur_temperature" in f.name
            ],
        },
        {
            "title": _("Boitier papillon"),
            "icon": "icons/boitier_papillon.png",
            "fields": [
                form[f.name]
                for f in form
                if "corps_papillon" in f.name
            ],
        },
        {
            "title": _("Collecteur d'admission"),
            "icon": "icons/admission.png",
            "fields": [
                form[f.name]
                for f in form
                if "collecteur" in f.name
            ],
        },
        {
            "title": _("Turbo"),
            "icon": "icons/turbo.png",
            "fields": [
                form[f.name]
                for f in form
                if "turbo" in f.name
            ],
        },
        {
            "title": _("Intercooler"),
            "icon": "icons/intercooler.png",
            "fields": [
                form[f.name]
                for f in form
                if "intercooler" in f.name
            ],
        },
        {
            "title": _("Vanne EGR"),
            "icon": "icons/vanne.png",
            "fields": [
                form[f.name]
                for f in form
                if "vanne_" in f.name
            ],
        },
        {
            "title": _("Durites d'admission"),
            "icon": "icons/durite.png",
            "fields": [
                form[f.name]
                for f in form
                if "durites_admission" in f.name
            ],
        },
        {
            "title": _("Joints"),
            "icon": "icons/joint_admission.png",
            "fields": [
                form[f.name]
                for f in form
                if "joints_admission" in f.name
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
            "title": _("Serrage des roues"),
            "icon": "icons/roue.png",
            "fields": [form[f.name] for f in form if "serrage" in f.name],
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
        "admission/modifier_admission.html",
        {
            "form": form,
            "admission": admission,
            "sections": sections,
            "exemplaire": exemplaire,
            "immatriculation": (
                exemplaire.immatriculation
            ),
        },
    )


@login_required
def admission_detail_pdf_view(request, pk):

    admission = get_object_or_404(
        Admission.objects.select_related(
            "voiture_exemplaire",
            "maintenance",
            "tech_technicien",
            "tech_societe",
            "main_oeuvre",
            "main_oeuvre__utilisateur",
        ),
        pk=pk,
    )

    # Génération du rapport des pièces remplacées
    rapport = admission.generer_rapport_remplacement() or {}

    rapport.setdefault("lignes", [])

    # -------------------------
    # Total des pièces
    # -------------------------

    total_pieces = Decimal(
        str(
            rapport.get("total_general")
            or Decimal("0.00")
        )
    ).quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP,
    )

    # -------------------------
    # Main-d'œuvre
    # -------------------------

    if admission.main_oeuvre:
        cout_main_oeuvre = Decimal(
            str(
                admission.main_oeuvre.cout_total
                or Decimal("0.00")
            )
        )
    else:
        cout_main_oeuvre = Decimal("0.00")

    cout_main_oeuvre = cout_main_oeuvre.quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP,
    )

    # -------------------------
    # Total général
    # -------------------------

    total_general_avec_main_oeuvre = (
        total_pieces + cout_main_oeuvre
    ).quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP,
    )

    rapport.update({
        "total_pieces": total_pieces,
        "cout_main_oeuvre": cout_main_oeuvre,
        "total_general_avec_main_oeuvre":
            total_general_avec_main_oeuvre,
    })

    # -------------------------
    # Génération HTML
    # -------------------------

    html_string = render_to_string(
        "admission/admission_detail_pdf.html",
        {
            "admission": admission,
            "rapport": rapport,
            "date_export": timezone.now(),
            "societe": request.user.societe,
        },
        request=request,
    )

    # -------------------------
    # Génération PDF
    # -------------------------

    pdf = HTML(
        string=html_string,
        base_url=request.build_absolute_uri("/"),
    ).write_pdf()

    # -------------------------
    # Nom du fichier
    # -------------------------

    # =========================================================
    # IMMATRICULATION
    # =========================================================

    immatriculation = (
        admission.voiture_exemplaire.immatriculation
        if admission.voiture_exemplaire
        else "sans_immatriculation"
    )

    # =========================================================
    # TECHNICIEN
    # =========================================================

    technicien = (
            admission.tech_nom_technicien
            or "technicien_inconnu"
    )

    # Nettoyage pour le nom du fichier
    technicien = str(technicien).replace(" ", "_")
    immatriculation = str(immatriculation).replace(" ", "_")

    # =========================================================
    # DATE
    # =========================================================

    date_pdf = (
        admission.date.strftime("%Y-%m-%d")
        if admission.date
        else timezone.now().strftime("%Y-%m-%d")
    )

    # =========================================================
    # TITRE / NOM DU PDF
    # =========================================================

    nom_fichier = (
        f"{_('Admission')}_{technicien}_{immatriculation}_{date_pdf}.pdf"
    )

    response = HttpResponse(
        pdf,
        content_type="application/pdf",
    )

    response["Content-Disposition"] = (
        f'inline; filename="{nom_fichier}"'
    )

    return response
