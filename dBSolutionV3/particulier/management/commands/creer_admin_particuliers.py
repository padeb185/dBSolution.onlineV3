"""
Crée (ou met à jour) un administrateur du tenant des particuliers :
    python manage.py creer_admin_particuliers --email admin@carscosts.com --prenom Pierre --nom Admin

Le mot de passe est demandé (ou --password). L'administrateur (rôle direction, staff) a accès à :
    /tenant/<schéma particuliers>/fr/particuliers/   page de gestion des comptes
    /tenant/<schéma particuliers>/fr/admin/          admin Django (modèles « particulier »)
"""
import getpass

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError
from django_tenants.utils import get_public_schema_name, schema_context


class Command(BaseCommand):
    help = "Crée un administrateur (direction, staff) du tenant des particuliers."

    def add_arguments(self, parser):
        parser.add_argument("--email", required=True)
        parser.add_argument("--prenom", default="Admin")
        parser.add_argument("--nom", default="Particuliers")
        parser.add_argument("--password", help="Sinon demandé de manière masquée.")

    def handle(self, *args, **o):
        from societe.models import Societe
        from utilisateurs.models import Utilisateur
        schema = getattr(settings, "PARTICULIERS_SCHEMA", "particuliers")
        email = o["email"].strip().lower()
        with schema_context(get_public_schema_name()):
            societe = Societe.objects.filter(schema_name=schema).first()
            if societe is None:
                raise CommandError("Le tenant des particuliers n'existe pas : lancez d'abord creer_tenant_particuliers.")
            existant = Utilisateur.objects.filter(email__iexact=email).first()
            if existant and existant.societe_id != societe.id_societe:
                raise CommandError("Cet email appartient déjà à un utilisateur d'une autre société.")
            if existant and existant.role == "particulier":
                raise CommandError("Cet email est un compte particulier de l'application : utilisez une autre adresse.")
            password = o.get("password")
            while not password:
                password = getpass.getpass("Mot de passe : ")
                if password != getpass.getpass("Confirmation : "):
                    self.stderr.write("Les mots de passe ne correspondent pas.")
                    password = None
            try:
                Utilisateur.objects.validate_password(password)
            except Exception as e:
                raise CommandError(" ".join(getattr(e, "messages", [str(e)])))
            if existant:
                user = existant
                user.set_password(password)
                user.role, user.is_staff, user.is_active = "direction", True, True
                user.save()
                self.stdout.write(self.style.SUCCESS(f"Administrateur mis à jour : {email}"))
            else:
                user = Utilisateur.objects.create_user(
                    email=email, password=password, prenom=o["prenom"], nom=o["nom"], role="direction",
                    societe=societe, schema_name=societe.schema_name, is_staff=True,
                )
                self.stdout.write(self.style.SUCCESS(f"Administrateur créé : {email}"))
            self.stdout.write(f"Connexion : /fr/connexion/ puis /tenant/{schema}/fr/particuliers/ (admin Django : /tenant/{schema}/fr/admin/)")
