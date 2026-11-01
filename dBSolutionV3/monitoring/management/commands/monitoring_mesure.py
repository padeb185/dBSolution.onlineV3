"""
Mesure du serveur à la demande (à planifier toutes les 5 minutes avec cron pour un historique
régulier même sans trafic) :

    */5 * * * * cd /var/www/carscosts/dBSolutionV3 && /var/www/carscosts/.venv/bin/python manage.py monitoring_mesure
"""
from django.core.management.base import BaseCommand

from monitoring.collecte import prendre_mesure


class Command(BaseCommand):
    help = "Enregistre une mesure du serveur (CPU, mémoire, disque, utilisateurs en ligne) et purge l'historique."

    def handle(self, *args, **options):
        m = prendre_mesure()
        self.stdout.write(self.style.SUCCESS(
            f"Mesure {m.horodatage:%d/%m/%Y %H:%M} – CPU {m.cpu} % – RAM {m.ram_pourcent} % – "
            f"en ligne {m.en_ligne} / sessions {m.sessions}"
        ))
