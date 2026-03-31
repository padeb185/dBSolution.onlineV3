from datetime import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.cache import never_cache
from django_tenants.utils import schema_context, tenant_context
from maintenance.models import Maintenance
from maintenance.types_maintenances import TYPES_MAINTENANCE
from voiture.voiture_exemplaire.models import VoitureExemplaire
from voiture.voiture_modele.models import VoitureModele
from maintenance.autres_interventions.boite_de_vitesse.models import ControleBoite
from maintenance.entretien.models import Entretien
from maintenance.freins.models import ControleFreins
from maintenance.jeux_pieces.models import ControleJeuxPieces
from maintenance.nettoyage_exterieur.models import NettoyageExterieur
from maintenance.nettoyage_interieur.models import NettoyageInterieur
from maintenance.niveaux.models import Niveau
from maintenance.pneus.models import ControlePneus
from maintenance.silent_blocs.models import SilentBloc
from maintenance.check_up.models import ControleGeneral
from utilisateurs.models import Mecanicien
from maintenance.autres_interventions.bte_auto.models import ControleBteAuto





@login_required
def liste_autre_all(request):
    tenant = request.user.societe

    with tenant_context(tenant):
        exemplaires = VoitureExemplaire.objects.select_related(
            'voiture_marque', 'voiture_modele'  # Ce sont les bons noms de champs
        ).all().order_by('id')

    return render(
        request,
        'autres_interventions/list.html',
        {
            'exemplaires': exemplaires
        }
    )



@never_cache
@login_required
def choisir_autre_maintenance(request, exemplaire_id):
    user = request.user
    context = {}

    # 🔹 Récupérer l'exemplaire AVANT
    exemplaire = get_object_or_404(VoitureExemplaire, id=exemplaire_id)

    # --- Sécurité tenant ---
    tenant_schema = getattr(request, 'tenant', None)
    schema_name = tenant_schema.schema_name if tenant_schema else None

    total_boite = total_bte_auto =  0

    boite = bte_auto = []

    if schema_name:
        with schema_context(schema_name):

            # ✅ FILTRAGE PAR EXEMPLAIRE
            boite = ControleBoite.objects.filter(voiture_exemplaire=exemplaire)
            bte_auto = ControleBteAuto.objects.filter(voiture_exemplaire=exemplaire)


            # ✅ COUNTS CORRECTS
            total_boite = boite.count()
            total_bte_auto = bte_auto.count()


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
                voiture_exemplaire=exemplaire,
                type_maintenance=type_choisi,
                immatriculation=exemplaire.immatriculation,
                date_intervention=date_intervention,
                description=description
            )
            return redirect('maintenance:list', modele_id=exemplaire.voiture_modele.id)

    # --- CONTEXT ---
    context.update({
        "exemplaire": exemplaire,
        "types_maintenance": TYPES_MAINTENANCE,

        "total_boite": total_boite,
        "total_bte_auto": total_bte_auto,

        "boite": boite,
        "bte_auto": bte_auto,


        "modeles": modeles,

    })

    return render(request, "autres_interventions/choisir_autre.html", context)





@login_required
def maintenance_tenant_view(request, exemplaire_id):
    tenant = request.user.societe

    with tenant_context(tenant):
        # 🔎 Vérifie que l'exemplaire appartient au tenant
        exemplaire = get_object_or_404(
            VoitureExemplaire.objects.filter(
                Q(client__societe=tenant) | Q(client__isnull=True, societe=tenant)
            ),
            id=exemplaire_id
        )

        # Vérifie que l'utilisateur est mécanicien
        if request.user.role != "mécanicien":
            messages.error(request, "Seuls les mécaniciens peuvent effectuer un check-up.")
            return redirect("maintenance:choisir_type", exemplaire.id)

        mecanicien = get_object_or_404(Mecanicien, id=request.user.id)

        if request.method == "POST":
            try:
                with transaction.atomic():

                    # 🧰 Création de la maintenance
                    maintenance = Maintenance.objects.create(
                        voiture_exemplaire=exemplaire,
                        mecanicien=mecanicien,
                        immatriculation=exemplaire.immatriculation,
                        date_intervention=timezone.now().date(),
                        kilometres_total=exemplaire.kilometres_total,
                        kilometres_derniere_intervention=exemplaire.kilometres_derniere_intervention,
                        type_maintenance="checkup",
                        tag=Maintenance.Tag.JAUNE,
                    )

                    # 🔧 Création du contrôle général
                    ControleGeneral.objects.create(
                        maintenance=maintenance
                    )

                    # 👤 Dernier mécanicien ayant fait la maintenance
                    exemplaire.last_maintained_by = request.user
                    exemplaire.save(update_fields=["last_maintained_by"])

                messages.success(request, "Check-up créé avec succès.")

                # 🚀 Redirection vers le contrôle complet
                return redirect(
                    "maintenance:controle_total_view",
                    exemplaire_id=exemplaire.id
                )

            except Exception as e:
                messages.error(request, f"Erreur lors de la création : {e}")

        # GET → affiche la page de confirmation
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



@login_required
def maintenance_liste_view(request):
    maintenances = Maintenance.objects.all().order_by("-date_intervention")

    return render(
        request,
        "maintenance/liste.html",
        {
            "maintenances": maintenances
        }
    )