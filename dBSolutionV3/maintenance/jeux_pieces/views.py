from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.db import transaction
from django.urls import reverse
from django.db.models import Q
from django.views.decorators.cache import never_cache
from django_tenants.utils import tenant_context
from django.utils.translation import gettext_lazy as _

from maintenance.models import Maintenance
from maintenance.jeux_pieces.models import ControleJeuxPieces
from maintenance.jeux_pieces.forms import ControleJeuxPiecesForm
from voiture.voiture_exemplaire.models import VoitureExemplaire


@never_cache
@login_required
def controle_jeux_pieces_view(request, exemplaire_id):
    tenant = request.user.societe

    with tenant_context(tenant):
        exemplaire = get_object_or_404(
            VoitureExemplaire.objects.filter(
                Q(client__societe=tenant) | Q(client__isnull=True, societe=tenant)
            ),
            id=exemplaire_id
        )

        # Vérification des rôles autorisés
        roles_autorises = ["mécanicien", "apprenti", "magasinier", "chef mécanicien"]
        if request.user.role not in roles_autorises:
            messages.error(
                request,
                _("Seuls les mécaniciens, apprentis, magasiniers et chefs mécaniciens peuvent accéder à cette page.")
            )
            return redirect("maintenance_liste_all")

        # 🔧 Récupération ou création de la maintenance
        maintenance = Maintenance.objects.filter(
            voiture_exemplaire=exemplaire,
            type_maintenance="checkup"
        ).order_by("-date_intervention").first()

        if not maintenance:
            maintenance = Maintenance.objects.create(
                voiture_exemplaire=exemplaire,
                mecanicien=request.user,
                immatriculation=exemplaire.immatriculation,
                date_intervention=timezone.now().date(),
                kilometres_chassis=exemplaire.kilometres_chassis,
                kilometres_derniere_intervention=exemplaire.kilometres_derniere_intervention,
                type_maintenance="jeux_pieces",
                tag=Maintenance.Tag.JAUNE,
            )

        # 🔧 Récupération ou création du ControleJeuxPieces
        controle_jeux_pieces, _ = ControleJeuxPieces.objects.get_or_create(
            maintenance=maintenance
        )

        # ------------------- POST -------------------
        if request.method == "POST":
            form = ControleJeuxPiecesForm(
                instance=controle_jeux_pieces,
                initial={"kilometres_chassis": exemplaire.kilometres_chassis},
                user=request.user
            )

            if form.is_valid():  # ✅ appeler la méthode
                try:
                    with transaction.atomic():
                        form.save()  # la logique kilométrage est gérée dans le formulaire

                    messages.success(request, _("Contrôle des jeux enregistré avec succès."))
                    return redirect(reverse(
                        "jeux_pieces:controle_jeux_pieces_view",
                        args=[exemplaire.id]
                    ))

                except Exception as e:
                    messages.error(request, _("Erreur lors de l'enregistrement : ") + str(e))
            if not form.is_valid():
                print(form.errors)  # Affiche tous les messages d'erreur par champ
                messages.error(request, _("Le formulaire contient des erreurs : ") + str(form.errors))

        # ------------------- GET -------------------
        else:
            form = ControleJeuxPiecesForm(
                instance=controle_jeux_pieces,
                initial={"kilometres_chassis": exemplaire.kilometres_chassis},
                user=request.user  # ✅ passer l'utilisateur, pas la société
            )

        context = {
            "exemplaire": exemplaire,
            "maintenance": maintenance,
            "form": form,
            "now": timezone.now(),
        }

        return render(request, "jeux_pieces/controle_jeux.html", context)