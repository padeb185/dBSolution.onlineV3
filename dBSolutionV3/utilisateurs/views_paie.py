"""
Paies mensuelles : panneau de contrôle, listes, détail, création,
modification et suppression.
"""
from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext as _
from django.views.decorators.cache import never_cache

from utils.securite import peut_supprimer, refuser_suppression
from .forms import PaieUtilisateurForm
from .models import PaieUtilisateur, Utilisateur, UserLog

# Rôles autorisés à consulter / gérer les paies
ROLES_PAIE = {"direction", "comptable", "chef_mecanicien"}

MOIS_NOMS = [
    "", "Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
    "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre",
]

TOTAUX = {
    "nb": Count("id"),
    "brut": Sum("salaire_brut_mensuel"),
    "onss": Sum("montant_onss"),
    "precompte": Sum("montant_precompte"),
    "csss": Sum("csss"),
    "net": Sum("salaire_net_mois"),
    "cotisations": Sum("cotisations_patronales"),
    "cout": Sum("salaire_brut_mensuel_employeur"),
}


def _acces_paie(user):
    return bool(getattr(user, "is_superuser", False) or getattr(user, "role", None) in ROLES_PAIE)


def _refuser(request):
    messages.error(request, _("Accès refusé"))
    return redirect("utilisateurs:dashboard")


def _paies_societe(request):
    return (
        PaieUtilisateur.objects
        .filter(utilisateur__societe=request.user.societe)
        .select_related("utilisateur")
    )


def _get_paie(request, pk):
    return get_object_or_404(_paies_societe(request), pk=pk)


def _annee(request):
    try:
        return int(request.GET.get("annee") or timezone.now().year)
    except ValueError:
        return timezone.now().year


def _log(request, action):
    try:
        UserLog.objects.create(utilisateur=request.user, action=action)
    except Exception:
        pass


# ==================================================================
# PANNEAU DE CONTRÔLE
# ==================================================================
@never_cache
@login_required
def paie_panneau(request):
    if not _acces_paie(request.user):
        return _refuser(request)

    annee = _annee(request)
    paies = _paies_societe(request)
    paies_annee = paies.filter(annee=annee)

    totaux = paies_annee.aggregate(**TOTAUX)

    # Totaux par mois
    par_mois_qs = {
        row["mois"]: row
        for row in paies_annee.values("mois").annotate(**TOTAUX)
    }
    par_mois = []
    for m in range(1, 13):
        row = par_mois_qs.get(m, {})
        par_mois.append({
            "mois": m,
            "nom": _(MOIS_NOMS[m]),
            "nb": row.get("nb", 0),
            "brut": row.get("brut"),
            "net": row.get("net"),
            "precompte": row.get("precompte"),
            "onss": row.get("onss"),
            "cout": row.get("cout"),
        })

    # Totaux par travailleur
    par_travailleur = (
        paies_annee
        .values("utilisateur", "utilisateur__prenom", "utilisateur__nom", "utilisateur__role")
        .annotate(**TOTAUX)
        .order_by("utilisateur__nom", "utilisateur__prenom")
    )

    # Travailleurs actifs sans paie ce mois-ci
    maintenant = timezone.now()
    avec_paie_ce_mois = paies.filter(
        annee=maintenant.year, mois=maintenant.month
    ).values_list("utilisateur_id", flat=True)
    sans_paie = (
        Utilisateur.objects
        .filter(societe=request.user.societe, is_active=True)
        .exclude(id__in=avec_paie_ce_mois)
        .order_by("nom", "prenom")
    )

    annees = sorted(set(paies.values_list("annee", flat=True)) | {annee, maintenant.year}, reverse=True)

    return render(request, "utilisateurs/paie/paie_panneau.html", {
        "annee": annee,
        "annees": annees,
        "totaux": totaux,
        "par_mois": par_mois,
        "par_travailleur": par_travailleur,
        "dernieres": paies.order_by("-annee", "-mois", "utilisateur__nom")[:10],
        "sans_paie": sans_paie,
        "mois_courant": _(MOIS_NOMS[maintenant.month]),
    })


