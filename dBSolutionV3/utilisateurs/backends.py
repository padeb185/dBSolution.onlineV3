from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django_tenants.utils import get_public_schema_name, schema_context



class PublicSchemaModelBackend(ModelBackend):

    def authenticate(
        self,
        request,
        username=None,
        password=None,
        email=None,
        **kwargs,
    ):
        UserModel = get_user_model()

        identifiant = email or username or kwargs.get(
            UserModel.USERNAME_FIELD
        )

        if not identifiant or not password:
            return None

        public_schema_name = get_public_schema_name()

        with schema_context(public_schema_name):
            try:
                utilisateur = (
                    UserModel._default_manager
                    .select_related("societe")
                    .get(email__iexact=identifiant)
                )
            except UserModel.DoesNotExist:
                return None

            if not utilisateur.check_password(password):
                return None

            if not self.user_can_authenticate(utilisateur):
                return None

            return utilisateur

    def get_user(self, user_id):
        from django.db import connection
        from django.contrib.auth import get_user_model
        from django_tenants.utils import (
            get_public_schema_name,
            schema_context,
        )

        UserModel = get_user_model()
        public_schema_name = get_public_schema_name()

        print("========== BACKEND GET_USER ==========")
        print("USER ID :", user_id)
        print("SCHEMA AVANT :", connection.schema_name)

        with schema_context(public_schema_name):
            print("SCHEMA RECHERCHE :", connection.schema_name)

            try:
                utilisateur = (
                    UserModel._default_manager
                    .select_related("societe")
                    .get(pk=user_id)
                )
            except UserModel.DoesNotExist:
                print("UTILISATEUR INTROUVABLE")
                return None

            if not self.user_can_authenticate(utilisateur):
                print("UTILISATEUR INACTIF")
                return None

            print("UTILISATEUR TROUVÉ :", utilisateur.email)
            print(
                "SOCIÉTÉ PRÉCHARGÉE :",
                getattr(utilisateur.societe, "schema_name", None),
            )

            return utilisateur