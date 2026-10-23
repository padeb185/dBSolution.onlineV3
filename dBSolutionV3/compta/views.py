import calendar
import csv
from datetime import date
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.translation import gettext as _
from django.views.decorators.cache import never_cache

from .forms import CompteTresorerieForm, MouvementTresorerieForm, VirementInterneForm
from .models import (COMPTE_VIREMENTS_INTERNES, COMPTES_CONTREPARTIE, INTITULES_CONTREPARTIE,
                     CompteTresorerie, MouvementTresorerie)

ROLES_COMPTA = {"direction", "comptable"}
ZERO = Decimal("0.00")
MOIS_NOMS = ["", "Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août",
             "Septembre", "Octobre", "Novembre", "Décembre"]


def _autorise(user):
    return bool(getattr(user, "is_superuser", False) or getattr(user, "role", None) in ROLES_COMPTA)


def _refus(request):
    messages.error(request, _("Accès refusé"))
    return redirect("utilisateurs:dashboard")


def _log(request, action):
    try:
        from utilisateurs.models import UserLog
        UserLog.objects.create(utilisateur=request.user, action=action)
    except Exception:
        pass


def _comptes(request):
    return CompteTresorerie.objects.filter(societe=request.user.societe)


def _contexte_commun():
    return {"comptes_pcmn": COMPTES_CONTREPARTIE}


# ==================================================================
# TABLEAU DE BORD
# ==================================================================
@never_cache
@login_required
def compta_tableau_de_bord(request):
    if not _autorise(request.user):
        return _refus(request)

    aujourdhui = timezone.localdate()
    comptes = list(_comptes(request))
    for c in comptes:
        c.solde_actuel = c.solde(au=aujourdhui)

    actifs = [c for c in comptes if c.actif]
    return render(request, "compta/tableau_de_bord.html", {
        "comptes": comptes,
        "total_caisse": sum((c.solde_actuel for c in actifs if c.type == c.Type.CAISSE), ZERO),
        "total_banque": sum((c.solde_actuel for c in actifs if c.type == c.Type.BANQUE), ZERO),
        "total_tresorerie": sum((c.solde_actuel for c in actifs), ZERO),
        "derniers": MouvementTresorerie.objects.filter(compte__societe=request.user.societe)
                    .select_related("compte").order_by("-date", "-created_at")[:10],
        "aujourdhui": aujourdhui,
    })


# ==================================================================
# COMPTES : ouverture / modification / suppression
# ==================================================================
@never_cache
@login_required
def compte_ouvrir(request):
    if not _autorise(request.user):
        return _refus(request)

    type_ = request.GET.get("type")
    initial = {"type": type_} if type_ in CompteTresorerie.Type.values else {}
    if not _comptes(request).filter(type=initial.get("type", CompteTresorerie.Type.BANQUE), par_defaut=True).exists():
        initial["par_defaut"] = True

    form = CompteTresorerieForm(request.POST or None, initial=initial)
    if request.method == "POST" and form.is_valid():
        compte = form.save(commit=False)
        compte.societe = request.user.societe
        compte.save()
        _log(request, f"Ouverture du compte de trésorerie {compte}")
        messages.success(request, _("Le compte « %(nom)s » est ouvert avec un solde de %(solde)s €.")
                         % {"nom": compte.nom, "solde": f"{compte.solde_ouverture:.2f}"})
        return redirect("compta:compte_journal", pk=compte.pk)

    return render(request, "compta/compte_form.html", {"form": form, "compte": None, **_contexte_commun()})


@never_cache
@login_required
def compte_modifier(request, pk):
    if not _autorise(request.user):
        return _refus(request)
    compte = get_object_or_404(_comptes(request), pk=pk)
    form = CompteTresorerieForm(request.POST or None, instance=compte)
    if request.method == "POST" and form.is_valid():
        form.save()
        _log(request, f"Modification du compte de trésorerie {compte}")
        messages.success(request, _("Le compte a été mis à jour."))
        return redirect("compta:compte_journal", pk=compte.pk)
    return render(request, "compta/compte_form.html", {"form": form, "compte": compte, **_contexte_commun()})