# ==================================================================
# LISTES
# ==================================================================
@never_cache
@login_required
def paie_list(request):
    if not _acces_paie(request.user):
        return _refuser(request)

    paies = _paies_societe(request).order_by("-annee", "-mois", "utilisateur__nom")
    annee = request.GET.get("annee")
    if annee:
        paies = paies.filter(annee=annee)

    return render(request, "utilisateurs/paie/paie_list.html", {
        "paies": paies,
        "totaux": paies.aggregate(**TOTAUX),
        "annee": annee,
        "travailleur": None,
    })


@never_cache
@login_required
def paie_list_travailleur(request, utilisateur_id):
    if not _acces_paie(request.user):
        return _refuser(request)

    travailleur = get_object_or_404(
        Utilisateur, pk=utilisateur_id, societe=request.user.societe
    )
    paies = _paies_societe(request).filter(utilisateur=travailleur).order_by("-annee", "-mois")
    annee = request.GET.get("annee")
    if annee:
        paies = paies.filter(annee=annee)

    return render(request, "utilisateurs/paie/paie_list.html", {
        "paies": paies,
        "totaux": paies.aggregate(**TOTAUX),
        "annee": annee,
        "travailleur": travailleur,
    })


# ==================================================================
# DÉTAIL
# ==================================================================
@never_cache
@login_required
def paie_detail(request, pk):
    if not _acces_paie(request.user):
        return _refuser(request)

    paie = _get_paie(request, pk)
    form = PaieUtilisateurForm(instance=paie, societe=request.user.societe)
    for champ in form.fields.values():   # fiche en lecture seule
        champ.disabled = True

    return render(request, "utilisateurs/paie/paie_detail.html", {
        "paie": paie,
        "form": form,
        "mois_nom": _(MOIS_NOMS[paie.mois]) if 1 <= paie.mois <= 12 else paie.mois,
    })


# ==================================================================
# CRÉATION
# ==================================================================
@login_required
def creer_paie_utilisateur(request):
    if not _acces_paie(request.user):
        return _refuser(request)

    if request.method == "POST":
        form = PaieUtilisateurForm(request.POST, societe=request.user.societe)

        if form.is_valid():
            if "calculer" in request.POST:
                paie = form.save(commit=False)
                paie.calculer()
                form = PaieUtilisateurForm(instance=paie, societe=request.user.societe)
                messages.info(request, _("Calcul effectué – vérifiez puis enregistrez."))
            else:
                paie = form.save()
                _log(request, f"Création paie {paie.mois}/{paie.annee} – {paie.utilisateur}")
                messages.success(request, _("La paie mensuelle a été enregistrée avec succès."))
                return redirect("utilisateurs:paie_detail", pk=paie.pk)
        else:
            messages.error(request, _("Le formulaire contient des erreurs."))
    else:
        maintenant = timezone.now()
        initial = {"mois": maintenant.month, "annee": maintenant.year}

        # Pré-remplissage depuis la dernière paie du travailleur
        utilisateur_id = request.GET.get("utilisateur")
        if utilisateur_id:
            initial["utilisateur"] = utilisateur_id
            derniere = (
                _paies_societe(request)
                .filter(utilisateur_id=utilisateur_id)
                .order_by("-annee", "-mois")
                .first()
            )
            if derniere:
                for champ in PaieUtilisateurForm.CHAMPS_REPRIS:
                    initial[champ] = getattr(derniere, champ)

        form = PaieUtilisateurForm(societe=request.user.societe, initial=initial)

    return render(request, "utilisateurs/paie/paie_form.html", {
        "form": form,
        "now": timezone.now(),
    })


# ==================================================================
# MODIFICATION
# ==================================================================
@login_required
def modifier_paie(request, pk):
    if not _acces_paie(request.user):
        return _refuser(request)

    paie = _get_paie(request, pk)

    if request.method == "POST":
        form = PaieUtilisateurForm(request.POST, instance=paie, societe=request.user.societe)

        if form.is_valid():
            if "calculer" in request.POST:
                paie_calc = form.save(commit=False)
                paie_calc.calculer()
                form = PaieUtilisateurForm(instance=paie_calc, societe=request.user.societe)
                messages.info(request, _("Calcul effectué – vérifiez puis enregistrez."))
            else:
                paie = form.save()
                _log(request, f"Modification paie {paie.mois}/{paie.annee} – {paie.utilisateur}")
                messages.success(request, _("La paie mensuelle a été mise à jour."))
                return redirect("utilisateurs:paie_detail", pk=paie.pk)
        else:
            messages.error(request, _("Le formulaire contient des erreurs."))
    else:
        form = PaieUtilisateurForm(instance=paie, societe=request.user.societe)

    return render(request, "utilisateurs/paie/modifier_paie.html", {
        "form": form,
        "paie": paie,
        "now": timezone.now(),
    })


