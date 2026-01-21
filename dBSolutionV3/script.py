import uuid
from datetime import timedelta, date

from django.utils.text import slugify

from societe.models import Societe, Domain
from adresse.models import Adresse
from django.contrib.auth import get_user_model

# 1️⃣ Créer une adresse pour le tenant public
adresse_public = Adresse.objects.create(
    rue="Place de Cochem",
    numero="3A",
    code_postal="4960",
    ville="Malmedy",
    pays="Belgique"
)

# 2️⃣ Créer le tenant public
societe = Societe.objects.create(
    schema_name="dbsolution",
    nom_du_type="dbsolution",
    nom="dbsolution",
    adresse=adresse_public,
    paid_until=date.today() + timedelta(days=365),
    slug=slugify("dbsolution"),
    numero_tva="BE1234567891"

)

# 3️⃣ Créer le domaine pour ce tenant
Domain.objects.create(
    domain="127.0.0.1:8000",  # ou ton domaine local / dev
    tenant=societe,
    is_primary=True
)

from utilisateurs.models import Utilisateur

superuser = Utilisateur.objects.create_superuser(
    email="pierre.andre1367@gmail.com",
    prenom="Pierre André",
    last_name="de Bournonville",
    password="9y7-T!c&wi]vwm&,s|#kFlD=@4skRG6ri#Z90GT,",
    is_active=True
)

print("Tenant dbsolution et superuser global créés avec succès !")

