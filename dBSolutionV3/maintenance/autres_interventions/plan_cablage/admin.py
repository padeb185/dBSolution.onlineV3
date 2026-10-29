from django.contrib import admin

from .models import ConnecteurCablage, FilCablage, PlanCablage

admin.site.register(PlanCablage)
admin.site.register(ConnecteurCablage)
admin.site.register(FilCablage)
