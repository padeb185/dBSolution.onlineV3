from django.conf import settings
from django.contrib.auth import password_validation
from django.utils.translation import gettext as _
from django.urls import reverse
from rest_framework import serializers

from ..models import Depense, Document, Entretien, Plein, Rappel, ReleveKilometrique, Vehicule
from .. import calculs


class FichierMixin:
    """Les champs fichier sont exposés comme URL de l'API (jamais /media/)."""
    fichiers = {}   # champ → nom de route

    def to_representation(self, instance):
        data = super().to_representation(instance)
        for champ, route in self.fichiers.items():
            data[champ] = (self.context["request"].build_absolute_uri(reverse(route, args=[instance.pk]))
                           if getattr(instance, champ) else None)
        return data


class VehiculeChampMixin:
    """Le véhicule doit appartenir à l'utilisateur."""

    def get_fields(self):
        fields = super().get_fields()
        request = self.context.get("request")
        if "vehicule" in fields and request is not None:
            fields["vehicule"].queryset = Vehicule.objects.filter(proprietaire=request.user)
        return fields


class VehiculeSerializer(FichierMixin, serializers.ModelSerializer):
    fichiers = {"photo": "api_particulier:vehicule-photo"}
    kilometrage_actuel = serializers.IntegerField(read_only=True)

    class Meta:
        model = Vehicule
        exclude = ["proprietaire"]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_pays_immatriculation(self, v):
        return valider_pays(v)

    def validate_vin(self, v):
        v = (v or "").upper().replace(" ", "")
        if v and len(v) != 17:
            raise serializers.ValidationError(_("Le VIN doit contenir 17 caractères."))
        return v


class ReleveSerializer(VehiculeChampMixin, serializers.ModelSerializer):
    class Meta:
        model = ReleveKilometrique
        fields = ["id", "vehicule", "date", "kilometrage", "created_at"]
        read_only_fields = ["id", "created_at"]


class PleinSerializer(VehiculeChampMixin, FichierMixin, serializers.ModelSerializer):
    """Plein de carburant : carburant restant ¾, ½, ¼, réserve ou fin de réserve."""
    fichiers = {"ticket": "api_particulier:plein-ticket"}
    prix_unitaire = serializers.DecimalField(max_digits=10, decimal_places=3, read_only=True)
    unite = serializers.CharField(read_only=True)

    class Meta:
        model = Plein
        fields = "__all__"
        read_only_fields = ["id", "created_at", "electrique", "montant_htva", "montant_tva"]

    def validate_pays(self, v):
        return valider_pays(v) if v else v

    def validate_niveau_restant(self, v):
        if v == "minimum":
            raise serializers.ValidationError(_("Choix invalide pour le carburant restant."))
        return v

    def validate_carburant(self, v):
        if v == "electricite":
            raise serializers.ValidationError(_("Une recharge électrique s'enregistre dans les recharges."))
        return v

    def validate(self, data):
        # Pays changé sans taux : taux du nouveau pays (recalculé à l'enregistrement)
        if "pays" in data and "taux_tva" not in data:
            data["taux_tva"] = None
        return data


class RechargeSerializer(PleinSerializer):
    """Recharge électrique : même enregistrement qu'un plein, carburant « electricite »."""
    fichiers = {"ticket": "api_particulier:recharge-ticket"}

    class Meta(PleinSerializer.Meta):
        read_only_fields = PleinSerializer.Meta.read_only_fields + ["carburant"]

    def validate_carburant(self, v):
        return v

    def validate_niveau_restant(self, v):
        # Batterie restante : ¾, ½, ¼ ou au minimum
        if v and v not in ("3/4", "1/2", "1/4", "minimum"):
            raise serializers.ValidationError(_("Choix invalide pour la batterie restante."))
        return v


class EntretienSerializer(VehiculeChampMixin, FichierMixin, serializers.ModelSerializer):
    fichiers = {"facture": "api_particulier:entretien-facture"}

    class Meta:
        model = Entretien
        fields = "__all__"
        read_only_fields = ["id", "created_at"]


class DocumentSerializer(VehiculeChampMixin, FichierMixin, serializers.ModelSerializer):
    fichiers = {"fichier": "api_particulier:document-fichier"}
    type_libelle = serializers.CharField(source="get_type_display", read_only=True)

    class Meta:
        model = Document
        fields = "__all__"
        read_only_fields = ["id", "created_at"]

    def validate(self, data):
        debut, fin = data.get("date_debut"), data.get("date_expiration")
        if debut and fin and fin < debut:
            raise serializers.ValidationError({"date_expiration": _("L'expiration précède le début de validité.")})
        return data


class RappelSerializer(VehiculeChampMixin, serializers.ModelSerializer):
    statut = serializers.SerializerMethodField()

    class Meta:
        model = Rappel
        fields = "__all__"
        read_only_fields = ["id", "created_at", "document"]

    def get_statut(self, obj):
        km = self.context.get("km_par_vehicule", {}).get(obj.vehicule_id)
        if km is None:
            km = obj.vehicule.kilometrage_actuel
        return calculs.statut_rappel(obj, km)

    def validate(self, data):
        date_, km = data.get("echeance_date"), data.get("echeance_km")
        if self.instance is None and not date_ and km is None:
            raise serializers.ValidationError("Indiquez une échéance (date ou kilométrage).")
        return data


