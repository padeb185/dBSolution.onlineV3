from django.db.models import Sum
from django.urls import NoReverseMatch, reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from proprietaire.models import  ProprietaireVoiture
from django.utils.translation import gettext_lazy as _
from adresse.models import Adresse
from django.http import JsonResponse
from utilisateurs.models import UserLog
from .forms import ProprietaireForm, ProprietaireVoitureForm
from adresse.forms import AdresseForm
from django.views.decorators.cache import never_cache
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import ProtectedError, RestrictedError
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext as _, gettext_noop

from core.suppression import analyser_suppression, masquer
from .models import Proprietaire





@never_cache
@login_required
def proprietaire_dashboard_view(request):
    user = request.user


    total_proprietaire = 0
    total_voiture_cop = 0
    proprietaire = Proprietaire.objects.none()
    proprietaire_voiture = ProprietaireVoiture.objects.none()

    # Chargement des données
    proprietaire = Proprietaire.objects.all()
    proprietaire_voiture = ProprietaireVoiture.objects.all()

    total_proprietaire = proprietaire.count()
    total_voiture_cop = proprietaire_voiture.count()

    context = {
        "user": user,
        "societe": getattr(user, "societe", None),
        "total_proprietaire": total_proprietaire,
        "total_voiture_cop": total_voiture_cop,
        "proprietaire": proprietaire,
        "proprietaire_voiture": proprietaire_voiture,
    }

    return render(
        request,
        "proprietaire/proprietaire_dashboard.html",
        context,
    )


@method_decorator([login_required, never_cache], name='dispatch')
class ProprietaireListView(ListView):
    model = Proprietaire
    template_name = "proprietaire/proprietaire_list.html"
    context_object_name = "proprietaires"
    ordering = ["nom", "prenom"]

    def get_queryset(self):
        user = self.request.user

        if not hasattr(user, "societe") or user.societe is None:
            return Proprietaire.objects.none()

        return Proprietaire.objects.filter(societe=user.societe)




@login_required
def proprietaire_form_view(request):
    tenant = request.user.societe

    if request.method == "POST":
        form = ProprietaireForm(request.POST)

        adresse_instance = Adresse(societe=tenant)
        adresse_form = AdresseForm(request.POST, instance=adresse_instance)

        if form.is_valid() and adresse_form.is_valid():

            adresse = adresse_form.save(commit=False)
            adresse.societe = tenant
            adresse.save()

            proprietaire = form.save(commit=False)
            proprietaire.societe = tenant
            proprietaire.adresse = adresse
            proprietaire.save()

            messages.success(
                request,
                _("Propriétaire '%(prenom)s %(nom)s' ajouté avec succès !") % {
                    "prenom": proprietaire.prenom,
                    "nom": proprietaire.nom
                }
            )

            return redirect(
                f"{reverse('proprietaire:proprietaire_list')}?saved=1"
            )


        else:
            messages.error(request, _("Veuillez corriger les erreurs du formulaire."))

    else:
        form = ProprietaireForm()
        adresse_form = AdresseForm()

    return render(
        request,
        "proprietaire/proprietaire_form.html",
        {
            "form": form,
            "adresse_form": adresse_form,
            "tenant": tenant,
        }
    )




@never_cache
@login_required
def proprietaire_detail_view(request, proprietaire_id):
    tenant = request.user.societe


    proprietaire = get_object_or_404(Proprietaire, id=proprietaire_id)
    adresse = proprietaire.adresse  # si tu veux l’afficher séparément

    return render(request, "proprietaire/proprietaire_detail.html", {
        "proprietaire": proprietaire,
        "adresse": adresse,
    })



@login_required
def modifier_proprietaire_view(request, proprietaire_id):
    tenant = request.user.societe


    proprietaire = get_object_or_404(Proprietaire, id=proprietaire_id)

    if request.method == "POST":
        form = ProprietaireForm(request.POST, instance=proprietaire)
        if form.is_valid():
            form.save()
            messages.success(request, _(f"Client '{proprietaire.prenom} {proprietaire.nom}' modifié avec succès !"))
            return redirect("proprietaire:proprietaire_detail", proprietaire_id=proprietaire.id)

        else:
            # Ici, si la carte bancaire est invalide, Django affichera automatiquement l'erreur
            messages.error(request, _("Veuillez corriger les erreurs dans le formulaire."))
    else:
        form = ProprietaireForm(instance=proprietaire)

    return render(
        request,
        "proprietaire/modifier_proprietaire.html",
        {
            "form": form,
            "proprietaire": proprietaire,
        }
    )





