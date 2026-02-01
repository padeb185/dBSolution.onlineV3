from utilisateurs.models import Utilisateur


class Mecanicien(Utilisateur):
    class Meta:
        proxy = True  # Très important si tu ne veux pas créer une table supplémentaire

    def __str__(self):
        return f"{self.prenom} {self.nom} - {self.get_role_display()}"
