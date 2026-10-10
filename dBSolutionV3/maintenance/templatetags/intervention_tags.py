from django import template

register = template.Library()


@register.filter
def premier(obj, cles):
    """
    Renvoie la première valeur non vide parmi plusieurs clés/attributs.
    Usage : {{ ligne|premier:"champ,nom,label" }}
    Contrairement à |default, une clé absente ne provoque pas d'erreur.
    """
    if obj is None:
        return ""
    for cle in str(cles).split(","):
        cle = cle.strip()
        if isinstance(obj, dict):
            valeur = obj.get(cle)
        else:
            valeur = getattr(obj, cle, None)
        if callable(valeur):
            try:
                valeur = valeur()
            except TypeError:
                continue
        if valeur not in (None, "", [], ()):
            return valeur
    return ""
