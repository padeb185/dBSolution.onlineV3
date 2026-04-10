from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.db import transaction, models
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import ListView
from django_tenants.utils import tenant_context
from maintenance.models import Maintenance
from voiture.voiture_exemplaire.models import VoitureExemplaire
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from maintenance.autres_interventions.bte_vitesse_auto.forms import ControleBteVitesseAutoForm
from maintenance.autres_interventions.bte_vitesse_auto.models import ControleBteVitesseAuto


# -----------------------------
# Classe ListView pour boite
# -----------------------------
@method_decorator([login_required, never_cache], name='dispatch')
class BteVitesseAutoListView(ListView):
    model = ControleBteVitesseAuto
    template_name = "bte_auto/bte_auto_list.html"
    context_object_name = "bte_autos"
    paginate_by = 100
    ordering = ["-id"]

    def get_queryset(self):
        queryset = ControleBteVitesseAuto.objects.select_related(   # ✅ ICI
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
def bte_auto_check_view(request, exemplaire_id):
    tenant = request.user.societe

    with tenant_context(tenant):
        # Récupération de l'exemplaire
        exemplaire = get_object_or_404(
            VoitureExemplaire.objects.filter(
                Q(client__societe=tenant) | Q(client__isnull=True, societe=tenant)
            ),
            id=exemplaire_id
        )

        # Vérification des rôles
        roles_autorises = ["mécanicien", "apprenti", "magasinier", "chef mécanicien"]
        if request.user.role not in roles_autorises:
            messages.error(
                request,
                _("Seuls les mécaniciens, apprentis, magasiniers et chefs mécaniciens peuvent accéder à cette page.")
            )
            return redirect("maintenance_liste_all")

        # Récupération ou création de la maintenance
        maintenance = Maintenance.objects.filter(
            voiture_exemplaire=exemplaire,
            type_maintenance="bte_auto"
        ).order_by("-date_intervention").first()

        if not maintenance:
            maintenance = Maintenance.objects.create(
                voiture_exemplaire=exemplaire,
                mecanicien=request.user,
                immatriculation=exemplaire.immatriculation,
                date_intervention=timezone.localtime(timezone.now()).date(),
                kilometres_chassis=exemplaire.kilometres_chassis,
                kilometres_derniere_intervention=exemplaire.kilometres_derniere_intervention,
                type_maintenance="bte_vitesse_auto",
                tag=Maintenance.Tag.JAUNE,
            )

        # Créer ou récupérer l'objet Boite
        bte_auto = ControleBteVitesseAuto(
            voiture_exemplaire=exemplaire,
            maintenance=maintenance,
            kilometres_chassis=exemplaire.kilometres_chassis
        )

        if request.method == "POST":
            form = ControleBteVitesseAutoForm(
                request.POST,
                instance=bte_auto,
                user=request.user,
                exemplaire=exemplaire
            )

            if form.is_valid():
                try:
                    with transaction.atomic():
                        bte_auto = form.save(commit=False)


                        bte_auto.assign_technicien(request.user)

                        # Gestion du kilométrage
                        km_checkup = form.cleaned_data.get("kilometres_chassis")
                        if km_checkup is not None and km_checkup >= exemplaire.kilometres_chassis:
                            bte_auto.kilometres_chassis = km_checkup
                            exemplaire.kilometres_chassis = km_checkup
                            exemplaire.save()
                        elif km_checkup is not None and km_checkup < exemplaire.kilometres_chassis:
                            form.add_error(
                                "kilometres_chassis",
                                _("Le kilométrage ne peut pas être inférieur au kilométrage actuel.")
                            )
                            raise ValueError("Kilométrage invalide")

                        bte_auto.save()

                    messages.success(request, _("Contrôle boite automatique enregistré avec succès."))

                except Exception as e:
                    messages.error(request, _(f"Erreur lors de l'enregistrement : {str(e)}"))
            else:
                messages.error(request, _("Le formulaire contient des erreurs."))
                print(form.errors)
        else:
            bte_auto.assign_technicien(request.user)

            form = ControleBteVitesseAutoForm(
                instance=bte_auto,
                user=request.user,
                exemplaire=exemplaire
            )

        return render(request, 'bte_auto/bte_auto_check.html', {
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
def bte_auto_detail_view(request, bte_auto_id):
    bte_auto = get_object_or_404(
        ControleBteVitesseAuto.objects.select_related("voiture_exemplaire"),
        id=bte_auto_id
    )

    context = {
        "bte_auto": bte_auto,
        "exemplaire": bte_auto.voiture_exemplaire,
    }
    return render(request, "bte_auto/bte_auto_detail.html", context)


@login_required
def modifier_bte_auto_view(request, bte_auto_id):
    tenant = request.user.societe

    with tenant_context(tenant):
        # Récupération du controle boite avec son exemplaire
        bte_auto = get_object_or_404(
            ControleBteVitesseAuto.objects.select_related("voiture_exemplaire"),
            id=bte_auto_id
        )

        # -------------------------
        # POST
        # -------------------------
        if request.method == "POST":
            form = ControleBteVitesseAutoForm(
                request.POST,
                instance=bte_auto,
                user=request.user,       # 🔑 important pour initialiser technicien/societe
                exemplaire=bte_auto.voiture_exemplaire
            )
            if form.is_valid():
                form.save()
                messages.success(request, _("Contrôle de la boite automatique modifié avec succès !"))
                return redirect("bte_auto:modifier_bte_auto", bte_auto_id=bte_auto.id)
            else:
                messages.error(request, _("Le formulaire contient des erreurs."))
                print(form.errors)

        # -------------------------
        # GET
        # -------------------------
        else:
            form = ControleBteVitesseAutoForm(
                instance=bte_auto,
                user=request.user,
                exemplaire=bte_auto.voiture_exemplaire
            )

    return render(
        request,
        "bte_auto/modifier_bte_auto.html",
        {
            "form": form,
            "bte_auto": bte_auto,
            "exemplaire": bte_auto.voiture_exemplaire,
        }
    )