from utilisateurs.models import Utilisateur

class Vendeur(Utilisateur):
    def __str__(self):
        # Ici tu peux accéder au champ role du parent
        return f"{self.prenom} {self.nom} - {self.get_role_display()}"
