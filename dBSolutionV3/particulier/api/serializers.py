from django.contrib.auth import password_validation
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
        from ..pays import CODES_PAYS
        v = (v or "").upper()
        if v not in CODES_PAYS:
            raise serializers.ValidationError("Pays d'immatriculation inconnu (code ISO à 2 lettres attendu).")
        return v

    def validate_vin(self, v):
        v = (v or "").upper().replace(" ", "")
        if v and len(v) != 17:
            raise serializers.ValidationError("Le VIN doit contenir 17 caractères.")
        return v


class ReleveSerializer(VehiculeChampMixin, serializers.ModelSerializer):
    class Meta:
        model = ReleveKilometrique
        fields = ["id", "vehicule", "date", "kilometrage", "created_at"]
        read_only_fields = ["id", "created_at"]


class PleinSerializer(VehiculeChampMixin, FichierMixin, serializers.ModelSerializer):
    fichiers = {"ticket": "api_particulier:plein-ticket"}
    prix_unitaire = serializers.DecimalField(max_digits=10, decimal_places=3, read_only=True)

    class Meta:
        model = Plein
        fields = "__all__"
        read_only_fields = ["id", "created_at"]


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
            raise serializers.ValidationError({"date_expiration": "L'expiration précède le début de validité."})
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
class InscriptionSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, trim_whitespace=False)
    prenom = serializers.CharField(max_length=100)
    nom = serializers.CharField(max_length=100)

    def validate_email(self, v):
        from utilisateurs.models import Utilisateur
        v = v.strip().lower()
        if Utilisateur.objects.filter(email__iexact=v).exists():
            raise serializers.ValidationError("Un compte existe déjà avec cet email.")
        return v

    def validate(self, data):
        from utilisateurs.models import Utilisateur
        password_validation.validate_password(
            data["password"], Utilisateur(email=data["email"], nom=data["nom"], prenom=data["prenom"]))
        return data


class UtilisateurSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    email = serializers.EmailField(read_only=True)
    prenom = serializers.CharField(max_length=100)
    nom = serializers.CharField(max_length=100)
    telephone = serializers.CharField(max_length=20, allow_blank=True, required=False, allow_null=True)

    def update(self, instance, data):
        for k, v in data.items():
            setattr(instance, k, v)
        instance.save(update_fields=list(data) + ["updated_at"])
        return instance
