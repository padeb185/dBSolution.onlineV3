"""Rappels d'abonnement des particuliers (e-mail + push). À lancer une fois par jour (cron / timer systemd) :

    python manage.py notifier_abonnements
"""
from django.core.management.base import BaseCommand
from django_tenants.utils import schema_context

from particulier.api.base import schema_particuliers
from particulier.notifications import tache_quotidienne


class Command(BaseCommand):
    help = "Envoie les rappels d'abonnement (renouvellement, paiement refusé, fin de formule)."

    def handle(self, *args, **options):
        with schema_context(schema_particuliers()):
            n = tache_quotidienne()
        self.stdout.write(self.style.SUCCESS(f"{n} notification(s) envoyée(s)."))
