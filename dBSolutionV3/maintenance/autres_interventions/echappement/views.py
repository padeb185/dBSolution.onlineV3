from django.shortcuts import get_object_or_404, redirect

from django.views.decorators.cache import never_cache

from django.contrib.auth.decorators import login_required
from django_tenants.utils import tenant_context, schema_context
from maintenance.models import Maintenance
from maintenance.types_maintenances import TYPES_MAINTENANCE
from voiture.voiture_exemplaire.models import VoitureExemplaire
from voiture.voiture_modele.models import VoitureModele


@never_cache
@login_required
def dashboard_echappement_view(request, exemplaire_id):
    tenant = request.user.societe

    with tenant_context(tenant):

        user = request.user
        context = {}

        # 🔹 Récupérer l'exemplaire AVANT
        exemplaire = get_object_or_404(VoitureExemplaire, id=exemplaire_id)

        # --- Sécurité tenant ---
        tenant_schema = getattr(request, 'tenant', None)
        schema_name = tenant_schema.schema_name if tenant_schema else None


        total_boite = total_remplacement_boite = total_int_boite = 0

        boite = remplacement_boite  = []



        if schema_name:
            with schema_context(schema_name):

                # ✅ FILTRAGE PAR EXEMPLAIRE

                echappement = ControleEchappement.objects.filter(voiture_exemplaire=exemplaire)
                collecteur = CollecteurEchappement.objects.filter(voiture_exemplaire=exemplaire)


                # ✅ COUNTS CORRECTS
                total_echappement = echappement.count()
                total_collecteur = collecteur.count()
                total_int_boite = echappement.count() + collecteur.count()


                total_int_boite = total_echappement + total_collecteur

                modeles = VoitureModele.objects.all()
        else:
            modeles = []

        # --- POST ---
        if request.method == "POST":
            type_choisi = request.POST.get("type_maintenance")
            date_intervention = request.POST.get("date_intervention")
            description = request.POST.get("description", "")

            if type_choisi and date_intervention:
                Maintenance.objects.create(
                    societe=tenant,
                    voiture_exemplaire=exemplaire,
                    type_maintenance=type_choisi,
                    immatriculation=exemplaire.immatriculation,
                    date_intervention=date_intervention,
                    description=description
                )
                return redirect(
                    'maintenance:dashboard_echappement',
                    exemplaire_id=exemplaire.id
                )

        # --- CONTEXT ---
        context.update({
            "exemplaire": exemplaire,
            "types_maintenance": TYPES_MAINTENANCE,

            "total_boite": total_boite,
            "total_remplacement_boite": total_remplacement_boite,
            "total_int_boite": total_int_boite,

            "boite": boite,
            "remplacement_boite": remplacement_boite,


            "modeles": modeles,

        })

        return render(request, "boite_de_vitesse/dashboard_boite.html", context)