# ==================================================================
# SUPPRESSION
# ==================================================================
@login_required
def delete_paie(request, pk):
    if not _acces_paie(request.user) or not peut_supprimer(request.user):
        return refuser_suppression(request)

    paie = _get_paie(request, pk)

    if request.method == "POST":
        libelle = f"{paie.mois}/{paie.annee} – {paie.utilisateur}"
        utilisateur_id = paie.utilisateur_id
        paie.delete()
        _log(request, f"Suppression paie {libelle}")
        messages.success(request, _("La paie %(libelle)s a été supprimée.") % {"libelle": libelle})
        return redirect("utilisateurs:paie_list_travailleur", utilisateur_id=utilisateur_id)

    return render(request, "utilisateurs/paie/delete_paie.html", {
        "paie": paie,
        "mois_nom": _(MOIS_NOMS[paie.mois]) if 1 <= paie.mois <= 12 else paie.mois,
    })


# ==================================================================
# PAIEMENT DU NET
# ==================================================================
@login_required
def paie_payer(request, pk):
    if not _acces_paie(request.user):
        return _refuser(request)

    paie = _get_paie(request, pk)

    if request.method == "POST":
        if "annuler" in request.POST:
            PaieUtilisateur.objects.filter(pk=paie.pk).update(date_paiement=None)
            _log(request, f"Annulation paiement paie {paie.mois}/{paie.annee} – {paie.utilisateur}")
            messages.success(request, _("Le paiement a été annulé."))
        else:
            try:
                date_paiement = date.fromisoformat(request.POST.get("date_paiement") or "")
            except ValueError:
                date_paiement = timezone.now().date()
            PaieUtilisateur.objects.filter(pk=paie.pk).update(date_paiement=date_paiement)
            _log(request, f"Paiement paie {paie.mois}/{paie.annee} – {paie.utilisateur}")
            messages.success(request, _("Le salaire net est marqué comme payé."))

    return redirect(request.POST.get("next") or reverse("utilisateurs:paie_detail", args=[paie.pk]))


# ==================================================================
# COMPTABILITÉ
# ==================================================================
def _dernier_jour(annee, mois):
    import calendar
    return date(annee, mois, calendar.monthrange(annee, mois)[1])


def _periode(request):
    annee = _annee(request)
    try:
        mois = int(request.GET.get("mois") or 0)
    except ValueError:
        mois = 0
    return annee, mois if 1 <= mois <= 12 else 0


def _paies_periode(request):
    annee, mois = _periode(request)
    paies = _paies_societe(request).filter(annee=annee)
    if mois:
        paies = paies.filter(mois=mois)
    return annee, mois, paies.order_by("mois", "utilisateur__nom", "utilisateur__prenom")


