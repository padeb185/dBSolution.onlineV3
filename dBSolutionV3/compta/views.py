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

from .forms import CompteTresorerieForm, MouvementTresorerieForm, VirementInterneForm, gobd
from .models import (COMPTE_VIREMENTS_INTERNES, COMPTES_CONTREPARTIE, INTITULES_CONTREPARTIE,
                     CompteTresorerie, MouvementTresorerie)
from .plans_comptables import code_plan, compte_national, comptes_proposes, plan_du_pays

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


def _pays(request):
    from core.pays import pays_societe
    return pays_societe(request.user.societe)


def _contexte_commun(pays):
    """Comptes proposés et règles du pays de la société (DE : SKR03 + GoBD)."""
    return {
        "comptes_pcmn": comptes_proposes(COMPTES_CONTREPARTIE, pays),
        "plan_code": code_plan(pays),
        "plan_national": bool(plan_du_pays(pays)),
        "gobd": gobd(pays),
        "compte_caisse_defaut": compte_national("570000", pays)[0],
        "compte_banque_defaut": compte_national("550000", pays)[0],
    }


def _affichage_compte(compte, pays):
    """Numéro du compte de trésorerie dans le plan du pays (DE : 1000 / 1200…)."""
    compte.compte_affiche = compte_national(compte.compte_pcmn, pays)[0]
    return compte


# ==================================================================
# TABLEAU DE BORD
# ==================================================================
@never_cache
@login_required
def compta_tableau_de_bord(request):
    if not _autorise(request.user):
        return _refus(request)

    aujourdhui = timezone.localdate()
    pays = _pays(request)
    comptes = list(_comptes(request))
    for c in comptes:
        c.solde_actuel = c.solde(au=aujourdhui)
        _affichage_compte(c, pays)

    actifs = [c for c in comptes if c.actif]
    return render(request, "compta/tableau_de_bord.html", {
        "comptes": comptes,
        "total_caisse": sum((c.solde_actuel for c in actifs if c.type == c.Type.CAISSE), ZERO),
        "total_banque": sum((c.solde_actuel for c in actifs if c.type == c.Type.BANQUE), ZERO),
        "total_tresorerie": sum((c.solde_actuel for c in actifs), ZERO),
        "derniers": MouvementTresorerie.objects.filter(compte__societe=request.user.societe)
                    .select_related("compte").order_by("-date", "-created_at")[:10],
        "aujourdhui": aujourdhui,
        **_contexte_commun(pays),
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

    pays = _pays(request)
    form = CompteTresorerieForm(request.POST or None, initial=initial, pays=pays)
    if request.method == "POST" and form.is_valid():
        compte = form.save(commit=False)
        compte.societe = request.user.societe
        compte.save()
        _log(request, f"Ouverture du compte de trésorerie {compte}")
        messages.success(request, _("Le compte « %(nom)s » est ouvert avec un solde de %(solde)s €.")
                         % {"nom": compte.nom, "solde": f"{compte.solde_ouverture:.2f}"})
        return redirect("compta:compte_journal", pk=compte.pk)

    return render(request, "compta/compte_form.html", {"form": form, "compte": None, **_contexte_commun(pays)})


@never_cache
@login_required
def compte_modifier(request, pk):
    if not _autorise(request.user):
        return _refus(request)
    compte = get_object_or_404(_comptes(request), pk=pk)
    pays = _pays(request)
    form = CompteTresorerieForm(request.POST or None, instance=compte, pays=pays)
    if request.method == "POST" and form.is_valid():
        form.save()
        _log(request, f"Modification du compte de trésorerie {compte}")
        messages.success(request, _("Le compte a été mis à jour."))
        return redirect("compta:compte_journal", pk=compte.pk)
    return render(request, "compta/compte_form.html", {"form": form, "compte": compte, **_contexte_commun(pays)})


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


def _journal(compte, debut, fin, pays=None):
    """Lignes du journal avec solde progressif ; contreparties dans le plan du pays (DE → SKR03)."""
    report = compte.solde(au=debut.fromordinal(debut.toordinal() - 1)) if debut > compte.date_ouverture else ZERO
    solde = report
    lignes = compte.lignes(debut=debut, fin=fin)
    national = bool(plan_du_pays(pays))
    for l in lignes:
        solde += l["entree"] - l["sortie"]
        l["solde"] = solde
        l["contrepartie_pcmn"] = l["contrepartie"]
        if national:
            l["contrepartie"], l["intitule_contrepartie"] = compte_national(l["contrepartie"], pays)
        else:
            l["intitule_contrepartie"] = INTITULES_CONTREPARTIE.get(l["contrepartie"], "")
        objet = l.get("objet")
        l["numero"] = getattr(objet, "numero", None) if l["source"] in ("manuel", "virement") else None
        l["extourne"] = bool(l["source"] in ("manuel", "virement") and objet is not None
                             and (objet.extourne_de_id or objet.est_extourne))
    return report, lignes, solde


@never_cache
@login_required
def compte_journal(request, pk):
    if not _autorise(request.user):
        return _refus(request)
    compte = get_object_or_404(_comptes(request), pk=pk)
    pays = _pays(request)
    _affichage_compte(compte, pays)
    annee, mois, debut, fin = _periode(request)
    report, lignes, solde_fin = _journal(compte, debut, fin, pays)

    if request.GET.get("export") == "csv":
        return _export_csv(compte, lignes, annee, mois, pays)
    if request.GET.get("export") == "datev" and plan_du_pays(pays):
        return _export_datev(compte, lignes, annee, mois)

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
        **_contexte_commun(pays),
    })


