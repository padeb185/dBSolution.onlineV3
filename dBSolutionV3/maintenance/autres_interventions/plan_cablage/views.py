"""Plan de câblage d'un véhicule : boîtier électronique, connecteurs (branches) et fils."""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.utils.text import slugify
from django.utils.translation import gettext as _, gettext_noop
from django.views.decorators.cache import never_cache

from utils.securite import ROLES_ATELIER, peut_supprimer, refuser_suppression, roles_requis
from voiture.voiture_exemplaire.models import VoitureExemplaire

from .forms import ConnecteurCablageForm, FilFormSet, PlanCablageForm
from .models import COULEURS_HEX, ConnecteurCablage, CouleurFil, PlanCablage

# Consultation : atelier + vendeurs / comptables (lecture) ; modification : atelier
ROLES_LECTURE = ROLES_ATELIER + ("vendeur", "comptable")
atelier = roles_requis(*ROLES_ATELIER)
lecture = roles_requis(*ROLES_LECTURE)


def _log(user, action, objet):
    from utilisateurs.models import UserLog
    UserLog.objects.create(utilisateur=user, action=f"{action} : {objet}"[:255])


def _exemplaire(request, exemplaire_id):
    return get_object_or_404(
        VoitureExemplaire.objects.filter(societe=request.user.societe).select_related("voiture_marque", "voiture_modele"),
        id=exemplaire_id,
    )


def _plans(request):
    return PlanCablage.objects.filter(voiture_exemplaire__societe=request.user.societe).select_related(
        "voiture_exemplaire", "voiture_exemplaire__voiture_modele", "voiture_exemplaire__voiture_marque")


def _peut_modifier(user):
    return user.is_superuser or getattr(user, "role", None) in ROLES_ATELIER


# ------------------------------------------------------------------ liste
@never_cache
@login_required
@lecture
def plan_liste(request, exemplaire_id):
    exemplaire = _exemplaire(request, exemplaire_id)
    plans = (PlanCablage.objects.filter(voiture_exemplaire=exemplaire)
             .prefetch_related("connecteurs__fils"))
    return render(request, "plan_cablage/liste.html", {
        "exemplaire": exemplaire, "plans": plans, "peut_modifier": _peut_modifier(request.user),
    })


# ------------------------------------------------------------------ plan (boîtier)
def _plan_form(request, exemplaire, plan=None):
    form = PlanCablageForm(request.POST or None, instance=plan)
    if request.method == "POST" and form.is_valid():
        obj = form.save(commit=False)
        obj.voiture_exemplaire = exemplaire
        obj.societe = request.user.societe
        if not obj.cree_par_id:
            obj.cree_par = request.user
        obj.save()
        _log(request.user, gettext_noop("Plan de câblage") if plan is None else gettext_noop("Modification du plan de câblage"), obj)
        messages.success(request, _("Plan de câblage « %(p)s » enregistré.") % {"p": obj})
        return redirect("plan_cablage:plan_detail", pk=obj.pk)
    return render(request, "plan_cablage/plan_form.html", {"form": form, "exemplaire": exemplaire, "plan": plan})


@never_cache
@login_required
@atelier
def plan_ajouter(request, exemplaire_id):
    return _plan_form(request, _exemplaire(request, exemplaire_id))


@never_cache
@login_required
@atelier
def plan_modifier(request, pk):
    plan = get_object_or_404(_plans(request), pk=pk)
    return _plan_form(request, plan.voiture_exemplaire, plan)


def _contexte_detail(plan):
    connecteurs = list(plan.connecteurs.prefetch_related("fils"))
    return {
        "plan": plan, "exemplaire": plan.voiture_exemplaire, "connecteurs": connecteurs,
        "nb_fils": sum(len(c.fils.all()) for c in connecteurs),
        "longueur_totale_m": round(sum((c.longueur_cm or 0) * len(c.fils.all()) for c in connecteurs) / 100, 2),
    }


@never_cache
@login_required
@lecture
def plan_detail(request, pk):
    plan = get_object_or_404(_plans(request), pk=pk)
    ctx = _contexte_detail(plan)
    ctx.update({"peut_modifier": _peut_modifier(request.user), "peut_supprimer": peut_supprimer(request.user)})
    return render(request, "plan_cablage/plan_detail.html", ctx)


