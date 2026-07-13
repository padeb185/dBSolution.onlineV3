from datetime import datetime
from decimal import Decimal

from django.http import HttpResponse
from django.template.loader import render_to_string

from django.contrib import messages
from django.db import models, transaction
from django.db.models import Q
from django.utils import timezone
from django.utils.decorators import method_decorator

from django.shortcuts import get_object_or_404, redirect, render

from django.views.decorators.cache import never_cache

from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django_tenants.utils import tenant_context, schema_context
from maintenance.autres_interventions.echappement.forms import ControleEchappementForm
from maintenance.autres_interventions.echappement.models import Echappement, EtatOKNotOK
from maintenance.models import Maintenance
from maintenance.types_maintenances import TYPES_MAINTENANCE
from utilisateurs.models import UserLog
from voiture.voiture_exemplaire.models import VoitureExemplaire
from voiture.voiture_modele.models import VoitureModele
from django.utils.translation import gettext_lazy as _
from weasyprint import HTML


@never_cache
@login_required
def dashboard_echappement_view(request, exemplaire_id):
    tenant = request.user.societe

    with tenant_context(tenant):

        user = request.user
        context = {}

        # 🔹 Récupérer l'exemplaire AVANT
        exemplaire = get_object_or_404(VoitureExemplaire, id=exemplaire_id)

        # --- Sécurité tenant ---
        tenant_schema = getattr(request, 'tenant', None)
        schema_name = tenant_schema.schema_name if tenant_schema else None


        total_echappement = total_echappement_check = 0

        echappement = echappement_check  = []



        if schema_name:
            with schema_context(schema_name):

                # ✅ FILTRAGE PAR EXEMPLAIRE

                echappement = Echappement.objects.filter(voiture_exemplaire=exemplaire)



                # ✅ COUNTS CORRECTS
                total_echappement = echappement.count()



                total_echappement = total_echappement_check

                modeles = VoitureModele.objects.all()
        else:
            modeles = []

        # --- POST ---
        if request.method == "POST":
            type_choisi = request.POST.get("type_maintenance")
            date_intervention = request.POST.get("date_intervention")
            description = request.POST.get("description", "")

            if type_choisi and date_intervention:
                Maintenance.objects.create(
                    societe=tenant,
                    voiture_exemplaire=exemplaire,
                    type_maintenance=type_choisi,
                    immatriculation=exemplaire.immatriculation,
                    date_intervention=date_intervention,
                    description=description
                )
                return redirect(
                    'maintenance:dashboard_echappement',
                    exemplaire_id=exemplaire.id
                )

        # --- CONTEXT ---
        context.update({
            "exemplaire": exemplaire,
            "types_maintenance": TYPES_MAINTENANCE,

            "total_boite": total_echappement,
            "total_echappement_check": total_echappement_check,


            "echappement": echappement,
            "echeppement_check": echappement_check,


            "modeles": modeles,

        })

        return render(request, "echappement/dashboard_echappement.html", context)