def _export_csv(compte, lignes, annee, mois, pays=None):
    """
    Export débit / crédit : chaque ligne du journal = 2 écritures (compte de trésorerie / contrepartie).
    Comptes dans le plan du pays (DE → SKR03), avec le compte interne PCMN en dernière colonne.
    """
    plan = plan_du_pays(pays)
    compte_tresorerie = compte_national(compte.compte_pcmn, pays)[0]
    nom = f"journal_{compte.journal_code}_{compte_tresorerie}_{annee}{'-%02d' % mois if mois else ''}.csv"
    response = HttpResponse(content_type="text/csv; charset=utf-8")
    response["Content-Disposition"] = f'attachment; filename="{nom}"'
    response.write("\ufeff")
    w = csv.writer(response, delimiter=";")
    entete = [_("Date"), _("Journal"), _("N°"), _("Pièce"), plan["code"] if plan else _("Compte"),
              _("Intitulé du compte"), _("Libellé"), _("Débit"), _("Crédit")]
    if plan:
        entete.append(_("Compte interne (PCMN)"))
    w.writerow(entete)
    fmt = lambda x: f"{x:.2f}".replace(".", ",") if x else ""
    for l in lignes:
        jour = l["date"].strftime("%d/%m/%Y")
        journal = "OUV" if l["source"] == "ouverture" else compte.journal_code
        libelle = str(l["libelle"])
        numero = l.get("numero") or ""
        # Ligne trésorerie : entrée = débit, sortie = crédit
        ligne = [jour, journal, numero, l["piece"], compte_tresorerie, compte.nom, libelle,
                 fmt(l["entree"]), fmt(l["sortie"])]
        w.writerow(ligne + ([compte.compte_pcmn] if plan else []))
        # Contrepartie
        ligne = [jour, journal, numero, l["piece"], l["contrepartie"], l["intitule_contrepartie"], libelle,
                 fmt(l["sortie"]), fmt(l["entree"])]
        w.writerow(ligne + ([l.get("contrepartie_pcmn", "")] if plan else []))
    return response


