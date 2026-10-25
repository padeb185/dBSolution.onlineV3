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


# ------------------------------------------------------------
# Interventions (maintenances) : création / modification réservées à l'atelier
# (même liste que les vues de création ; « apprentis » est la valeur réelle du rôle en base)
# ------------------------------------------------------------
ROLES_ATELIER = ("mecanicien", "apprenti", "apprentis", "magasinier", "chef_mecanicien", "direction")


def roles_requis(*roles):
    """
    Décorateur de vue : accès réservé aux rôles donnés (et au super admin).
    Usage : @roles_requis(*ROLES_ATELIER)
    """
    from functools import wraps

    def decorateur(vue):
        @wraps(vue)
        def enveloppe(request, *args, **kwargs):
            user = request.user
            if not (getattr(user, "is_superuser", False) or getattr(user, "role", None) in roles):
                from django.contrib import messages
                from django.shortcuts import redirect
                from django.utils.translation import gettext as _
                messages.error(request, _("Accès refusé"))
                return redirect("utilisateurs:dashboard")
            return vue(request, *args, **kwargs)
        return enveloppe
    return decorateur


atelier_requis = roles_requis(*ROLES_ATELIER)
