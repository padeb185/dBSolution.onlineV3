from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST

from .models import Notification


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
