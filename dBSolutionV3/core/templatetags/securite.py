from django import template

from core.securite import url_sure

register = template.Library()


@register.filter
def lien_sur(url):
    """Lien interne uniquement (sinon vide) : {{ request.META.HTTP_REFERER|lien_sur|default:url_liste }}."""
    return url_sure(url)