@login_required
@lecture
def plan_pdf(request, pk):
    from weasyprint import HTML
    plan = get_object_or_404(_plans(request), pk=pk)
    ctx = _contexte_detail(plan)
    ctx["societe"] = request.user.societe
    html = render_to_string("plan_cablage/plan_pdf.html", ctx, request=request)
    pdf = HTML(string=html, base_url=request.build_absolute_uri("/")).write_pdf()
    nom = slugify(f"cablage-{plan.voiture_exemplaire.immatriculation or ''}-{plan.nom_boitier}") or "cablage"
    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = f'inline; filename="{nom}.pdf"'
    return response


@login_required
def plan_supprimer(request, pk):
    if not peut_supprimer(request.user):
        return refuser_suppression(request)
    plan = get_object_or_404(_plans(request), pk=pk)
    if request.method == "POST":
        exemplaire_id = plan.voiture_exemplaire_id
        libelle = str(plan)
        plan.delete()
        _log(request.user, gettext_noop("Suppression du plan de câblage"), libelle)
        messages.success(request, _("Plan de câblage supprimé."))
        return redirect("plan_cablage:plan_liste", exemplaire_id=exemplaire_id)
    return render(request, "plan_cablage/supprimer.html", {"objet": plan, "plan": plan, "exemplaire": plan.voiture_exemplaire})


# ------------------------------------------------------------------ connecteur + fils
def _connecteur_form(request, plan, connecteur=None):
    instance = connecteur or ConnecteurCablage(plan=plan, ordre=plan.connecteurs.count() + 1)
    form = ConnecteurCablageForm(request.POST or None, instance=instance)
    fils = FilFormSet(request.POST or None, instance=instance, prefix="fil")
    if request.method == "POST":
        if form.is_valid() and fils.is_valid():
            with transaction.atomic():
                obj = form.save(commit=False)
                obj.plan = plan
                obj.save()
                fils.instance = obj
                for i, f in enumerate(fils.save(commit=False), start=1):
                    if not f.ordre:
                        f.ordre = i
                    f.save()
                for f in fils.deleted_objects:
                    f.delete()
            messages.success(request, _("Connecteur « %(c)s » enregistré.") % {"c": obj})
            if request.POST.get("suivant"):
                return redirect("plan_cablage:connecteur_ajouter", plan_pk=plan.pk)
            return redirect(f"{plan_url(plan)}#connecteur-{obj.pk}")
        messages.error(request, _("Le formulaire contient des erreurs."))
    return render(request, "plan_cablage/connecteur_form.html", {
        "form": form, "fils": fils, "plan": plan, "exemplaire": plan.voiture_exemplaire,
        "connecteur": connecteur, "couleurs_hex": COULEURS_HEX, "couleurs": CouleurFil.choices,
    })


def plan_url(plan):
    from django.urls import reverse
    return reverse("plan_cablage:plan_detail", kwargs={"pk": plan.pk})


@never_cache
@login_required
@atelier
def connecteur_ajouter(request, plan_pk):
    plan = get_object_or_404(_plans(request), pk=plan_pk)
    return _connecteur_form(request, plan)


@never_cache
@login_required
@atelier
def connecteur_modifier(request, pk):
    connecteur = get_object_or_404(ConnecteurCablage.objects.filter(plan__in=_plans(request)), pk=pk)
    return _connecteur_form(request, connecteur.plan, connecteur)


@login_required
@atelier
def connecteur_supprimer(request, pk):
    connecteur = get_object_or_404(ConnecteurCablage.objects.filter(plan__in=_plans(request)), pk=pk)
    plan = connecteur.plan
    if request.method == "POST":
        nom = str(connecteur)
        connecteur.delete()
        messages.success(request, _("Connecteur « %(c)s » supprimé.") % {"c": nom})
        return redirect("plan_cablage:plan_detail", pk=plan.pk)
    return render(request, "plan_cablage/supprimer.html", {"objet": connecteur, "plan": plan, "exemplaire": plan.voiture_exemplaire})
