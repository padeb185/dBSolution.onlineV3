from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.db import transaction, models
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import ListView
from django_tenants.utils import tenant_context
from maintenance.models import Maintenance
from voiture.voiture_exemplaire.models import VoitureExemplaire
from django.db.models import Q
from maintenance.nettoyage_exterieur.models import NettoyageExterieur
from django.utils.translation import gettext_lazy as _
from .forms import CheckupTrackForm
from .models import CheckupTrack


# -----------------------------
# Classe ListView pour checkup_track
# -----------------------------
@method_decorator([login_required, never_cache], name='dispatch')
class CheckupTrackListView(ListView):
    model = CheckupTrack
    template_name = "checkup_track/checkup_track_list.html"
    context_object_name = "track_checks"
    paginate_by = 100
    ordering = ["-id"]

    def get_queryset(self):
        queryset = CheckupTrack.objects.select_related(
            "voiture_exemplaire", "maintenance", "tech_societe"
        )

        # Filtrer par société : inclure les objets NULL ou ceux de la société de l'utilisateur
        societe = getattr(self.request.user, "societe", None)
        if societe:
            queryset = queryset.filter(
                models.Q(tech_societe=societe) | models.Q(tech_societe__isnull=True)
            )

        return queryset.order_by(*self.ordering)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        exemplaire_id = self.kwargs.get("exemplaire_id")
        context["exemplaire"] = get_object_or_404(VoitureExemplaire, id=exemplaire_id)
        return context




@never_cache
@login_required
def track_check_form_view(request, exemplaire_id):
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
            type_maintenance="checkup_track"
        ).order_by("-date_intervention").first()

        if not maintenance:
            maintenance = Maintenance.objects.create(
                voiture_exemplaire=exemplaire,
                mecanicien=request.user,
                immatriculation=exemplaire.immatriculation,
                date_intervention=timezone.localtime(timezone.now()).date(),
                kilometres_chassis=exemplaire.kilometres_chassis,
                kilometres_dernier_entretien=exemplaire.kilometres_dernier_entretien,
                type_maintenance="checkup_track",
                tag=Maintenance.Tag.JAUNE,
            )

        # Créer ou récupérer l'objet NettoyageInterieur
        checkup_track = CheckupTrack(
            voiture_exemplaire=exemplaire,
            maintenance=maintenance,
            kilometres_chassis=exemplaire.kilometres_chassis
        )

        if request.method == "POST":
            form = CheckupTrackForm(
                request.POST,
                instance=checkup_track,
                user=request.user,
                exemplaire=exemplaire
            )

            if form.is_valid():
                try:
                    with transaction.atomic():
                        checkup_track = form.save(commit=False)


                        checkup_track.assign_technicien(request.user)

                        # Gestion du kilométrage
                        km_checkup_track = form.cleaned_data.get("kilometres_chassis")
                        if km_checkup_track is not None and km_checkup_track >= exemplaire.kilometres_chassis:
                            checkup_track.kilometres_chassis = km_checkup_track
                            exemplaire.kilometres_chassis = km_checkup_track
                            exemplaire.save()
                        elif km_checkup_track is not None and km_checkup_track < exemplaire.kilometres_chassis:
                            form.add_error(
                                "kilometres_chassis",
                                _("Le kilométrage ne peut pas être inférieur au kilométrage actuel.")
                            )
                            raise ValueError("Kilométrage invalide")

                        checkup_track.save()

                    messages.success(request, _("Checkup piste enregistré avec succès."))

                except Exception as e:
                    messages.error(request, _(f"Erreur lors de l'enregistrement : {str(e)}"))
            else:
                messages.error(request, _("Le formulaire contient des erreurs."))
                print(form.errors)
        else:
            checkup_track.assign_technicien(request.user)

            form = CheckupTrackForm(
                instance=checkup_track,
                user=request.user,
                exemplaire=exemplaire
            )

        return render(request, 'checkup_track/track_check_form.html', {
            "exemplaire": exemplaire,
            "immatriculation": exemplaire.immatriculation,
            "maintenance": maintenance,
            "form": form,
            "now": timezone.now(),
        })



# ------------
# Vue détail checkup_track
# -----------------------------
@login_required
def checkup_track_detail_view(request, checkup_track_id):
    checkup_track = get_object_or_404(
        CheckupTrack.objects.select_related("voiture_exemplaire"),
        id=checkup_track_id
    )

    context = {
        "checkup_track": checkup_track,
        "exemplaire": checkup_track.voiture_exemplaire,
    }
    return render(request, "checkup_track/checkup_track_detail.html", context)


@login_required
def modifier_checkup_track_view(request, checkup_track_id):
    tenant = request.user.societe

    with tenant_context(tenant):
        # Récupération du checkup_track avec son exemplaire
        checkup_track = get_object_or_404(
            CheckupTrack.objects.select_related("voiture_exemplaire"),
            id=checkup_track_id
        )

        # -------------------------
        # POST
        # -------------------------
        if request.method == "POST":
            form = CheckupTrackForm(
                request.POST,
                instance=checkup_track,
                user=request.user,       # 🔑 important pour initialiser technicien/societe
                exemplaire=checkup_track.voiture_exemplaire
            )
            if form.is_valid():
                form.save()
                messages.success(request, _("checkup piste modifié avec succès !"))
                return redirect("checkup_track:modifier_checkup_track", checkup_track_id=checkup_track.id)
            else:
                messages.error(request, _("Le formulaire contient des erreurs."))
                print(form.errors)

        # -------------------------
        # GET
        # -------------------------
        else:
            form = CheckupTrackForm(
                instance=checkup_track,
                user=request.user,
                exemplaire=checkup_track.voiture_exemplaire
            )

    return render(
        request,
        "checkup_track/modifier_checkup_track.html",
        {
            "form": form,
            "checkup_track": checkup_track,
            "exemplaire": checkup_track.voiture_exemplaire,
        }
    )