@method_decorator([login_required, never_cache], name='dispatch')
class ProprietaireVoitureListView(ListView):
    model = Proprietaire
    template_name = "proprietaire/proprietaire_voiture_list.html"
    context_object_name = "proprietaire_voitures"
    ordering = ["proprietaire_voitures"]

    def get_queryset(self):
        user = self.request.user

        if not hasattr(user, "societe") or user.societe is None:
            return ProprietaireVoiture.objects.none()

        return ProprietaireVoiture.objects.filter(societe=user.societe)




@login_required
def proprietaire_voiture_form_view(request):
    tenant = request.user.societe

    if request.method == "POST":
        form = ProprietaireVoitureForm(request.POST)

        if form.is_valid():

            proprietaire_voiture = form.save(commit=False)
            proprietaire_voiture.societe = tenant
            proprietaire_voiture.save()

            messages.success(
                request,
                _("Lien propriétaire / voiture ajouté avec succès !")
            )
            return redirect(
                "proprietaire:proprietaire_voiture_list")


        else:
            messages.error(
                request,
                _("Veuillez corriger les erreurs du formulaire.")
            )

    else:
        form = ProprietaireVoitureForm()

    return render(
        request,
        "proprietaire/proprietaire_voiture_form.html",
        {
            "form": form,
            "tenant": tenant,
        }
    )




def total_part_voiture(request, voiture_id):
    total = (
        ProprietaireVoiture.objects
        .filter(voiture_exemplaire_id=voiture_id)
        .aggregate(total=Sum("part_proprietaire_pourcent"))
        ["total"] or 0
    )

    return JsonResponse({"total": total})


@login_required
def proprietaire_voiture_detail_view(request, proprietaire_voiture_id):
    tenant = request.user.societe


    proprietaire_voiture = get_object_or_404(ProprietaireVoiture, id=proprietaire_voiture_id)
    adresse = proprietaire_voiture.proprietaire.adresse

    return render(
        request,
        "proprietaire/proprietaire_voiture_detail.html",
        {
            "proprietaire_voiture": proprietaire_voiture,
            "adresse": adresse,
        },
    )



@login_required
def modifier_proprietaire_voiture_view(request, proprietaire_voiture_id):
    tenant = request.user.societe

    proprietaire_voiture = get_object_or_404(
        ProprietaireVoiture,
        id=proprietaire_voiture_id
    )

    if request.method == "POST":
        form_proprietaire_voiture = ProprietaireVoitureForm(
            request.POST,
            instance=proprietaire_voiture
        )

        if form_proprietaire_voiture.is_valid():  # ✅ corrigé
            proprietaire_voiture = form_proprietaire_voiture.save()

            messages.success(
                request,
                _("Propriété mise à jour avec succès.")
            )
            return redirect("proprietaire:propriétaire_voiture_detail", proprietaire_voiture_id=proprietaire_voiture.id)

        else:
            messages.error(request, _("Le formulaire contient des erreurs."))

    else:
        form_proprietaire_voiture = ProprietaireVoitureForm(
            instance=proprietaire_voiture
        )

    return render(
        request,
        "proprietaire/modifier_proprietaire_voiture.html",
        {
            "form": form_proprietaire_voiture,
            "proprietaire_voiture": proprietaire_voiture,
        }
    )





ACTION_SUPPRESSION_PROPRIETAIRE = gettext_noop("Suppression du propriétaire")


@login_required
def delete_proprietaire_view(request, pk):
    proprietaire = get_object_or_404(
        Proprietaire.objects.select_related("adresse", "societe"),
        pk=pk,
    )

    parts = list(
        proprietaire.proprietaire_voitures
        .select_related("voiture_exemplaire")
        .order_by("voiture_exemplaire__id")
    )

    analyse = analyser_suppression(proprietaire)
    objets_bloquants = analyse["bloquants"]
    # Les parts (ProprietaireVoiture) sont affichées à part, avec les véhicules et les %
    objets_supprimes = [
        (label, objets) for label, objets in analyse["supprimes"]
        if not (objets and objets[0].__class__.__name__ == "ProprietaireVoiture")
    ]

    if request.method == "POST":
        nom_complet = f"{proprietaire.nom} {proprietaire.prenom}"

        if objets_bloquants:
            messages.error(
                request,
                _("Impossible de supprimer « %(nom)s » : ce propriétaire est encore utilisé ailleurs.") % {"nom": nom_complet},
            )
            return redirect("proprietaire:delete_proprietaire", pk=pk)

        # Libellé pour le log (capturé AVANT la suppression) — sans données sensibles
        nom_log = nom_complet


        try:
            with transaction.atomic():
                adresse = proprietaire.adresse
                proprietaire.delete()  # supprime aussi ses parts (ProprietaireVoiture, CASCADE)

                # L'adresse est supprimée avec le propriétaire
                if adresse:
                    adresse.delete()

                UserLog.objects.create(
                    utilisateur=request.user,
                    action=f"{ACTION_SUPPRESSION_PROPRIETAIRE} : {nom_log}",
                )
        except (ProtectedError, RestrictedError):
            messages.error(
                request,
                _("Impossible de supprimer « %(nom)s » : le propriétaire ou son adresse est encore utilisé ailleurs.") % {"nom": nom_complet},
            )
            return redirect("proprietaire:delete_proprietaire", pk=pk)

        messages.success(request, _("Le propriétaire « %(nom)s » a bien été supprimé.") % {"nom": nom_complet})
        return redirect("proprietaire:proprietaire_list")

    return render(
        request,
        "proprietaire/delete_proprietaire.html",
        {
            "proprietaire": proprietaire,
            "parts": parts,
            "objets_supprimes": objets_supprimes,
            "objets_bloquants": objets_bloquants,
            # Données sensibles masquées pour l'affichage
            "carte_id_masquee": masquer(proprietaire.numero_carte_id, 3),
            "compte_masque": masquer(proprietaire.numero_compte),
            "carte_bancaire_masquee": masquer(proprietaire.numero_carte_bancaire),
        },
    )






