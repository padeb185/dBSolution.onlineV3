import os
import sys
import django

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dBSolutionV3.settings")

django.setup()

from django_tenants.utils import tenant_context
from societe.models import Societe
from maintenance.autres_interventions.moteur.admission.models import Admission
from voiture_exemplaire.models import VoitureExemplaire

tenant = Societe.objects.get(schema_name="dbsolution")

with tenant_context(tenant):

    voiture = VoitureExemplaire.objects.first()

    qs = Admission.objects.filter(voiture_exemplaire__isnull=True)

    print("Fix:", qs.count())

    qs.update(voiture_exemplaire=voiture)

    print("DONE")