from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.utils import timezone
from django.views.decorators.cache import never_cache
from django.utils.translation import gettext_lazy as _
from utilisateurs.models import UserLog
from weasyprint import HTML
from .forms import MainDoeuvreForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import ProtectedError, RestrictedError
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import NoReverseMatch
from django.utils.translation import gettext as _, gettext_noop

from core.suppression import analyser_suppression
from .models import MainDoeuvre







@method_decorator(never_cache, name="dispatch")
class MainDoeuvreListView(LoginRequiredMixin, ListView):
    model = MainDoeuvre
    template_name = "maindoeuvre/main_oeuvre_list.html"
    context_object_name = "maindoeuvres"
    ordering = ["-date"]





@never_cache
@login_required
def main_oeuvre_form_view(request):
    tenant = request.user.societe

    roles_autorises = [
        "mécanicien"
        "chef mécanicien",
        "direction"
    ]

    if request.user.role not in roles_autorises:
        messages.error(
            request,
            _("Accès refusé.")
        )
        return redirect("maindoeuvre:main_oeuvre_list")

    if request.method == "POST":

        form = MainDoeuvreForm(request.POST)

        if form.is_valid():

            try:
                with transaction.atomic():

                    main_oeuvre = form.save(commit=False)

                    # Société
                    main_oeuvre.societe = tenant

                    # Utilisateur connecté
                    main_oeuvre.utilisateur = request.user

                    main_oeuvre.save()

                    messages.success(
                        request,
                        _("Main d'œuvre enregistrée avec succès.")
                    )
                    return redirect("maindoeuvre:main_oeuvre_list")

            except Exception as e:

                messages.error(
                    request,
                    _("Erreur lors de l'enregistrement : %(error)s") % {
                        "error": str(e)
                    }
                )

        else:

            print(form.errors)

            messages.error(
                request,
                _("Veuillez corriger les erreurs ci-dessous.")
            )

    else:

        form = MainDoeuvreForm(
            initial={
                "utilisateur": request.user,
                "temps_minutes": 0,
            }
        )

    sections = [
        {
            "title": _("Temps de travail"),
            "icon": "icons/main-doeuvre.png",
            "fields": [
                form["temps_minutes"],
            ],
        },
        {
            "title": _("Utilisateur"),
            "icon": "icons/user.png",
            "fields": [
                form["utilisateur"],
            ] if "utilisateur" in form.fields else [],
        },
    ]

    return render(
        request,
        "maindoeuvre/main_oeuvre_form.html",
        {
            "form": form,
            "sections": sections,
            "now": timezone.now(),
        },
    )




# ------------
# Vue détail boite
# -----------------------------
@login_required
def maindoeuvre_detail_view(request, main_oeuvre_id):
    maindoeuvre = get_object_or_404(
        MainDoeuvre.objects.select_related("societe", "utilisateur"),
        id=main_oeuvre_id
    )

    context = {
        "maindoeuvre": maindoeuvre,

    }
    return render(request, "maindoeuvre/main_oeuvre_detail.html", context)


@login_required
def modifier_maindoeuvre_view(request, main_oeuvre_id):
    tenant = request.user.societe


    maindoeuvre = get_object_or_404(
        MainDoeuvre.objects.select_related("societe", "utilisateur"),
        id=main_oeuvre_id
    )

    if request.method == "POST":
        form = MainDoeuvreForm(
            request.POST,
            instance=maindoeuvre,
            user=request.user
        )

        if form.is_valid():
            form.save()

            UserLog.objects.create(
                utilisateur=request.user,
                action=_("Modification de la main d'œuvre")
            )

            messages.success(request, _("Main d'œuvre modifiée avec succès !"))
            return redirect(
                "maindoeuvre:main_oeuvre_detail",
                main_oeuvre_id=maindoeuvre.id
            )
        else:
            messages.error(request, _("Le formulaire contient des erreurs."))
            print(form.errors)

    else:
        form = MainDoeuvreForm(
            instance=maindoeuvre,
            user=request.user
        )

    sections = [
        {
            "title": _("Temps de travail"),
            "icon": "icons/main_doeuvre.png",
            "fields": [
                form["temps_minutes"],
            ],
        },
        {
            "title": _("Utilisateur"),
            "icon": "icons/user.png",
            "fields": [
                form["utilisateur"],
            ] if "utilisateur" in form.fields else [],
        },
    ]

    return render(
        request,
        "maindoeuvre/modifier_maindoeuvre.html",
        {
            "form": form,
            "maindoeuvre": maindoeuvre,
            "sections": sections,
        }
    )

