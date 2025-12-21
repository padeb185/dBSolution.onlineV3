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
    schema_name="public",
    nom="Admin Global",
    adresse=adresse_public,
    paid_until=date.today() + timedelta(days=365),
    slug=slugify("Admin Global"),
    numero_tva="ADMIN-000"# valeur obligatoire pour paid_until

)

# 3️⃣ Créer le domaine pour ce tenant
Domain.objects.create(
    domain="127.0.0.1:8000",  # ou ton domaine local / dev
    tenant=societe,
    is_primary=True
)

# 4️⃣ Créer un superuser global (dans le schema public)
User = get_user_model()
if not User.objects.filter(username="admin_global").exists():
    User.objects.create_superuser(
        username="Pierre-AndredeBournonville",
        email="pierre;andre1367@gmail.com",
        password="JIsWrpuRfjkW9bBFPd1GLsIFRFgbbxKrqWjZXxGd",
        first_name="Pierre",
        last_name="Andre",
        is_active=True
    )

print("Tenant public et superuser global créés avec succès !")

