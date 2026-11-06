"""Variables de gabarit liées au pays du tenant (Societe.pays)."""
from django.utils.functional import SimpleLazyObject


def pays_tenant(request):
    from core.pays import nom_pays, pays_societe, profil_pays

    return {
        "pays_tenant": SimpleLazyObject(lambda: pays_societe()),
        "pays_tenant_nom": SimpleLazyObject(lambda: nom_pays(pays_societe())),
        "profil_pays_tenant": SimpleLazyObject(lambda: profil_pays(pays_societe())),
    }


def modules_tenant(request):
    """{{ modules.location }} … : modules activés pour la société du tenant (societe/modules.py)."""
    from societe.modules import ModulesActifs

    def charger():
        from dBSolutionV3.middleware.modules_tenant import societe_de
        return ModulesActifs(societe_de(request))

    return {"modules": SimpleLazyObject(charger)}
