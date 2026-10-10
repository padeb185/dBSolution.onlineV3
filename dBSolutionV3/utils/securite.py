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
