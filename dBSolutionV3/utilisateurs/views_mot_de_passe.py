"""
Mot de passe : « mot de passe oublié » (lien par e-mail), nouveau mot de passe,
changement par l'utilisateur connecté, envoi d'un lien de réinitialisation par la direction.

Les pages publiques sont sous /connexion/… (exclues des contrôles tenant / TOTP).
"""
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.crypto import get_random_string
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST

from .models import Utilisateur, UserLog
from .mot_de_passe import (ChangementMotDePasseForm, NouveauMotDePasseForm, ReinitialisationForm,
                           adresse_recuperation)

MAX_DEMANDES = 5               # demandes de lien…
FENETRE_SECONDES = 15 * 60     # …par adresse IP et par période de 15 minutes
ROLES_REINITIALISATION = ("direction",)

GABARITS_EMAIL = {
    "email_template_name": "utilisateurs/mot_de_passe/email_reinitialisation.txt",
    "html_email_template_name": "utilisateurs/mot_de_passe/email_reinitialisation.html",
    "subject_template_name": "utilisateurs/mot_de_passe/email_reinitialisation_sujet.txt",
}


def _ip(request):
    transmis = request.META.get("HTTP_X_FORWARDED_FOR", "")
    return (transmis.split(",")[0].strip() if transmis else request.META.get("REMOTE_ADDR", "")) or "inconnue"


class MotDePasseOublieView(auth_views.PasswordResetView):
    form_class = ReinitialisationForm
    template_name = "utilisateurs/mot_de_passe/oublie.html"
    success_url = reverse_lazy("password_reset_done")
    email_template_name = GABARITS_EMAIL["email_template_name"]
    html_email_template_name = GABARITS_EMAIL["html_email_template_name"]
    subject_template_name = GABARITS_EMAIL["subject_template_name"]

    def form_valid(self, form):
        cle = f"mdp_oublie_ip_{_ip(self.request)}"
        if (cache.get(cle) or 0) >= MAX_DEMANDES:
            form.add_error(None, _("Trop de demandes. Réessayez dans quelques minutes."))
            return self.form_invalid(form)
        try:
            cache.incr(cle)
        except ValueError:
            cache.set(cle, 1, FENETRE_SECONDES)
        return super().form_valid(form)


class MotDePasseOublieEnvoyeView(auth_views.PasswordResetDoneView):
    template_name = "utilisateurs/mot_de_passe/oublie_envoye.html"


class NouveauMotDePasseView(auth_views.PasswordResetConfirmView):
    form_class = NouveauMotDePasseForm
    template_name = "utilisateurs/mot_de_passe/nouveau.html"
    success_url = reverse_lazy("password_reset_complete")

    def form_valid(self, form):
        reponse = super().form_valid(form)
        UserLog.objects.create(utilisateur=form.user, action="Réinitialisation du mot de passe (lien e-mail)")
        return reponse


class NouveauMotDePasseTermineView(auth_views.PasswordResetCompleteView):
    template_name = "utilisateurs/mot_de_passe/nouveau_termine.html"


class ChangerMotDePasseView(auth_views.PasswordChangeView):
    form_class = ChangementMotDePasseForm
    template_name = "utilisateurs/mot_de_passe/changer.html"
    success_url = reverse_lazy("password_change_done")

    def form_valid(self, form):
        reponse = super().form_valid(form)
        UserLog.objects.create(utilisateur=self.request.user, action="Changement du mot de passe")
        return reponse


class ChangerMotDePasseTermineView(auth_views.PasswordChangeDoneView):
    template_name = "utilisateurs/mot_de_passe/changer_termine.html"


@login_required
@require_POST
def envoyer_lien_reinitialisation(request, pk):
    """La direction envoie à un utilisateur de sa société un lien pour (re)définir son mot de passe."""
    if not (request.user.is_superuser or getattr(request.user, "role", None) in ROLES_REINITIALISATION):
        messages.error(request, _("Accès refusé"))
        return redirect("utilisateurs:liste_utilisateurs")

    filtre = {} if request.user.is_superuser else {"societe": request.user.societe}
    utilisateur = get_object_or_404(Utilisateur, pk=pk, **filtre)
    adresse = adresse_recuperation(utilisateur)
    if not adresse or not utilisateur.is_active:
        messages.error(request, _("Cet utilisateur n'a pas d'adresse e-mail ou son compte est désactivé."))
        return redirect("utilisateurs:liste_utilisateurs")

    if not utilisateur.has_usable_password():
        # compte sans mot de passe utilisable : mot de passe aléatoire, le lien permet d'en définir un
        utilisateur.set_password(get_random_string(32))
        utilisateur.save(update_fields=["password"])

    form = ReinitialisationForm({"email": utilisateur.email or utilisateur.email_entreprise})
    if form.is_valid():
        form.save(request=request, use_https=request.is_secure(), **GABARITS_EMAIL)
        UserLog.objects.create(
            utilisateur=request.user,
            action=f"Envoi d'un lien de réinitialisation du mot de passe - {utilisateur.prenom} {utilisateur.nom}",
        )
        messages.success(request, _("Lien de réinitialisation envoyé à %(email)s.") % {"email": adresse})
    return redirect("utilisateurs:liste_utilisateurs")
