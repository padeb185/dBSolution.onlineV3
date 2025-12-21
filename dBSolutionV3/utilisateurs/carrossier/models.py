# Create your models here.
import uuid
from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from utilisateurs.models import Utilisateur  # ton