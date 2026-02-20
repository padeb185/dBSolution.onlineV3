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
    return group_by(value, [4, 4, 4, 4])


@register.filter
def format_card(value):
    return group_by(value, [4, 4, 4, 4])


@register.filter
def mask_card(value):
    if not value or len(value) < 4:
        return value
    return "**** **** **** " + value[-4:]