@login_required
def maindoeuvre_detail_pdf_view(request, id):
    maindoeuvre = get_object_or_404(MainDoeuvre, id=id)

    html_string = render_to_string(
        "maindoeuvre/main_oeuvre_detail_pdf.html",
        {"maindoeuvre": maindoeuvre},
        request=request
    )

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = (
        f'inline; filename="main_oeuvre_{maindoeuvre.id}.pdf"'
    )

    HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(response)
    return response






ACTION_SUPPRESSION_MAIN_OEUVRE = gettext_noop("Suppression de la main-d'œuvre")


def _redirect_apres_suppression(voiture_id):
    """Retour à la fiche du véhicule si possible, sinon à la liste."""
    if voiture_id:
        try:
            return redirect("voiture_exemplaire:detail", exemplaire_id=voiture_id)
        except NoReverseMatch:
            pass
    return redirect("maindoeuvre:main_oeuvre_list")


@login_required
def delete_main_oeuvre_view(request, pk):
    main_oeuvre = get_object_or_404(
        MainDoeuvre.objects.select_related("utilisateur", "voiture_exemplaire", "societe"),
        pk=pk,
    )

    analyse = analyser_suppression(main_oeuvre)
    objets_bloquants = analyse["bloquants"]
    objets_supprimes = analyse["supprimes"]

    if request.method == "POST":
        libelle = main_oeuvre.descriptif or main_oeuvre.temps_display
        voiture_id = main_oeuvre.voiture_exemplaire_id

        if objets_bloquants:
            messages.error(
                request,
                _("Impossible de supprimer « %(nom)s » : elle est encore utilisée ailleurs.") % {"nom": libelle},
            )
            return redirect("maindoeuvre:delete_main_oeuvre", pk=pk)

        # Libellé pour le log (capturé AVANT la suppression)
        voiture = str(main_oeuvre.voiture_exemplaire) if voiture_id else "—"
        mecanicien = str(main_oeuvre.utilisateur) if main_oeuvre.utilisateur_id else "—"
        date_mo = main_oeuvre.date.strftime("%d/%m/%Y") if main_oeuvre.date else "—"
        nom_log = (
            f"{libelle} – {voiture} – {mecanicien} – {date_mo} – "
            f"{main_oeuvre.temps_display} – {main_oeuvre.cout_total:.2f} €"
        )

        try:
            with transaction.atomic():
                main_oeuvre.delete()

                UserLog.objects.create(
                    utilisateur=request.user,
                    action=f"{ACTION_SUPPRESSION_MAIN_OEUVRE} : {nom_log}",
                )
        except (ProtectedError, RestrictedError):
            messages.error(
                request,
                _("Impossible de supprimer « %(nom)s » : elle est encore utilisée ailleurs.") % {"nom": libelle},
            )
            return redirect("maindoeuvre:delete_main_oeuvre", pk=pk)

        messages.success(request, _("La main-d'œuvre « %(nom)s » a bien été supprimée.") % {"nom": libelle})
        return _redirect_apres_suppression(voiture_id)

    return render(
        request,
        "maindoeuvre/delete_main_oeuvre.html",
        {
            "main_oeuvre": main_oeuvre,
            "objets_supprimes": objets_supprimes,
            "objets_bloquants": objets_bloquants,
        },
    )