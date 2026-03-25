class TechnicienMixin:
    def assign_technicien(self, user):
        self.tech_technicien = user
        self.tech_nom_technicien = f"{user.prenom} {user.nom}"
        self.tech_role_technicien = user.role
        self.tech_societe = user.societe

    def save(self, *args, **kwargs):
        if not self.tech_technicien and hasattr(self, '_user'):
            self.assign_technicien(self._user)
        super().save(*args, **kwargs)