@never_cache
@login_required
def compte_supprimer(request, pk):
    if not _autorise(request.user):
        return _refus(request)
    compte = get_object_or_404(_comptes(request), pk=pk)
    nb_mouvements = compte.mouvements.count()

    if request.method == "POST":
        if nb_mouvements:
            messages.error(request, _("Ce compte contient des mouvements : désactivez-le plutôt que de le supprimer."))
            return redirect("compta:compte_journal", pk=compte.pk)
        nom = str(compte)
        compte.delete()
        _log(request, f"Suppression du compte de trésorerie {nom}")
        messages.success(request, _("Le compte a été supprimé."))
        return redirect("compta:tableau_de_bord")

    return render(request, "compta/compte_supprimer.html", {"compte": compte, "nb_mouvements": nb_mouvements})


# ==================================================================
# JOURNAL D'UN COMPTE
# ==================================================================
def _periode(request):
    aujourdhui = timezone.localdate()
    try:
        annee = int(request.GET.get("annee") or aujourdhui.year)
    except ValueError:
        annee = aujourdhui.year
    try:
        mois = int(request.GET.get("mois") or 0)
    except ValueError:
        mois = 0
    if 1 <= mois <= 12:
        return annee, mois, date(annee, mois, 1), date(annee, mois, calendar.monthrange(annee, mois)[1])
    return annee, 0, date(annee, 1, 1), date(annee, 12, 31)


def _journal(compte, debut, fin):
    report = compte.solde(au=debut.fromordinal(debut.toordinal() - 1)) if debut > compte.date_ouverture else ZERO
    solde = report
    lignes = compte.lignes(debut=debut, fin=fin)
    for l in lignes:
        solde += l["entree"] - l["sortie"]
        l["solde"] = solde
        l["intitule_contrepartie"] = INTITULES_CONTREPARTIE.get(l["contrepartie"], "")
    return report, lignes, solde


@never_cache
@login_required
def compte_journal(request, pk):
    if not _autorise(request.user):
        return _refus(request)
    compte = get_object_or_404(_comptes(request), pk=pk)
    annee, mois, debut, fin = _periode(request)
    report, lignes, solde_fin = _journal(compte, debut, fin)

    if request.GET.get("export") == "csv":
        return _export_csv(compte, lignes, annee, mois)

    aujourdhui = timezone.localdate()
    return render(request, "compta/compte_journal.html", {
        "compte": compte,
        "annee": annee, "mois": mois,
        "annees": range(min(compte.date_ouverture.year, aujourdhui.year), aujourdhui.year + 2),
        "mois_choix": [(i, _(MOIS_NOMS[i])) for i in range(1, 13)],
        "report": report,
        "lignes": lignes,
        "total_entrees": sum((l["entree"] for l in lignes), ZERO),
        "total_sorties": sum((l["sortie"] for l in lignes), ZERO),
        "solde_fin": solde_fin,
        "solde_actuel": compte.solde(au=aujourdhui),
    })


def _export_csv(compte, lignes, annee, mois):
    """Export PCMN : chaque ligne du journal = 2 écritures (compte de trésorerie / contrepartie)."""
    nom = f"journal_{compte.journal_code}_{compte.compte_pcmn}_{annee}{'-%02d' % mois if mois else ''}.csv"
    response = HttpResponse(content_type="text/csv; charset=utf-8")
    response["Content-Disposition"] = f'attachment; filename="{nom}"'
    response.write("﻿")
    w = csv.writer(response, delimiter=";")
    w.writerow([_("Date"), _("Journal"), _("Pièce"), _("Compte"), _("Intitulé du compte"),
                _("Libellé"), _("Débit"), _("Crédit")])
    fmt = lambda x: f"{x:.2f}".replace(".", ",") if x else ""
    for l in lignes:
        jour = l["date"].strftime("%d/%m/%Y")
        journal = "OUV" if l["source"] == "ouverture" else compte.journal_code
        libelle = str(l["libelle"])
        # Ligne trésorerie : entrée = débit, sortie = crédit
        w.writerow([jour, journal, l["piece"], compte.compte_pcmn, compte.nom, libelle,
                    fmt(l["entree"]), fmt(l["sortie"])])
        # Contrepartie
        w.writerow([jour, journal, l["piece"], l["contrepartie"], l["intitule_contrepartie"], libelle,
                    fmt(l["sortie"]), fmt(l["entree"])])
    return response