def _export_datev(compte, lignes, annee, mois):
    """
    Export au format des colonnes du « Buchungsstapel » DATEV (import ASCII chez le Steuerberater) :
    Umsatz, Soll/Haben-Kennzeichen, WKZ, Konto, Gegenkonto, BU-Schlüssel, Belegdatum (TTMM),
    Belegfeld 1, Buchungstext. Konto = Kasse / Bank (S = entrée, H = sortie), Gegenkonto en SKR03.
    Encodage Windows-1252, séparateur « ; », virgule décimale. L'en-tête EXTF (n° de conseiller,
    de client, exercice) est ajouté par le Steuerberater ou par DATEV Unternehmen online.
    """
    from .plans_comptables import compte_national as cn
    konto = cn(compte.compte_pcmn, "DE")[0]
    nom = f"DATEV_{'Kassenbuch' if compte.type == compte.Type.CAISSE else 'Bankbuch'}_{konto}_{annee}" \
          f"{'-%02d' % mois if mois else ''}.csv"
    response = HttpResponse(content_type="text/csv; charset=windows-1252")
    response["Content-Disposition"] = f'attachment; filename="{nom}"'
    lignes_csv = []
    sortie = csv.writer(_Tampon(lignes_csv), delimiter=";", quoting=csv.QUOTE_MINIMAL)
    sortie.writerow(["Umsatz (ohne Soll/Haben-Kz)", "Soll/Haben-Kennzeichen", "WKZ Umsatz", "Konto",
                     "Gegenkonto (ohne BU-Schlüssel)", "BU-Schlüssel", "Belegdatum", "Belegfeld 1", "Buchungstext"])
    for l in lignes:
        montant = l["entree"] or l["sortie"]
        if not montant:
            continue
        sortie.writerow([
            f"{montant:.2f}".replace(".", ","), "S" if l["entree"] else "H", "EUR", konto, l["contrepartie"], "",
            l["date"].strftime("%d%m"), (str(l["piece"] or l.get("numero") or ""))[:36], str(l["libelle"])[:60],
        ])
    response.write("".join(lignes_csv).encode("cp1252", errors="replace"))
    return response


class _Tampon:
    def __init__(self, lignes):
        self.lignes = lignes

    def write(self, texte):
        self.lignes.append(texte)


# ==================================================================
# MOUVEMENTS
# ==================================================================
@never_cache
@login_required
def mouvement_ajouter(request, pk):
    if not _autorise(request.user):
        return _refus(request)
    compte = get_object_or_404(_comptes(request), pk=pk)
    pays = _pays(request)
    _affichage_compte(compte, pays)
    sens = request.GET.get("sens")
    initial = {"date": timezone.localdate()}
    if sens in MouvementTresorerie.Sens.values:
        initial["sens"] = sens
        initial["compte_contrepartie"] = "700000" if sens == "ENTREE" else "610000"

    form = MouvementTresorerieForm(request.POST or None, compte=compte, initial=initial, pays=pays)
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
        "form": form, "compte": compte, "mouvement": None, **_contexte_commun(pays),
    })


@never_cache
@login_required
def mouvement_modifier(request, pk):
    if not _autorise(request.user):
        return _refus(request)
    m = get_object_or_404(MouvementTresorerie.objects.filter(compte__societe=request.user.societe), pk=pk)
    pays = _pays(request)
    if gobd(pays):
        messages.error(request, _("GoBD : une écriture de caisse ou de banque ne se modifie pas. "
                                  "Extournez-la (Storno) puis encodez l'écriture correcte."))
        return redirect("compta:compte_journal", pk=m.compte_id)
    if m.virement_lie_id:
        messages.error(request, _("Un virement interne ne se modifie pas : supprimez-le puis recréez-le."))
        return redirect("compta:compte_journal", pk=m.compte_id)
    if m.extourne_de_id or m.est_extourne:
        messages.error(request, _("Un mouvement extourné ou une extourne ne se modifie pas."))
        return redirect("compta:compte_journal", pk=m.compte_id)
    _affichage_compte(m.compte, pays)

    form = MouvementTresorerieForm(request.POST or None, instance=m, compte=m.compte, pays=pays)
    if request.method == "POST" and form.is_valid():
        form.save()
        _log(request, f"Modification mouvement {m.montant} € – {m.compte}")
        messages.success(request, _("Mouvement mis à jour."))
        return redirect("compta:compte_journal", pk=m.compte_id)
    return render(request, "compta/mouvement_form.html", {
        "form": form, "compte": m.compte, "mouvement": m, **_contexte_commun(pays),
    })


