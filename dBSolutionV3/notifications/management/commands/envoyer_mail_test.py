from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Envoie un e-mail de test pour vérifier la configuration (Brevo / SMTP)."

    def add_arguments(self, parser):
        parser.add_argument("destinataire")

    def handle(self, *args, **opts):
        self.stdout.write(f"Backend : {settings.EMAIL_BACKEND}")
        self.stdout.write(f"Expéditeur : {settings.DEFAULT_FROM_EMAIL}")
        n = send_mail("CarsCosts – e-mail de test",
                      "Si vous lisez ce message, l'envoi d'e-mails de CarsCosts fonctionne.",
                      None, [opts["destinataire"]], fail_silently=False)
        self.stdout.write(self.style.SUCCESS(f"{n} e-mail envoyé à {opts['destinataire']}."))