# -----------------------------
# Classe ListView pour Echappement
# -----------------------------
@method_decorator([login_required, never_cache], name='dispatch')
class EchappementListView(ListView):
    model = Echappement   # ✅ ICI
    template_name = "echappement/echappement_list.html"
    context_object_name = "echappements"

    ordering = ["-id"]

    def get_queryset(self):
        queryset = Echappement.objects.select_related(
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
def echappement_check_view(request, exemplaire_id):
    tenant = request.user.societe
    role = request.user.role

    maintenance = None

    with tenant_context(tenant):

        # Récupération sécurisée de l'exemplaire
        exemplaire = get_object_or_404(
            VoitureExemplaire.objects.filter(
                Q(client__societe=tenant)
                | Q(client__isnull=True, societe=tenant)
            ),
            id=exemplaire_id
        )

        roles_autorises = [
            "mecanicien",
            "apprenti",
            "magasinier",
            "chef_mecanicien",
            "direction",
        ]

        if role not in roles_autorises:
            messages.error(request, _("Accès refusé."))
            return redirect("utilisateurs:dashboard")

        # =========================
        # POST
        # =========================
        if request.method == "POST":

            # On crée une instance déjà liée au véhicule
            instance_echappement = Echappement(
                voiture_exemplaire=exemplaire,
                kilometres_chassis=exemplaire.kilometres_chassis,
            )

            instance_echappement.assign_technicien(request.user)

            form = ControleEchappementForm(
                request.POST,
                instance=instance_echappement,
                user=request.user,
                exemplaire=exemplaire,
            )

            if form.is_valid():
                km = form.cleaned_data.get("kilometrage_echappement")

                # Sécurité supplémentaire
                if km is None:
                    form.add_error(
                        "kilometrage_echappement",
                        _("Le kilométrage est obligatoire.")
                    )
                else:
                    km = int(km)
                    ancien_km = exemplaire.kilometres_chassis or 0

                    if km < ancien_km:
                        form.add_error(
                            "kilometrage_echappement",
                            _(
                                "Le kilométrage ne peut pas être inférieur "
                                "au kilométrage actuel du véhicule."
                            )
                        )

                # On vérifie qu'aucune erreur n'a été ajoutée
                if not form.errors:
                    try:
                        with transaction.atomic():

                            # =========================
                            # Mise à jour du véhicule
                            # =========================
                            if km > (exemplaire.kilometres_chassis or 0):
                                exemplaire.kilometres_chassis = km

                            exemplaire.date_derniere_intervention = (
                                timezone.localdate()
                            )

                            exemplaire.update_kilometres()
                            exemplaire.save()

                            # =========================
                            # Création maintenance
                            # =========================
                            maintenance = Maintenance.objects.create(
                                societe=tenant,
                                voiture_exemplaire=exemplaire,
                                immatriculation=exemplaire.immatriculation,
                                date_intervention=timezone.localdate(),
                                kilometres_chassis=(
                                    exemplaire.kilometres_chassis
                                ),
                                kilometres_dernier_entretien=(
                                    exemplaire.kilometres_dernier_entretien
                                ),

                                # Remplacer par la valeur exacte de ton enum
                                type_maintenance=(
                                    Maintenance.TypeMaintenance.ECHAPPEMENT
                                ),

                                tag=Maintenance.Tag.JAUNE,
                            )

                            # =========================
                            # Attribution du personnel
                            # =========================
                            if role == "mecanicien":
                                maintenance.mecanicien = request.user

                            elif role == "chef_mecanicien":
                                maintenance.chef_mecanicien = request.user

                            elif role == "magasinier":
                                maintenance.magasinier = request.user

                            elif role == "direction":
                                maintenance.direction = request.user

                            maintenance.save()

                            # ManyToMany après le premier save
                            if role == "apprenti":
                                maintenance.apprentis.add(request.user)

                            # =========================
                            # Création échappement
                            # =========================
                            echappement = form.save(commit=False)

                            # Affectations obligatoires
                            echappement.voiture_exemplaire = exemplaire
                            echappement.maintenance = maintenance
                            echappement.kilometres_chassis = (
                                exemplaire.kilometres_chassis
                            )
                            echappement.kilometrage_echappement = km

                            echappement.assign_technicien(request.user)
                            echappement.save()

                            # Nécessaire si le formulaire contient des M2M
                            form.save_m2m()

                            UserLog.objects.create(
                                utilisateur=request.user,
                                action=_(
                                    "Contrôle échappement - "
                                    "%(immatriculation)s"
                                ) % {
                                    "immatriculation": (
                                        exemplaire.immatriculation
                                    )
                                }
                            )

                        messages.success(
                            request,
                            _(
                                "Le contrôle de l'échappement "
                                "a été enregistré avec succès."
                            )
                        )

                        # Redirection indispensable pour éviter un double POST
                        return redirect(
                            "echappement:echappement_detail",
                            echappement_id=echappement.id,
                        )

                    except Exception as e:
                        messages.error(
                            request,
                            _("Erreur lors de l'enregistrement : %(erreur)s")
                            % {
                                "erreur": str(e)
                            }
                        )

            else:
                print("FORM INVALID:", form.errors)

                messages.error(
                    request,
                    _("Le formulaire contient des erreurs.")
                )

        # =========================
        # GET
        # =========================
        else:
            instance_echappement = Echappement(
                voiture_exemplaire=exemplaire,
                kilometres_chassis=exemplaire.kilometres_chassis,
                kilometrage_echappement=exemplaire.kilometres_chassis,
            )

            instance_echappement.assign_technicien(request.user)

            form = ControleEchappementForm(
                instance=instance_echappement,
                user=request.user,
                exemplaire=exemplaire,
            )

        return render(
            request,
            "echappement/echappement_check.html",
            {
                "exemplaire": exemplaire,
                "immatriculation": exemplaire.immatriculation,
                "maintenance": maintenance,
                "form": form,
                "now": timezone.now(),
            }
        )

# ------------
# Vue détail echappement
# -----------------------------
@login_required
def echappement_detail_view(request,echappement_id):
   echappement = get_object_or_404(
        Echappement.objects.select_related("voiture_exemplaire"),
        id=echappement_id
    )

   context = {
        "echappement":echappement,
        "exemplaire":echappement.voiture_exemplaire,
    }
   return render(request, "echappement/echappement_detail.html", context)



@login_required
def modifier_echappement_view(request, echappement_id):
    tenant = request.user.societe

    with tenant_context(tenant):
        # Récupération du contrôle échappement avec son exemplaire
        echappement = get_object_or_404(
            Echappement.objects.select_related("voiture_exemplaire"),
            id=echappement_id,
        )

        exemplaire = echappement.voiture_exemplaire

        # -------------------------
        # POST
        # -------------------------
        if request.method == "POST":
            form = ControleEchappementForm(
                request.POST,
                instance=echappement,
                user=request.user,
                exemplaire=exemplaire,
            )

            if form.is_valid():
                form.save()

                UserLog.objects.create(
                    utilisateur=request.user,
                    action=_(
                        "Modification contrôle de l'échappement - %(immatriculation)s"
                    )
                    % {
                        "immatriculation": exemplaire.immatriculation,
                    },
                )

                messages.success(
                    request,
                    _("Checkup de l'échappement modifié avec succès !"),
                )

                return redirect(
                    "echappement:modifier_echappement",
                    echappement_id=echappement.id,
                )

            messages.error(
                request,
                _("Le formulaire contient des erreurs."),
            )
            print(form.errors)

        # -------------------------
        # GET
        # -------------------------
        else:
            form = ControleEchappementForm(
                instance=echappement,
                user=request.user,
                exemplaire=exemplaire,
            )

        return render(
            request,
            "echappement/modifier_echappement.html",
            {
                "form": form,
                "echappement": echappement,
                "exemplaire": exemplaire,
            },
        )



@login_required
def echappement_check_pdf_view(request, pk):
    echappement = get_object_or_404(
        Echappement.objects.select_related(
            "voiture_exemplaire",
            "tech_technicien",
            "tech_societe",
            "societe",
            "main_oeuvre",
        ),
        pk=pk,
    )

    rapport = echappement.generer_rapport_remplacement()

    html_string = render_to_string(
        "echappement/echappement_check_pdf.html",
        {
            "echappement": echappement,
            "rapport": rapport,
            "date_export": timezone.now(),
            "societe": request.user.societe,
        },
        request=request,
    )

    pdf = HTML(
        string=html_string,
        base_url=request.build_absolute_uri("/"),
    ).write_pdf()

    voiture = echappement.voiture_exemplaire

    if voiture and voiture.immatriculation:
        immatriculation = voiture.immatriculation
    elif echappement.immatriculation:
        immatriculation = echappement.immatriculation
    else:
        immatriculation = "sans_immatriculation"

    technicien = (
        echappement.tech_nom_technicien
        or "technicien_inconnu"
    )

    filename = (
        f"rapport_echappement_"
        f"{immatriculation}_"
        f"{technicien}.pdf"
    )

    response = HttpResponse(
        pdf,
        content_type="application/pdf",
    )

    response["Content-Disposition"] = (
        f'attachment; filename="{filename}"'
    )

    return response

