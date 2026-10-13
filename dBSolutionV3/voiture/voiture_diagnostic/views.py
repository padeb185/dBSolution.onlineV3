from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Prefetch, ProtectedError
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.translation import gettext as _
from django.views.decorators.cache import never_cache

from .forms import DiagnosticCodeFormSet, DiagnosticForm
from .models import Diagnostic, DiagnosticCode

# Mêmes autorisations que les maintenances (ex. checkup piste)
ROLES_LECTURE_ECRITURE = ["mecanicien", "apprenti", "magasinier", "chef_mecanicien", "direction"]
ROLES_SUPPRESSION = ["direction", "chef_mecanicien"]


def _autorise(user, roles):
    return user.is_superuser or getattr(user, "role", None) in roles


def _refus(request, message=None):
    messages.error(request, message or _("Accès refusé"))
    return redirect("utilisateurs:dashboard")


def _queryset(request):
    return (
        Diagnostic.objects
        .filter(societe=request.user.societe)
        .select_related(
            "voiture_exemplaire__voiture_marque",
            "voiture_exemplaire__voiture_modele",
            "main_oeuvre__utilisateur",
        )
        .prefetch_related(
            Prefetch("codes", queryset=DiagnosticCode.objects.order_by("ordre", "code_defaut")),
            "factures",
        )
    )


def _enregistrer(form, formset):
    """Enregistre le diagnostic et ses codes défaut dans une seule transaction."""
    with transaction.atomic():
        diagnostic = form.save()
        formset.instance = diagnostic
        codes = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for code in codes:
            code.diagnostic = diagnostic
            code.save()
        # Ordre d'affichage = ordre de saisie
        for i, f in enumerate(f for f in formset.forms if f.instance.pk and not f.cleaned_data.get("DELETE")):
            DiagnosticCode.objects.filter(pk=f.instance.pk).update(ordre=i)
    return diagnostic


@never_cache
@login_required
def diagnostic_liste(request):
    if not _autorise(request.user, ROLES_LECTURE_ECRITURE):
        return _refus(request, _(
            "Seuls les mécaniciens, apprentis, magasiniers "
            "et chefs mécaniciens peuvent accéder à cette page."
        ))

    return render(request, "voiture_diagnostic/diagnostic_list.html", {
        "diagnostics": _queryset(request),
        "peut_supprimer": _autorise(request.user, ROLES_SUPPRESSION),
    })


@never_cache
@login_required
def diagnostic_ajouter(request):
    if not _autorise(request.user, ROLES_LECTURE_ECRITURE):
        return _refus(request)

    initial = {}
    if request.GET.get("voiture_exemplaire"):
        initial["voiture_exemplaire"] = request.GET["voiture_exemplaire"]

    form = DiagnosticForm(request.POST or None, user=request.user, initial=initial)
    formset = DiagnosticCodeFormSet(request.POST or None, instance=Diagnostic(), prefix="codes")
    if request.GET.get("code_defaut") and not request.POST:
        formset = DiagnosticCodeFormSet(instance=Diagnostic(), prefix="codes",
                                        initial=[{"code_defaut": request.GET["code_defaut"]}])

    if request.method == "POST" and form.is_valid() and formset.is_valid():
        diagnostic = _enregistrer(form, formset)
        messages.success(request, _("Diagnostic '%(code)s' créé avec succès.") % {"code": diagnostic.liste_codes})
        return redirect("voiture_diagnostic:diagnostic_liste")

    return render(request, "voiture_diagnostic/diagnostic_form.html", {
        "form": form,
        "formset": formset,
        "diagnostic": None,
    })


@never_cache
@login_required
def diagnostic_modifier(request, diagnostic_id):
    if not _autorise(request.user, ROLES_LECTURE_ECRITURE):
        return _refus(request)

    diagnostic = get_object_or_404(_queryset(request), id=diagnostic_id)
    form = DiagnosticForm(request.POST or None, instance=diagnostic, user=request.user)
    formset = DiagnosticCodeFormSet(request.POST or None, instance=diagnostic, prefix="codes")
    if request.method == "POST" and form.is_valid() and formset.is_valid():
        diagnostic = _enregistrer(form, formset)
        messages.success(request, _("Diagnostic '%(code)s' mis à jour.") % {"code": diagnostic.liste_codes})
        return redirect("voiture_diagnostic:diagnostic_detail", diagnostic_id=diagnostic.id)

    return render(request, "voiture_diagnostic/diagnostic_form.html", {
        "form": form,
        "formset": formset,
        "diagnostic": diagnostic,
    })


@never_cache
@login_required
def diagnostic_supprimer(request, diagnostic_id):
    if not _autorise(request.user, ROLES_SUPPRESSION):
        return _refus(request)

    diagnostic = get_object_or_404(_queryset(request), id=diagnostic_id)
    if request.method == "POST":
        try:
            diagnostic.delete()
            messages.success(request, _("Diagnostic supprimé."))
        except ProtectedError:
            messages.error(request, _("Impossible de supprimer ce diagnostic."))
        return redirect("voiture_diagnostic:diagnostic_liste")

    return render(request, "voiture_diagnostic/diagnostic_confirm_delete.html", {"diagnostic": diagnostic})


@never_cache
@login_required
def diagnostic_detail(request, diagnostic_id):
    if not _autorise(request.user, ROLES_LECTURE_ECRITURE):
        return _refus(request)
    diagnostic = get_object_or_404(_queryset(request), id=diagnostic_id)
    return render(request, "voiture_diagnostic/diagnostic_detail.html", {
        "diagnostic": diagnostic,
        "exemplaire": diagnostic.voiture_exemplaire,
        "peut_supprimer": _autorise(request.user, ROLES_SUPPRESSION),
        "peut_facturer": _autorise(request.user, ["direction", "chef_mecanicien", "comptable"]),
    })


@login_required
def diagnostic_pdf(request, diagnostic_id):
    if not _autorise(request.user, ROLES_LECTURE_ECRITURE):
        return _refus(request)
    from weasyprint import HTML

    diagnostic = get_object_or_404(
        _queryset(request).select_related("societe", "societe__adresse"), id=diagnostic_id
    )
    html = render_to_string(
        "voiture_diagnostic/diagnostic_pdf.html",
        {
            "diagnostic": diagnostic,
            "exemplaire": diagnostic.voiture_exemplaire,
            "societe": diagnostic.societe,
            "date_export": timezone.now(),
        },
        request=request,
    )
    pdf = HTML(string=html, base_url=request.build_absolute_uri("/")).write_pdf()

    immat = getattr(diagnostic.voiture_exemplaire, "immatriculation", "") or "sans_immatriculation"
    nom_fichier = f"{_('Diagnostic')}_{immat}_{diagnostic.date_diagnostic:%Y-%m-%d}.pdf".replace(" ", "_")
    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = f'inline; filename="{nom_fichier}"'
    return response
