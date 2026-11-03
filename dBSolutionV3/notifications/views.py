from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST

from utils.securite import roles_requis

from .forms import ParametresNotificationsForm, PreferencesNotificationsForm
from .models import (Notification, ParametresNotifications, PreferenceNotification, RegleNotification,
                     TYPES_PARAMETRABLES)
from .services import adresse_email, diagnostic, expediteur


@login_required
def liste(request):
    qs = Notification.objects.filter(destinataire=request.user).select_related("emetteur")
    filtre = request.GET.get("filtre", "")
    if filtre == "non_lues":
        qs = qs.filter(lue=False)
    elif filtre in Notification.Type.values:
        qs = qs.filter(type=filtre)
    page = Paginator(qs, 25).get_page(request.GET.get("page"))
    return render(request, "notifications/liste.html", {
        "page": page, "filtre": filtre, "types": Notification.Type.choices,
        "nb_non_lues": Notification.objects.filter(destinataire=request.user, lue=False).count(),
        "peut_parametrer": _peut_parametrer(request.user),
    })


@login_required
def ouvrir(request, pk):
    """Marque la notification comme lue et renvoie vers sa raison (maintenance, facture, achat…)."""
    n = get_object_or_404(Notification, pk=pk, destinataire=request.user)
    if not n.lue:
        n.lue, n.lue_le = True, timezone.now()
        n.save(update_fields=["lue", "lue_le"])
    lien = n.lien()
    if lien and url_has_allowed_host_and_scheme(lien, allowed_hosts={request.get_host()}):
        return redirect(lien)
    messages.info(request, _("Cette notification n'a pas de page liée."))
    return redirect("notifications:liste")


@login_required
@require_POST
def marquer(request, pk):
    n = get_object_or_404(Notification, pk=pk, destinataire=request.user)
    n.lue = not n.lue
    n.lue_le = timezone.now() if n.lue else None
    n.save(update_fields=["lue", "lue_le"])
    return redirect(request.POST.get("retour") or "notifications:liste")


@login_required
@require_POST
def tout_lire(request):
    nb = Notification.objects.filter(destinataire=request.user, lue=False).update(lue=True, lue_le=timezone.now())
    messages.success(request, _("%(n)s notification(s) marquée(s) comme lue(s).") % {"n": nb})
    return redirect("notifications:liste")


def _peut_parametrer(user):
    return getattr(user, "is_superuser", False) or getattr(user, "role", None) == "direction"


@login_required
@roles_requis("direction")
def parametres(request):
    """Direction : qui reçoit quoi, par quel canal, et expéditeur des e-mails."""
    regles = {t: RegleNotification.pour(t) for t in TYPES_PARAMETRABLES}
    param = ParametresNotifications.charger()
    form = ParametresNotificationsForm(
        request.POST or None, regles=regles,
        initial={"nom_expediteur": param.nom_expediteur, "email_reponse": param.email_reponse,
                 "notifier_auteur": param.notifier_auteur})
    if request.method == "POST" and form.is_valid():
        d = form.cleaned_data
        param.nom_expediteur, param.email_reponse = d["nom_expediteur"].strip(), d["email_reponse"]
        param.notifier_auteur = d["notifier_auteur"]
        param.save()
        for t, r in regles.items():
            r.actif, r.canal_app, r.canal_email = d[f"{t}_actif"], d[f"{t}_app"], d[f"{t}_email"]
            r.roles = list(d[f"{t}_roles"])
            r.save()
        messages.success(request, _("Paramètres des notifications enregistrés."))
        return redirect("notifications:parametres")
    return render(request, "notifications/parametres.html", {
        "form": form, "diag": diagnostic(request.user, getattr(request, "tenant", None)),
        "adresse": adresse_email(request.user)})


@login_required
@roles_requis("direction")
@require_POST
def tester(request):
    """Envoie une notification de test à l'utilisateur connecté (application + e-mail)."""
    from django.conf import settings
    from django.core.mail import EmailMessage
    n = Notification.objects.create(
        destinataire=request.user, emetteur=None, type=Notification.Type.AUTRE,
        titre=_("Notification de test"), message=_("Si vous voyez ceci, les notifications fonctionnent."),
        url_name="notifications:parametres")
    adresse = adresse_email(request.user)
    if adresse:
        param = ParametresNotifications.charger()
        try:
            EmailMessage(f"[CarsCosts] {n.titre}", n.message, expediteur(param), [adresse],
                         reply_to=[param.email_reponse] if param.email_reponse else None).send()
            Notification.objects.filter(pk=n.pk).update(email_envoye=True)
            messages.success(request, _("Notification de test créée et e-mail envoyé à %(adresse)s.") % {"adresse": adresse})
        except Exception as exc:
            messages.error(request, _("Notification créée, mais l'e-mail n'est pas parti : %(erreur)s") % {"erreur": exc})
    else:
        messages.success(request, _("Notification de test créée (aucune adresse e-mail sur votre profil)."))
    return redirect("notifications:parametres")


@login_required
def preferences(request):
    """Chaque utilisateur : couper l'application ou l'e-mail pour les types qui le concernent."""
    role = getattr(request.user, "role", None)
    types = [(t, r) for t, r in ((t, RegleNotification.pour(t)) for t in TYPES_PARAMETRABLES)
             if r.actif and role in r.roles and (r.canal_app or r.canal_email)]
    prefs = {p.type: p for p in PreferenceNotification.objects.filter(utilisateur=request.user)}
    form = PreferencesNotificationsForm(request.POST or None, types=types, prefs=prefs)
    if request.method == "POST" and form.is_valid():
        d = form.cleaned_data
        for t, regle in types:
            p = prefs.get(t) or PreferenceNotification(utilisateur=request.user, type=t)
            if regle.canal_app:
                p.recevoir_app = d.get(f"{t}_app", False)
            if regle.canal_email:
                p.recevoir_email = d.get(f"{t}_email", False)
            p.save()
        messages.success(request, _("Vos préférences ont été enregistrées."))
        return redirect("notifications:preferences")
    return render(request, "notifications/preferences.html", {
        "form": form, "adresse": adresse_email(request.user), "peut_parametrer": _peut_parametrer(request.user),
    })
