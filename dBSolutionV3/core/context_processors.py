"""Variables de gabarit liées au pays du tenant (Societe.pays)."""
from django.utils.functional import SimpleLazyObject


def pays_tenant(request):
    from core.pays import nom_pays, pays_societe, profil_pays

    return {
        "pays_tenant": SimpleLazyObject(lambda: pays_societe()),
        "pays_tenant_nom": SimpleLazyObject(lambda: nom_pays(pays_societe())),
        "profil_pays_tenant": SimpleLazyObject(lambda: profil_pays(pays_societe())),
    }
