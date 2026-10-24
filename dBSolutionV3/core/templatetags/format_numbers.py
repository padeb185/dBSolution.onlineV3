from django import template

register = template.Library()


def group_by(value, sizes, sep=" "):
    if not value:
        return value

    value = "".join(c for c in value if c.isalnum()).upper()

    result = []
    index = 0

    for size in sizes:
        if index >= len(value):
            break
        result.append(value[index:index + size])
        index += size

    if index < len(value):
        result.append(value[index:])

    return sep.join(result)


@register.filter
def format_iban(value):
    """IBAN en groupes de 4 sur toute sa longueur (BE68 5390 0754 7034, FR76 3000 …)."""
    from core.iban import formater_iban
    return formater_iban(value) if value else value


@register.filter
def format_card(value):
    return group_by(value, [4, 4, 4, 4])


@register.filter
def mask_card(value):
    if not value or len(value) < 4:
        return value
    return "**** **** **** " + value[-4:]

@register.filter
def format_tva(value):
    """Numéro de TVA mis en forme : BE 0123.456.789, FR 12 345 678 901, NL 123456789 B01…"""
    from core.tva import formater_tva
    return formater_tva(value) if value else value
