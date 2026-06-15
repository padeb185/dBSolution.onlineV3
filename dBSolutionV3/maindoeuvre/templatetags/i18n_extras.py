# maindoeuvre/templatetags/i18n_extras.py

from django import template
from django.utils.translation import gettext

register = template.Library()

@register.filter
def db_trans(value):
    if not value:
        return "-"
    return gettext(str(value))