@never_cache
@login_required
def mouvement_supprimer(request, pk):
    if not _autorise(request.user):
        return _refus(request)
    m = get_object_or_404(MouvementTresorerie.objects.filter(compte__societe=request.user.societe), pk=pk)
    compte_id = m.compte_id
    if gobd(_pays(request)):
        messages.error(request, _("GoBD : une écriture de caisse ou de banque ne se supprime pas. "
                                  "Extournez-la (Storno)."))
        return redirect("compta:compte_journal", pk=compte_id)
    if request.method == "POST":
        with transaction.atomic():
            jumeau = MouvementTresorerie.objects.filter(virement_lie=m).first() or m.virement_lie
            a_supprimer = [m] + ([jumeau] if jumeau else [])
            # Les extournes éventuelles disparaissent avec le mouvement qu'elles annulent
            extournes = list(MouvementTresorerie.objects.filter(extourne_de__in=a_supprimer))
            ids = [x.pk for x in a_supprimer + extournes]
            MouvementTresorerie.objects.filter(pk__in=ids).update(virement_lie=None)
            for x in extournes:
                x.delete()
            if jumeau:
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
    form = VirementInterneForm(request.POST or None, societe=request.user.societe, initial=initial,
                               pays=_pays(request))

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


# ==================================================================
# EXTOURNE (Storno) – correction sans modification ni suppression (GoBD)
# ==================================================================
@never_cache
@login_required
def mouvement_extourner(request, pk):
    """
    Annule un mouvement par une écriture inverse datée du jour (Storno). Le mouvement d'origine reste
    dans le journal, barré, avec son numéro : obligatoire en Allemagne (GoBD, § 146 al. 4 AO),
    disponible aussi ailleurs. Un virement interne est extourné sur ses deux comptes.
    """
    if not _autorise(request.user):
        return _refus(request)
    m = get_object_or_404(MouvementTresorerie.objects.filter(compte__societe=request.user.societe)
                          .select_related("compte"), pk=pk)
    retour = redirect("compta:compte_journal", pk=m.compte_id)
    if m.extourne_de_id:
        messages.error(request, _("Une extourne ne s'extourne pas : encodez une nouvelle écriture."))
        return retour
    if m.est_extourne:
        messages.error(request, _("Ce mouvement est déjà extourné."))
        return retour

    jumeau = MouvementTresorerie.objects.filter(virement_lie=m).first() or m.virement_lie
    aujourdhui = timezone.localdate()
    date_extourne = max(aujourdhui, m.date)
    originaux = [m] + ([jumeau] if jumeau else [])

    # La caisse ne peut pas devenir négative à cause de l'extourne d'une entrée
    for o in originaux:
        if o.compte.type == o.compte.Type.CAISSE and o.sens == o.Sens.ENTREE and o.montant > o.compte.solde(au=date_extourne):
            messages.error(request, _("Solde de caisse insuffisant pour extourner cette entrée (%(solde)s € disponibles).")
                           % {"solde": f"{o.compte.solde(au=date_extourne):.2f}"})
            return retour

    if request.method == "POST":
        motif = (request.POST.get("motif") or "").strip()[:150]
        with transaction.atomic():
            crees = []
            for o in originaux:
                crees.append(MouvementTresorerie.objects.create(
                    compte=o.compte, date=date_extourne,
                    sens=o.Sens.SORTIE if o.sens == o.Sens.ENTREE else o.Sens.ENTREE,
                    montant=o.montant, compte_contrepartie=o.compte_contrepartie,
                    libelle=(f"Storno n° {o.numero} – {o.libelle}" + (f" ({motif})" if motif else ""))[:255],
                    piece=(f"ST-{o.piece}" if o.piece else f"ST-{o.numero}")[:50],
                    remarques=motif, extourne_de=o, cree_par=request.user,
                ))
            if len(crees) == 2:
                crees[0].virement_lie = crees[1]
                crees[1].virement_lie = crees[0]
                for c in crees:
                    c.save(update_fields=["virement_lie"])
        _log(request, f"Extourne (Storno) du mouvement n° {m.numero} {m.montant} € – {m.compte}")
        messages.success(request, _("Mouvement n° %(numero)s extourné.") % {"numero": m.numero})
        return retour

    return render(request, "compta/mouvement_extourner.html", {
        "mouvement": m, "jumeau": jumeau, "date_extourne": date_extourne,
    })
