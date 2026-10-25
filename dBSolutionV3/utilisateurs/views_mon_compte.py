"""
Dashboard utilisateur (« Mon compte ») : ouvert depuis la cartouche « Utilisateur » du tableau de bord.
Infos personnelles, adresse, sécurité (mot de passe, 2FA), maintenances (nombres et statistiques),
total des salaires nets et heures prestées.
"""
from collections import OrderedDict
from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q, Sum
from django.shortcuts import redirect, render
from django.utils import timezone
from django.utils.translation import gettext as _
from django.views.decorators.cache import never_cache
from django_tenants.utils import schema_context

ZERO = Decimal("0.00")


def _heures_minutes(minutes):
    minutes = int(minutes or 0)
    h, m = divmod(minutes, 60)
    return f"{h}h{m:02d}"


@never_cache
@login_required
def mon_compte_view(request):
    user = request.user
    if not getattr(user, "societe", None):
        return redirect("utilisateurs:dashboard")
    return render(request, "utilisateurs/mon_compte.html", contexte_compte(user))


def contexte_compte(user):
    """Infos, adresse, maintenances et paies d'un utilisateur (dashboard « Mon compte » / profil)."""
    societe = getattr(user, "societe", None)

    aujourdhui = timezone.localdate()
    annee = aujourdhui.year
    schema_name = getattr(societe, "schema_name", None)

    # ==================================================
    # MAINTENANCES
    # ==================================================
    maint = {
        "total": 0, "annee": 0, "mois": 0, "en_cours": 0,
        "par_type": [], "par_tag": {"VERT": 0, "JAUNE": 0, "ROUGE": 0},
        "par_mois": [], "max_mois": 0, "par_role": [], "dernieres": [],
        "mo_minutes_total": 0, "mo_minutes_annee": 0, "mo_cout_total": ZERO, "mo_nb": 0,
    }
    if schema_name:
        from maintenance.models import Maintenance
        from maindoeuvre.models import MainDoeuvre

        with schema_context(schema_name):
            qs = (
                Maintenance.objects.filter(societe=societe)
                .filter(Q(mecanicien_id=user.id) | Q(chef_mecanicien_id=user.id)
                        | Q(apprentis_id=user.id) | Q(tech_technicien_id=user.id))
                .distinct()
            )
            ids = list(qs.values_list("id", flat=True))
            base = Maintenance.objects.filter(id__in=ids)

            maint["total"] = len(ids)
            maint["annee"] = base.filter(date_intervention__year=annee).count()
            maint["mois"] = base.filter(date_intervention__year=annee, date_intervention__month=aujourdhui.month).count()

            # Par état (tag)
            for row in base.values("tag").annotate(n=Count("id")):
                if row["tag"] in maint["par_tag"]:
                    maint["par_tag"][row["tag"]] = row["n"]
            maint["en_cours"] = maint["par_tag"]["JAUNE"] + maint["par_tag"]["ROUGE"]

            # Par type (top 10)
            libelles = dict(Maintenance.TypeMaintenance.choices)
            par_type = base.values("type_maintenance").annotate(n=Count("id")).order_by("-n")
            maint["par_type"] = [
                {"label": libelles.get(r["type_maintenance"], r["type_maintenance"] or _("Non précisé")), "n": r["n"],
                 "pct": round(r["n"] * 100 / maint["total"]) if maint["total"] else 0}
                for r in par_type[:10]
            ]

            # Par mois de l'année en cours
            mois_noms = [_("Janv."), _("Févr."), _("Mars"), _("Avr."), _("Mai"), _("Juin"),
                         _("Juil."), _("Août"), _("Sept."), _("Oct."), _("Nov."), _("Déc.")]
            compte_mois = {r["date_intervention__month"]: r["n"] for r in
                           base.filter(date_intervention__year=annee)
                           .values("date_intervention__month").annotate(n=Count("id"))}
            maint["par_mois"] = [{"label": mois_noms[m - 1], "n": compte_mois.get(m, 0)} for m in range(1, 13)]
            maint["max_mois"] = max([m["n"] for m in maint["par_mois"]] + [1])

            # Rôle tenu sur les maintenances
            roles = [
                (_("Mécanicien"), base.filter(mecanicien_id=user.id).count()),
                (_("Chef mécanicien"), base.filter(chef_mecanicien_id=user.id).count()),
                (_("Apprenti"), base.filter(apprentis_id=user.id).count()),
                (_("Technicien"), base.filter(tech_technicien_id=user.id).count()),
            ]
            maint["par_role"] = [{"label": l, "n": n} for l, n in roles if n]

            maint["dernieres"] = list(
                base.select_related("voiture_exemplaire").order_by("-date_intervention")[:10]
            )

            # Main-d'œuvre encodée sur les interventions
            mo = MainDoeuvre.objects.filter(utilisateur=user)
            agg = mo.aggregate(minutes=Sum("temps_minutes"), nb=Count("id"))
            maint["mo_minutes_total"] = agg["minutes"] or 0
            maint["mo_nb"] = agg["nb"] or 0
            maint["mo_minutes_annee"] = mo.filter(date__year=annee).aggregate(m=Sum("temps_minutes"))["m"] or 0
            cout = ZERO
            for ligne in mo.only("temps_minutes", "taux_horaire"):
                cout += Decimal(ligne.temps_minutes or 0) / Decimal(60) * (ligne.taux_horaire or ZERO)
            maint["mo_cout_total"] = cout.quantize(Decimal("0.01"))

    maint["mo_total_display"] = _heures_minutes(maint["mo_minutes_total"])
    maint["mo_annee_display"] = _heures_minutes(maint["mo_minutes_annee"])

    # ==================================================
    # PAIES : salaires nets et heures prestées
    # ==================================================
    from .models import PaieUtilisateur

    paies = PaieUtilisateur.objects.filter(utilisateur=user).order_by("-annee", "-mois")
    par_annee = OrderedDict()
    for p in paies:
        a = par_annee.setdefault(p.annee, {"annee": p.annee, "nb": 0, "net": ZERO, "heures": ZERO,
                                           "heures_sup": ZERO, "jours": 0, "brut": ZERO})
        a["nb"] += 1
        a["net"] += p.salaire_net_mois or ZERO
        a["heures"] += p.nombre_heures_preste or ZERO
        a["heures_sup"] += p.heures_supplementaires or ZERO
        a["jours"] += p.nombre_jours_preste or 0
        a["brut"] += p.salaire_brut_mensuel or ZERO

    def somme(cle):
        return sum((a[cle] for a in par_annee.values()), ZERO if cle != "jours" and cle != "nb" else 0)

    paie = {
        "nb": somme("nb"),
        "net_total": somme("net"),
        "heures_total": somme("heures"),
        "heures_sup_total": somme("heures_sup"),
        "jours_total": somme("jours"),
        "brut_total": somme("brut"),
        "annee": par_annee.get(annee, {"net": ZERO, "heures": ZERO, "nb": 0}),
        "par_annee": list(par_annee.values()),
        "dernieres": list(paies[:12]),
    }

    return {
        "u": user,
        "societe": societe,
        "adresse": getattr(user, "adresse", None),
        "role_display": user.get_role_display() if hasattr(user, "get_role_display") else user.role,
        "maint": maint,
        "paie": paie,
        "annee": annee,
    }