@never_cache
@login_required
def paie_comptabilite(request):
    from decimal import Decimal
    from collections import OrderedDict
    from .paie_belgique import COMPTES

    if not _acces_paie(request.user):
        return _refuser(request)

    annee, mois, paies = _paies_periode(request)
    z = Decimal("0")

    # ---- Balance par compte
    balance = OrderedDict((c, {"compte": c, "intitule": i, "debit": z, "credit": z}) for c, i in COMPTES.items())
    journal = []
    for paie in paies:
        lignes = paie.ecritures_comptables()
        journal.append({"paie": paie, "lignes": lignes})
        for l in lignes:
            b = balance[l["compte"]]
            b["debit"] += l["debit"]
            b["credit"] += l["credit"]
    balance = [b for b in balance.values() if b["debit"] or b["credit"]]
    for b in balance:
        b["solde"] = b["debit"] - b["credit"]
    total_debit = sum((b["debit"] for b in balance), z)
    total_credit = sum((b["credit"] for b in balance), z)

    # ---- Précompte à verser au SPF Finances (mensuel, le 15 du mois suivant)
    precompte = OrderedDict()
    # ---- ONSS à verser (trimestriel, fin du mois qui suit le trimestre)
    onss = OrderedDict()
    for paie in paies:
        pp = (paie.montant_precompte or z) + (paie.double_pecule_precompte or z)
        cle = paie.mois
        if cle not in precompte:
            m_suiv, a_suiv = (1, paie.annee + 1) if paie.mois == 12 else (paie.mois + 1, paie.annee)
            precompte[cle] = {"periode": f"{paie.mois:02d}/{paie.annee}",
                              "echeance": date(a_suiv, m_suiv, 15), "montant": z}
        precompte[cle]["montant"] += pp

        montant_onss = (
            (paie.montant_onss or z) + (paie.csss or z) + (paie.cotisations_patronales or z)
            + (paie.cotisation_co2 or z) + (paie.double_pecule_onss or z)
            + ((paie.cotisations_vacances or z) if paie.statut_travailleur == "ouvrier" else z)
        )
        trimestre = (paie.mois - 1) // 3 + 1
        if trimestre not in onss:
            m_ech = trimestre * 3 + 1
            a_ech = paie.annee + 1 if m_ech > 12 else paie.annee
            m_ech = 1 if m_ech > 12 else m_ech
            onss[trimestre] = {"periode": f"T{trimestre} {paie.annee}",
                               "echeance": _dernier_jour(a_ech, m_ech), "montant": z}
        onss[trimestre]["montant"] += montant_onss

    # ---- Salaires nets à payer
    non_payees = [p for p in paies if not p.est_paye]
    payees = [p for p in paies if p.est_paye]

    return render(request, "utilisateurs/paie/paie_comptabilite.html", {
        "annee": annee,
        "mois": mois,
        "mois_choix": [(i, _(MOIS_NOMS[i])) for i in range(1, 13)],
        "annees": sorted(set(_paies_societe(request).values_list("annee", flat=True)) | {annee}, reverse=True),
        "balance": balance,
        "total_debit": total_debit,
        "total_credit": total_credit,
        "journal": journal,
        "precompte": list(precompte.values()),
        "total_precompte": sum((p["montant"] for p in precompte.values()), z),
        "onss": list(onss.values()),
        "total_onss": sum((o["montant"] for o in onss.values()), z),
        "non_payees": non_payees,
        "total_a_payer": sum((p.net_a_payer for p in non_payees), z),
        "total_paye": sum((p.net_a_payer for p in payees), z),
        "aujourdhui": timezone.now().date(),
    })


@login_required
def paie_comptabilite_csv(request):
    """Export du journal des salaires (CSV ; séparateur point-virgule, virgule décimale)."""
    import csv
    from django.http import HttpResponse

    if not _acces_paie(request.user):
        return _refuser(request)

    annee, mois, paies = _paies_periode(request)
    nom = f"journal_salaires_{annee}{'-%02d' % mois if mois else ''}.csv"

    response = HttpResponse(content_type="text/csv; charset=utf-8")
    response["Content-Disposition"] = f'attachment; filename="{nom}"'
    response.write("﻿")  # BOM pour Excel

    w = csv.writer(response, delimiter=";")
    w.writerow(["Date", "Journal", "Pièce", "Compte", "Intitulé du compte",
                "Libellé", "Travailleur", "Débit", "Crédit"])

    def fmt(x):
        return f"{x:.2f}".replace(".", ",") if x else ""

    for paie in paies:
        piece = f"PAIE-{paie.annee}{paie.mois:02d}-{paie.pk}"
        travailleur = f"{paie.utilisateur.prenom} {paie.utilisateur.nom}"
        for l in paie.ecritures_comptables():
            jour = paie.date_paiement if l["type"] == "paiement" else _dernier_jour(paie.annee, paie.mois)
            journal = "BQ" if l["type"] == "paiement" else "OD"
            w.writerow([jour.strftime("%d/%m/%Y"), journal, piece, l["compte"], l["intitule"],
                        l["libelle"], travailleur, fmt(l["debit"]), fmt(l["credit"])])

    return response
