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
from maintenance.jeux_pieces.models import ControleJeuxPieces
from maintenance.jeux_pieces.forms import ControleJeuxPiecesForm
from voiture.voiture_exemplaire.models import VoitureExemplaire
from django.db.models import Q
from django.utils.translation import gettext_lazy as _




# -----------------------------
# Classe ListView pour checkup
# -----------------------------
@method_decorator([login_required, never_cache], name='dispatch')
class JeuListView(ListView):
    model = ControleJeuxPieces
    template_name = "jeux_pieces/jeux_pieces_list.html"
    context_object_name = "jeux_pieces"
    paginate_by = 100
    ordering = ["-id"]

    def get_queryset(self):
        queryset = ControleJeuxPieces.objects.select_related(
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
def controle_jeux_pieces_view(request, exemplaire_id):
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
            type_maintenance="controle"
        ).order_by("-date_intervention").first()

        if not maintenance:
            maintenance = Maintenance.objects.create(
                voiture_exemplaire=exemplaire,
                mecanicien=request.user,
                immatriculation=exemplaire.immatriculation,
                date_intervention=timezone.localtime(timezone.now()).date(),
                kilometres_chassis=exemplaire.kilometres_chassis,
                kilometres_derniere_intervention=exemplaire.kilometres_derniere_intervention,
                type_maintenance="controle",
                tag=Maintenance.Tag.JAUNE,
            )

        # Créer ou récupérer l'objet NettoyageInterieur
        controle = ControleJeuxPieces(
            voiture_exemplaire=exemplaire,
            maintenance=maintenance,
            kilometres_chassis=exemplaire.kilometres_chassis
        )

        if request.method == "POST":
            form = ControleJeuxPiecesForm(
                request.POST,
                instance=controle,
                user=request.user,
                exemplaire=exemplaire
            )

            if form.is_valid():
                try:
                    with transaction.atomic():
                        controle = form.save(commit=False)


                        controle.assign_technicien(request.user)

                        # Gestion du kilométrage
                        km_checkup = form.cleaned_data.get("kilometres_chassis")
                        if km_checkup is not None and km_checkup >= exemplaire.kilometres_chassis:
                            controle.kilometres_chassis = km_checkup
                            exemplaire.kilometres_chassis = km_checkup
                            exemplaire.save()
                        elif km_checkup is not None and km_checkup < exemplaire.kilometres_chassis:
                            form.add_error(
                                "kilometres_chassis",
                                _("Le kilométrage ne peut pas être inférieur au kilométrage actuel.")
                            )
                            raise ValueError("Kilométrage invalide")

                        controle.save()

                    messages.success(request, _("Controle des jeux enregistré avec succès."))

                except Exception as e:
                    messages.error(request, _(f"Erreur lors de l'enregistrement : {str(e)}"))
            else:
                messages.error(request, _("Le formulaire contient des erreurs."))
                print(form.errors)
        else:
            controle.assign_technicien(request.user)

            form = ControleJeuxPiecesForm(
                instance=controle,
                user=request.user,
                exemplaire=exemplaire
            )

        return render(request, "jeux_pieces/controle_jeux.html", {
            "exemplaire": exemplaire,
            "immatriculation": exemplaire.immatriculation,
            "maintenance": maintenance,
            "form": form,
            "now": timezone.now(),
        })




# ------------
# Vue détail checkup
# -----------------------------
@login_required
def jeux_pieces_detail_view(request, jeu_id):
    jeu = get_object_or_404(
        ControleJeuxPieces.objects.select_related("voiture_exemplaire"),
        id=jeu_id
    )

    context = {
        "jeu": jeu,
        "exemplaire": jeu.voiture_exemplaire,
    }
    return render(request, "jeux_pieces/jeux_pieces_detail.html", context)


@login_required
def modifier_jeux_pieces_view(request, jeu_id):
    tenant = request.user.societe

    with tenant_context(tenant):
        # Récupération du checkup avec son exemplaire
        jeu = get_object_or_404(
            ControleJeuxPieces.objects.select_related("voiture_exemplaire"),
            id=jeu_id
        )

        # -------------------------
        # POST
        # -------------------------
        if request.method == "POST":
            form = ControleJeuxPiecesForm(
                request.POST,
                instance=jeu,
                user=request.user,
                exemplaire=jeu.voiture_exemplaire
            )
            if form.is_valid():
                form.save()
                messages.success(request, _("Controle des jeux modifié avec succès !"))

            else:
                messages.error(request, _("Le formulaire contient des erreurs."))
                print(form.errors)

        # -------------------------
        # GET
        # -------------------------
        else:
            form = ControleJeuxPiecesForm(
                instance=jeu,
                user=request.user,
                exemplaire=jeu.voiture_exemplaire
            )

    return render(
        request,
        "jeux_pieces/modifier_jeux_pieces.html",
        {
            "form": form,
            "jeu": jeu,
            "exemplaire": jeu.voiture_exemplaire,
        }
    )