from decimal import Decimal



ACTION_SUPPRESSION_PART = gettext_noop("Suppression de la part de propriété")


def _redirect_premier(*candidats):
    """Essaie chaque (nom_url, kwargs) dans l'ordre ; retourne le premier qui existe."""
    for nom_url, kwargs in candidats:
        try:
            return redirect(nom_url, **kwargs)
        except NoReverseMatch:
            continue
    return redirect("/")


@login_required
def delete_proprietaire_voiture_view(request, pk):
    part = get_object_or_404(
        ProprietaireVoiture.objects.select_related("proprietaire", "voiture_exemplaire", "societe"),
        pk=pk,
    )

    # Autres copropriétaires du même véhicule
    autres_parts = list(
        ProprietaireVoiture.objects
        .filter(voiture_exemplaire_id=part.voiture_exemplaire_id)
        .exclude(pk=part.pk)
        .select_related("proprietaire")
        .order_by("-part_proprietaire_pourcent")
    )
    total_autres = sum((p.part_proprietaire_pourcent or Decimal("0")) for p in autres_parts)
    total_avant = total_autres + (part.part_proprietaire_pourcent or Decimal("0"))

    analyse = analyser_suppression(part)
    objets_bloquants = analyse["bloquants"]
    objets_supprimes = analyse["supprimes"]

    if request.method == "POST":
        proprietaire_nom = f"{part.proprietaire.nom} {part.proprietaire.prenom}"
        voiture_libelle = str(part.voiture_exemplaire)
        libelle = f"{proprietaire_nom} – {voiture_libelle}"
        voiture_id = part.voiture_exemplaire_id
        proprietaire_id = part.proprietaire_id

        if objets_bloquants:
            messages.error(
                request,
                _("Impossible de supprimer la part « %(nom)s » : elle est encore utilisée ailleurs.") % {"nom": libelle},
            )
            return redirect("proprietaire:delete_proprietaire_voiture", pk=pk)

        nom_log = f"{libelle} ({part.part_proprietaire_pourcent:.2f} %)"

        try:
            with transaction.atomic():
                part.delete()

                UserLog.objects.create(
                    utilisateur=request.user,
                    action=f"{ACTION_SUPPRESSION_PART} : {nom_log}",
                )
        except (ProtectedError, RestrictedError):
            messages.error(
                request,
                _("Impossible de supprimer la part « %(nom)s » : elle est encore utilisée ailleurs.") % {"nom": libelle},
            )
            return redirect("proprietaire:delete_proprietaire_voiture", pk=pk)

        messages.success(
            request,
            _("La part de « %(proprietaire)s » sur « %(voiture)s » a bien été supprimée.") % {
                "proprietaire": proprietaire_nom,
                "voiture": voiture_libelle,
            },
        )
        return _redirect_premier(
            ("voiture_exemplaire:detail", {"exemplaire_id": voiture_id}),
            ("proprietaire:proprietaire_detail", {"pk": proprietaire_id}),
            ("proprietaire:proprietaire_list", {}),
        )

    return render(
        request,
        "proprietaire/delete_proprietaire_voiture.html",
        {
            "part": part,
            "autres_parts": autres_parts,
            "total_avant": total_avant,
            "total_apres": total_autres,
            "objets_supprimes": objets_supprimes,
            "objets_bloquants": objets_bloquants,
        },
    )