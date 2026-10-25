"""
Profil d'un utilisateur (consultation + édition) depuis la liste des utilisateurs.
Accès : super-admin et direction, uniquement pour les utilisateurs de leur société.
"""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext as _
from django.views.decorators.cache import never_cache

from .forms import AdresseUtilisateurForm, UtilisateurProfilForm
from .models import UserLog, Utilisateur
from .views_mon_compte import contexte_compte


def peut_gerer_utilisateurs(user):
    return user.is_authenticated and (user.is_superuser or getattr(user, "role", None) == "direction")


def _utilisateur_gere(request, pk):
    qs = Utilisateur.objects.select_related("adresse", "societe")
    societe = getattr(request.user, "societe", None)
    if societe is not None:
        qs = qs.filter(societe=societe)
    elif not request.user.is_superuser:
        qs = qs.none()
    if not request.user.is_superuser:
        qs = qs.exclude(is_superuser=True)
    return get_object_or_404(qs, pk=pk)


def _refuser(request):
    messages.error(request, _("Accès refusé"))
    return redirect("utilisateurs:dashboard")


@never_cache
@login_required
def utilisateur_profil(request, pk):
    if not peut_gerer_utilisateurs(request.user):
        return _refuser(request)
    utilisateur = _utilisateur_gere(request, pk)
    contexte = contexte_compte(utilisateur)
    contexte["vue_direction"] = True
    return render(request, "utilisateurs/mon_compte.html", contexte)


@never_cache
@login_required
def utilisateur_modifier(request, pk):
    if not peut_gerer_utilisateurs(request.user):
        return _refuser(request)
    utilisateur = _utilisateur_gere(request, pk)
    adresse = utilisateur.adresse

    if request.method == "POST":
        form = UtilisateurProfilForm(request.POST, instance=utilisateur, editeur=request.user)
        form_adresse = AdresseUtilisateurForm(request.POST, instance=adresse, prefix="adr")
        if form.is_valid() and form_adresse.is_valid():
            with transaction.atomic():
                obj = form.save()
                if not form_adresse.est_vide():
                    adr = form_adresse.save(commit=False)
                    if adr.societe_id is None:
                        adr.societe = obj.societe
                    adr.save()
                    if obj.adresse_id != adr.pk:
                        obj.adresse = adr
                        obj.save(update_fields=["adresse"])
                UserLog.objects.create(
                    utilisateur=request.user,
                    action=f"Modification du profil de {obj.prenom} {obj.nom}",
                )
            messages.success(request, _("Profil enregistré."))
            return redirect("utilisateurs:utilisateur_profil", pk=obj.pk)
        messages.error(request, _("Le formulaire contient des erreurs."))
    else:
        form = UtilisateurProfilForm(instance=utilisateur, editeur=request.user)
        form_adresse = AdresseUtilisateurForm(instance=adresse, prefix="adr")

    return render(request, "utilisateurs/utilisateur_modifier.html", {
        "utilisateur": utilisateur,
        "form": form,
        "form_adresse": form_adresse,
    })
