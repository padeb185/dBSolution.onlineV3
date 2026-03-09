from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.cache import never_cache
from django_tenants.utils import tenant_context, schema_context
from voiture.voiture_exemplaire.models import VoitureExemplaire
from voiture.voiture_modele.models import VoitureModele
from maintenance.models import Maintenance
from maintenance.models import TypeMaintenance
from django.utils.translation import gettext as _
from maintenance.utils import creer_maintenance_complete
from voiture.voiture_marque.models import VoitureMarque
from voiture.voiture_exemplaire.models import TypeUtilisation
from django.utils import timezone
from maintenance.check_up.views import TYPES_MAINTENANCE
from maintenance.check_up.views import creer_checkup_complet
from maintenance.check_up.models import Checkup


@login_required
def liste_maintenance_all(request):
    tenant = request.user.societe

    with tenant_context(tenant):
        exemplaires = VoitureExemplaire.objects.select_related(
            'voiture_marque', 'voiture_modele'  # Ce sont les bons noms de champs
        ).all().order_by('id')

    return render(
        request,
        'maintenance/list.html',
        {
            'exemplaires': exemplaires
        }
    )



@never_cache
@login_required
def choisir_type_maintenance(request, exemplaire_id):
    user = request.user
    context = {}

    # --- Sécurité : récupère le tenant ---
    tenant_schema = getattr(request, 'tenant', None)
    schema_name = tenant_schema.schema_name if tenant_schema else None

    total_checkup = total_entretien = total_freins = total_pneus = \
    total_niveaux = total_nettoyage_exterieur = total_nettoyage_interieur =\
    total_autres = 0
    checkup = entretien = []

    if schema_name:
        with schema_context(schema_name):
            checkup = Maintenance.objects.all()
            entretien = Maintenance.objects.all()
            freins = Maintenance.objects.all()
            pneus = Maintenance.objects.all()
            niveaux = Maintenance.objects.all()
            nettoyage_exterieur = Maintenance.objects.all()
            nettoyage_interieur = Maintenance.objects.all()
            autres = Maintenance.objects.all()

            total_checkup = checkup.count()
            total_entretien = entretien.count()
            total_freins = freins.count()
            total_pneus = pneus.count()
            total_niveaux = niveaux.count()
            total_nettoyage_exterieur = nettoyage_interieur.count()
            total_nettoyage_interieur = nettoyage_interieur.count()
            total_autres = autres.count()
            modeles = VoitureModele.objects.all()
    else:
        modeles = []

    exemplaire = get_object_or_404(VoitureExemplaire, id=exemplaire_id)

    if request.method == "POST":
        type_choisi = request.POST.get("type_maintenance")
        date_intervention = request.POST.get("date_intervention")
        description = request.POST.get("description", "")

        if type_choisi and date_intervention:
            Maintenance.objects.create(
                voiture_exemplaire=exemplaire,
                type_maintenance=type_choisi,
                immatriculation=exemplaire.immatriculation,
                date_intervention=date_intervention,
                description=description
            )
            # Redirige vers la liste de maintenance du modèle
            return redirect('maintenance:list', modele_id=exemplaire.voiture_modele.id)

    # --- Construit le contexte final avec toutes les infos ---
    context.update({
        "exemplaire": exemplaire,
        "types_maintenance": TYPES_MAINTENANCE,
        "total_checkup": total_checkup,
        "total_entretien": total_entretien,
        'total_freins': total_freins,
        'total_pneus': total_pneus,
        'total_niveaux': total_niveaux,
        'total_autres': total_autres,
        'total_nettoyage_exterieur': total_nettoyage_exterieur,
        'total_nettoyage_interieur': total_nettoyage_interieur,

        "checkup": checkup,
        "entretien": entretien,
        'freins': freins,
        'pneus': pneus,
        'niveaux': niveaux,
        'nettoyage_exterieur': nettoyage_exterieur,
        'nettoyage_interieur': nettoyage_interieur,
        'autres': autres,
        "modeles": modeles,
    })

    return render(request, "maintenance/choisir_type.html", context)





@login_required
def maintenance_tenant_view(request, exemplaire_id):
    tenant = request.user.societe

    with tenant_context(tenant):
        # Récupère l'exemplaire correspondant au tenant ou client None
        exemplaire = get_object_or_404(
            VoitureExemplaire.objects.filter(
                Q(client__societe=tenant) | Q(client__isnull=True, societe=tenant)
            ),
            id=exemplaire_id
        )

        if request.method == "POST":
            try:
                with transaction.atomic():
                    # Création du check-up complet
                    maintenance = creer_checkup_complet(request, exemplaire)

                    # Mise à jour du dernier utilisateur ayant fait la maintenance
                    exemplaire.last_maintained_by = request.user
                    exemplaire.save(update_fields=["last_maintained_by"])

                messages.success(request, "Maintenance créée avec succès !")

                # POST → GET : retourne le formulaire avec le lien vers la maintenance créée
                return render(
                    request,
                    "maintenance/creer_maintenance.html",
                    {
                        "exemplaire": exemplaire,
                        "now": timezone.now(),
                        "maintenance": maintenance,  # pour le lien vers détail

                    },
                )

            except Exception as e:
                messages.error(request, f"Erreur lors de la création : {e}")
                return render(
                    request,
                    "maintenance/creer_maintenance.html",
                    {
                        "exemplaire": exemplaire,
                        "now": timezone.now(),

                    },
                )

        # GET → affiche le formulaire de création
        return render(
            request,
            "maintenance/creer_maintenance.html",
            {
                "exemplaire": exemplaire,
                "now": timezone.now(),

            },
        )






@login_required
def maintenance_detail_view(request, maintenance_id):
    tenant = request.user.societe

    # Récupère la maintenance uniquement si elle appartient au tenant
    maintenance = get_object_or_404(
        Maintenance.objects.filter(
            Q(exemplaire__client__societe=tenant) |
            Q(exemplaire__client__isnull=True, exemplaire__societe=tenant)
        ),
        id=maintenance_id
    )

    return render(request, "maintenance/detail.html", {
        "maintenance": maintenance
    })