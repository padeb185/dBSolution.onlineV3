from django.db.models import Q


def q_intervention_tenant(user, prefix="voiture_exemplaire__"):
    """
    Filtre limitant une intervention de maintenance à la société de l'utilisateur :
    - véhicule d'un client de la société,
    - véhicule de la société sans client,
    - ou intervention sans véhicule réalisée par la société.
    Le superutilisateur voit tout.
    """
    if getattr(user, "is_superuser", False):
        return Q()

    societe = getattr(user, "societe", None)
    return (
        Q(**{f"{prefix}client__societe": societe})
        | Q(**{f"{prefix}client__isnull": True, f"{prefix}societe": societe})
        | Q(voiture_exemplaire__isnull=True, tech_societe=societe)
    )


# ------------------------------------------------------------
# Suppressions : réservées à la direction, au chef mécanicien et au super admin
# ------------------------------------------------------------
ROLES_SUPPRESSION = ("direction", "chef_mecanicien")


def peut_supprimer(user):
    return bool(
        getattr(user, "is_superuser", False)
        or getattr(user, "role", None) in ROLES_SUPPRESSION
    )


def refuser_suppression(request):
    from django.contrib import messages
    from django.shortcuts import redirect
    from django.utils.translation import gettext as _

    messages.error(request, _("Accès refusé"))
    return redirect("utilisateurs:dashboard")
