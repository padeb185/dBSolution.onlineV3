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
from django.db.models import Q
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

        # Vérification rôles (même logique que ABS)
        roles_autorises = ["mécanicien", "apprenti", "magasinier", "chef mécanicien"]

        if request.user.role not in roles_autorises:
            messages.error(
                request,
                _("Accès refusé.")
            )
            return redirect("main_oeuvre_list")

        # Instance vide (création)
        main_oeuvre = MainDoeuvre(
            utilisateur=request.user,
            temps_minutes=0,
        )

        # --- FORM ---
        if request.method == "POST":
            form = MainDoeuvreForm(request.POST, instance=main_oeuvre)

            if form.is_valid():
                try:
                    with transaction.atomic():
                        main_oeuvre = form.save(commit=False)

                        # sécurité utilisateur (toujours forcé)
                        main_oeuvre.utilisateur = request.user

                        main_oeuvre.save()

                    messages.success(
                        request,
                        _("Main d'œuvre enregistrée avec succès.")
                    )


                except Exception as e:
                    messages.error(
                        request,
                        _("Erreur lors de l'enregistrement : %(error)s") % {"error": str(e)}
                    )
            else:
                messages.error(request, _("Le formulaire contient des erreurs."))

        else:
            form = MainDoeuvreForm(instance=main_oeuvre)

        # --- SECTIONS (style identique ABS) ---
        sections = [
            {
                "title": _("Temps de travail"),
                "icon": "icons/main-doeuvre.png",
                "fields": [form["temps_minutes"]],
            },
            {
                "title": _("Utilisateur"),
                "icon": "icons/user.png",
                "fields": [form["utilisateur"]] if "utilisateur" in form.fields else [],
            },
        ]

        return render(request, "maindoeuvre/main_oeuvre_form.html", {
            "form": form,
            "sections": sections,
            "now": timezone.now(),
        })