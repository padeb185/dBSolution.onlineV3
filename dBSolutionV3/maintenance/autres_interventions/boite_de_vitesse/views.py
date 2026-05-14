from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.db import transaction, models
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import ListView
from django_tenants.utils import tenant_context, schema_context
from maintenance.models import Maintenance
from voiture.voiture_exemplaire.models import VoitureExemplaire
from django.db.models import Q
from maintenance.nettoyage_exterieur.models import NettoyageExterieur
from django.utils.translation import gettext_lazy as _
from maintenance.autres_interventions.boite_de_vitesse.forms import ControleBoiteForm
from maintenance.autres_interventions.boite_de_vitesse.models import ControleBoite
from maintenance.autres_interventions.boite_de_vitesse.remplacement_boite.models import RemplacementBoite
from maintenance.types_maintenances import TYPES_MAINTENANCE
from voiture.voiture_modele.models import VoitureModele





# -----------------------------
# Classe ListView pour boite
# -----------------------------
@method_decorator([login_required, never_cache], name='dispatch')
class BoiteListView(ListView):
    model = ControleBoite   # ✅ ICI
    template_name = "boite_de_vitesse/boite_list.html"
    context_object_name = "boite_de_vitesses"
    paginate_by = 100
    ordering = ["-id"]

    def get_queryset(self):
        queryset = ControleBoite.objects.select_related(
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
        return context





@never_cache
@login_required
def boite_check_view(request, exemplaire_id):

    tenant = request.user.societe
    role = request.user.role

    maintenance = None  # 👈 important pour éviter UnboundLocalError

    with tenant_context(tenant):

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

            form = ControleBoiteForm(
                request.POST,
                user=request.user,
                exemplaire=exemplaire
            )

            if form.is_valid():

                try:
                    with transaction.atomic():

                        # 🔴 maintenance unique
                        maintenance = Maintenance.objects.create(
                            societe=request.user.societe,
                            voiture_exemplaire=exemplaire,
                            immatriculation=exemplaire.immatriculation,
                            date_intervention=timezone.now().date(),
                            kilometres_chassis=exemplaire.kilometres_chassis,
                            kilometres_dernier_entretien=exemplaire.kilometres_dernier_entretien,
                            type_maintenance=Maintenance.TypeMaintenance.BOITE,
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
                        boite = form.save(commit=False)

                        boite.assign_technicien(request.user)


                        boite.assign_technicien(request.user)

                        # Gestion du kilométrage
                        km_checkup = form.cleaned_data.get("kilometres_chassis")

                        if km_checkup is not None:

                            km_checkup = int(km_checkup)

                            if km_checkup >= exemplaire.kilometres_chassis:

                                # mise à jour intervention
                                boite.kilometres_chassis = km_checkup

                                # mise à jour véhicule
                                exemplaire.kilometres_chassis = km_checkup
                                exemplaire.save(update_fields=["kilometres_chassis"])

                            else:
                                form.add_error(
                                    "kilometres_chassis",
                                    _("Le kilométrage ne peut pas être inférieur au kilométrage actuel.")
                                )

                                raise ValueError("Kilométrage invalide")

                        boite.save()

                    messages.success(request, _("Checkup enregistré avec succès."))

                except Exception as e:
                    messages.error(request, _(f"Erreur lors de l'enregistrement : {str(e)}"))
            else:
                print("FORM INVALID:", form.errors)
                messages.error(request, _("Le formulaire contient des erreurs."))

        else:
            boite = ControleBoite(
                voiture_exemplaire=exemplaire,
                kilometres_chassis=exemplaire.kilometres_chassis
            )

            boite.assign_technicien(request.user)

            form = ControleBoiteForm(
                instance=boite,
                user=request.user,
                exemplaire=exemplaire
            )

        return render(request, 'boite_de_vitesse/boite_check.html', {
            "exemplaire": exemplaire,
            "immatriculation": exemplaire.immatriculation,
            "maintenance": maintenance,
            "form": form,
            "now": timezone.now(),
        })



# ------------
# Vue détail boite
# -----------------------------
@login_required
def boite_detail_view(request, boite_id):
    boite = get_object_or_404(
        ControleBoite.objects.select_related("voiture_exemplaire"),
        id=boite_id
    )

    context = {
        "boite": boite,
        "exemplaire": boite.voiture_exemplaire,
    }
    return render(request, "boite_de_vitesse/boite_detail.html", context)





@login_required
def modifier_boite_view(request, boite_id):
    tenant = request.user.societe

    with tenant_context(tenant):
        # Récupération du controle boite avec son exemplaire
        boite = get_object_or_404(
            ControleBoite.objects.select_related("voiture_exemplaire"),
            id=boite_id
        )

        # -------------------------
        # POST
        # -------------------------
        if request.method == "POST":
            form = ControleBoiteForm(
                request.POST,
                instance=boite,
                user=request.user,       # 🔑 important pour initialiser technicien/societe
                exemplaire=boite.voiture_exemplaire
            )
            if form.is_valid():
                form.save()
                messages.success(request, _("Checkup modifié avec succès !"))
                return redirect("boite_de_vitesse:modifier_boite", boite_id=boite.id)
            else:
                messages.error(request, _("Le formulaire contient des erreurs."))
                print(form.errors)

        # -------------------------
        # GET
        # -------------------------
        else:
            form = ControleBoiteForm(
                instance=boite,
                user=request.user,
                exemplaire=boite.voiture_exemplaire
            )

    return render(
        request,
        "boite_de_vitesse/modifier_boite.html",
        {
            "form": form,
            "boite": boite,
            "exemplaire": boite.voiture_exemplaire,
        }
    )






@never_cache
@login_required
def dashboard_boite_view(request, exemplaire_id):
    tenant = request.user.societe

    with tenant_context(tenant):

        user = request.user
        context = {}

        # 🔹 Récupérer l'exemplaire AVANT
        exemplaire = get_object_or_404(VoitureExemplaire, id=exemplaire_id)

        # --- Sécurité tenant ---
        tenant_schema = getattr(request, 'tenant', None)
        schema_name = tenant_schema.schema_name if tenant_schema else None


        total_boite = total_remplacement_boite = total_int_boite = 0

        boite = remplacement_boite  = []



        if schema_name:
            with schema_context(schema_name):

                # ✅ FILTRAGE PAR EXEMPLAIRE

                boite = ControleBoite.objects.filter(voiture_exemplaire=exemplaire)
                remplacement_boite = RemplacementBoite.objects.filter(voiture_exemplaire=exemplaire)


                # ✅ COUNTS CORRECTS
                total_boite = boite.count()
                total_remplacement_boite = remplacement_boite.count()
                total_int_boite = boite.count() + remplacement_boite.count()


                total_int_boite = total_boite + total_remplacement_boite

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
                    'maintenance:dashboard_boite',
                    exemplaire_id=exemplaire.id
                )

        # --- CONTEXT ---
        context.update({
            "exemplaire": exemplaire,
            "types_maintenance": TYPES_MAINTENANCE,

            "total_boite": total_boite,
            "total_remplacement_boite": total_remplacement_boite,
            "total_int_boite": total_int_boite,

            "boite": boite,
            "remplacement_boite": remplacement_boite,


            "modeles": modeles,

        })

        return render(request, "boite_de_vitesse/dashboard_boite.html", context)