# ==================================================================
# MOUVEMENTS
# ==================================================================
@never_cache
@login_required
def mouvement_ajouter(request, pk):
    if not _autorise(request.user):
        return _refus(request)
    compte = get_object_or_404(_comptes(request), pk=pk)
    sens = request.GET.get("sens")
    initial = {"date": timezone.localdate()}
    if sens in MouvementTresorerie.Sens.values:
        initial["sens"] = sens
        initial["compte_contrepartie"] = "700000" if sens == "ENTREE" else "610000"

    form = MouvementTresorerieForm(request.POST or None, compte=compte, initial=initial)
    if request.method == "POST" and form.is_valid():
        m = form.save(commit=False)
        m.compte = compte
        m.cree_par = request.user
        m.save()
        _log(request, f"Mouvement {m.get_sens_display()} {m.montant} € – {compte}")
        messages.success(request, _("Mouvement enregistré."))
        if "ajouter_autre" in request.POST:
            return redirect(f"{request.path}?sens={m.sens}")
        return redirect("compta:compte_journal", pk=compte.pk)

    return render(request, "compta/mouvement_form.html", {
        "form": form, "compte": compte, "mouvement": None, **_contexte_commun(),
    })


@never_cache
@login_required
def mouvement_modifier(request, pk):
    if not _autorise(request.user):
        return _refus(request)
    m = get_object_or_404(MouvementTresorerie.objects.filter(compte__societe=request.user.societe), pk=pk)
    if m.virement_lie_id:
        messages.error(request, _("Un virement interne ne se modifie pas : supprimez-le puis recréez-le."))
        return redirect("compta:compte_journal", pk=m.compte_id)

    form = MouvementTresorerieForm(request.POST or None, instance=m, compte=m.compte)
    if request.method == "POST" and form.is_valid():
        form.save()
        _log(request, f"Modification mouvement {m.montant} € – {m.compte}")
        messages.success(request, _("Mouvement mis à jour."))
        return redirect("compta:compte_journal", pk=m.compte_id)
    return render(request, "compta/mouvement_form.html", {
        "form": form, "compte": m.compte, "mouvement": m, **_contexte_commun(),
    })


@never_cache
@login_required
def mouvement_supprimer(request, pk):
    if not _autorise(request.user):
        return _refus(request)
    m = get_object_or_404(MouvementTresorerie.objects.filter(compte__societe=request.user.societe), pk=pk)
    compte_id = m.compte_id
    if request.method == "POST":
        with transaction.atomic():
            jumeau = MouvementTresorerie.objects.filter(virement_lie=m).first() or m.virement_lie
            if jumeau:
                MouvementTresorerie.objects.filter(pk__in=[m.pk, jumeau.pk]).update(virement_lie=None)
                jumeau.delete()
            m.delete()
        _log(request, f"Suppression mouvement {m.montant} € – {m.compte}")
        messages.success(request, _("Mouvement supprimé."))
        return redirect("compta:compte_journal", pk=compte_id)
    return render(request, "compta/mouvement_supprimer.html", {"mouvement": m})


# ==================================================================
# VIREMENT INTERNE (caisse ↔ banque, banque ↔ banque)
# ==================================================================
@never_cache
@login_required
def virement_interne(request):
    if not _autorise(request.user):
        return _refus(request)
    initial = {"date": timezone.localdate()}
    if request.GET.get("source"):
        initial["compte_source"] = request.GET["source"]
    form = VirementInterneForm(request.POST or None, societe=request.user.societe, initial=initial)

    if request.method == "POST" and form.is_valid():
        d = form.cleaned_data
        src, dst = d["compte_source"], d["compte_destination"]
        libelle = d["libelle"] or _("Virement interne %(src)s → %(dst)s") % {"src": src.nom, "dst": dst.nom}
        with transaction.atomic():
            sortie = MouvementTresorerie.objects.create(
                compte=src, date=d["date"], sens=MouvementTresorerie.Sens.SORTIE, montant=d["montant"],
                libelle=libelle, compte_contrepartie=COMPTE_VIREMENTS_INTERNES, piece="VIR", cree_par=request.user,
            )
            entree = MouvementTresorerie.objects.create(
                compte=dst, date=d["date"], sens=MouvementTresorerie.Sens.ENTREE, montant=d["montant"],
                libelle=libelle, compte_contrepartie=COMPTE_VIREMENTS_INTERNES, piece="VIR", cree_par=request.user,
                virement_lie=sortie,
            )
            sortie.virement_lie = entree
            sortie.save(update_fields=["virement_lie"])
        _log(request, f"Virement interne {d['montant']} € {src} → {dst}")
        messages.success(request, _("Virement interne de %(montant)s € enregistré.") % {"montant": f"{d['montant']:.2f}"})
        return redirect("compta:tableau_de_bord")

    return render(request, "compta/virement_form.html", {"form": form})