class DepenseSerializer(VehiculeChampMixin, serializers.ModelSerializer):
    class Meta:
        model = Depense
        fields = "__all__"
        read_only_fields = ["id", "created_at"]


# ------------------------------------------------------------------
# Comptes
# ------------------------------------------------------------------
LANGUES = [code for code, _nom in settings.LANGUAGES]


def valider_pays(v):
    from ..pays import CODES_PAYS
    v = (v or "").upper()
    if v not in CODES_PAYS:
        raise serializers.ValidationError(_("Pays d'immatriculation inconnu (code ISO à 2 lettres attendu)."))
    return v


class InscriptionSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, trim_whitespace=False)
    prenom = serializers.CharField(max_length=100)
    nom = serializers.CharField(max_length=100)
    langue = serializers.ChoiceField(choices=LANGUES, required=False, default="fr")
    # Pays de l'utilisateur : pays par défaut des véhicules et unités (miles / gallons aux États-Unis…)
    pays = serializers.CharField(max_length=2, required=False)
    unite_distance = serializers.ChoiceField(choices=["km", "mi"], required=False)
    unite_volume = serializers.ChoiceField(choices=["L", "gal_us", "gal_uk"], required=False)

    def validate_pays(self, v):
        return valider_pays(v)

    def validate_email(self, v):
        from utilisateurs.models import Utilisateur
        v = v.strip().lower()
        if Utilisateur.objects.filter(email__iexact=v).exists():
            raise serializers.ValidationError(_("Un compte existe déjà avec cet email."))
        return v

    def validate(self, data):
        from utilisateurs.models import Utilisateur
        password_validation.validate_password(
            data["password"], Utilisateur(email=data["email"], nom=data["nom"], prenom=data["prenom"]))
        return data


class UtilisateurSerializer(serializers.Serializer):
    """Profil + préférences (langue, pays par défaut, rangées dans le schéma des particuliers)."""
    id = serializers.UUIDField(read_only=True)
    email = serializers.EmailField(read_only=True)
    prenom = serializers.CharField(max_length=100)
    nom = serializers.CharField(max_length=100)
    telephone = serializers.CharField(max_length=20, allow_blank=True, required=False, allow_null=True)
    langue = serializers.ChoiceField(choices=LANGUES, required=False)
    pays_defaut = serializers.CharField(max_length=2, required=False)
    unite_distance = serializers.ChoiceField(choices=["km", "mi"], required=False)
    unite_volume = serializers.ChoiceField(choices=["L", "gal_us", "gal_uk"], required=False)

    PREFERENCES = ("langue", "pays_defaut", "unite_distance", "unite_volume")

    def validate_pays_defaut(self, v):
        return valider_pays(v)

    def to_representation(self, instance):
        from ..models import PreferencesParticulier
        data = {
            "id": str(instance.pk), "email": instance.email, "prenom": instance.prenom, "nom": instance.nom,
            "telephone": instance.telephone,
        }
        prefs = PreferencesParticulier.objects.filter(utilisateur=instance).first()
        data["langue"] = prefs.langue if prefs else "fr"
        data["pays_defaut"] = prefs.pays_defaut if prefs else "BE"
        data["unite_distance"] = prefs.unite_distance if prefs else "km"
        data["unite_volume"] = prefs.unite_volume if prefs else "L"
        return data

    def update(self, instance, data):
        from ..models import PreferencesParticulier
        prefs = {k: data.pop(k) for k in self.PREFERENCES if k in data}
        for k, v in data.items():
            setattr(instance, k, v)
        if data:
            instance.save(update_fields=list(data) + ["updated_at"])
        if prefs:
            PreferencesParticulier.objects.update_or_create(utilisateur=instance, defaults=prefs)
        return instance


class MotDePasseSerializer(serializers.Serializer):
    ancien = serializers.CharField(trim_whitespace=False)
    nouveau = serializers.CharField(trim_whitespace=False)

    def validate_ancien(self, v):
        if not self.context["request"].user.check_password(v):
            raise serializers.ValidationError(_("Mot de passe actuel incorrect."))
        return v

    def validate(self, data):
        password_validation.validate_password(data["nouveau"], self.context["request"].user)
        return data


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(trim_whitespace=False)

    def validate_password(self, v):
        if not self.context["request"].user.check_password(v):
            raise serializers.ValidationError(_("Mot de passe incorrect."))
        return v

    def validate_email(self, v):
        from django_tenants.utils import get_public_schema_name, schema_context
        from utilisateurs.models import Utilisateur
        v = v.strip().lower()
        with schema_context(get_public_schema_name()):
            if Utilisateur.objects.filter(email__iexact=v).exclude(pk=self.context["request"].user.pk).exists():
                raise serializers.ValidationError(_("Un compte existe déjà avec cet email."))
        return v
