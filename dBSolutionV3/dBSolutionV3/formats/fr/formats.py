"""
Français : formats de Django, avec une espace fine insécable (U+202F) comme séparateur des milliers
(1 234 567,50) – plus légère que l'espace insécable par défaut.
"""
from django.conf.locale.fr.formats import *  # noqa: F401,F403

THOUSAND_SEPARATOR = " "
