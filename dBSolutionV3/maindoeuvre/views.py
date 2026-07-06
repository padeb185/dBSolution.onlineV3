from datetime import datetime

from django.http import HttpResponse
from django.template.loader import render_to_string

from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django_tenants.utils import tenant_context
from maindoeuvre.models import MainDoeuvre
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from django.db import transaction
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from utilisateurs.models import UserLog
from weasyprint import HTML
from .models import MainDoeuvre
from .forms import MainDoeuvreForm




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

    with tenant_context(tenant):

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

    with tenant_context(tenant):
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
def maindoeuvre_detail_pdf_view(request, main_oeuvre_id):
    maindoeuvre = get_object_or_404(MainDoeuvre, id=main_oeuvre_id)

    context = {
        "maindoeuvre": maindoeuvre,
    }

    html = render_to_string(
        "maindoeuvre/main_oeuvre_detail_pdf.html",
        context,
        request=request
    )

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = (
        f'inline; filename="main_oeuvre_{maindoeuvre.id}.pdf"'
    )

    HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(response)
    return response