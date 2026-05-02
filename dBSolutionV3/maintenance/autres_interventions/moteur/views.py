from datetime import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
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
from maintenance.autres_interventions.moteur.admission.models import Admission
from maintenance.autres_interventions.moteur.alternateur.models import Alternateur
from maintenance.autres_interventions.moteur.courroie.models import CourroieDistribution
from maintenance.autres_interventions.moteur.remplacement_moteur.models import RemplacementMoteur
from maintenance.autres_interventions.moteur.turbo.models import Turbo





@login_required
def liste_moteur_all_view(request):
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
def dashboard_moteur_view(request, exemplaire_id):
    tenant = request.user.societe

    with tenant_context(tenant):

        user = request.user
        context = {}

        # 🔹 Récupérer l'exemplaire AVANT
        exemplaire = get_object_or_404(VoitureExemplaire, id=exemplaire_id)

        # --- Sécurité tenant ---
        tenant_schema = getattr(request, 'tenant', None)
        schema_name = tenant_schema.schema_name if tenant_schema else None


        total_admission = total_alternateur = total_courroie = total_remplacement_moteur =  0

        admission = alternateur = courroie = moteur_remplacement =[]



        if schema_name:
            with schema_context(schema_name):

                # ✅ FILTRAGE PAR EXEMPLAIRE

                admission = Admission.objects.filter(voiture_exemplaire=exemplaire)
                alternateur = Alternateur.objects.filter(voiture_exemplaire=exemplaire)
                courroie = CourroieDistribution.objects.filter(voiture_exemplaire=exemplaire)
                moteur_remplacement = RemplacementMoteur.objects.filter(voiture_exemplaire=exemplaire)
                turbo = Turbo.objects.filter(voiture_exemplaire=exemplaire)


                # ✅ COUNTS CORRECTS
                total_admission = admission.count()
                total_alternateur = alternateur.count()
                total_courroie = courroie.count()
                total_remplacement_moteur = moteur_remplacement.count()
                total_turbo = turbo.count()

                total_int_moteur = total_admission + total_alternateur + total_courroie + total_remplacement_moteur + total_turbo

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
                return redirect('maintenance:list', modele_id=exemplaire.voiture_modele.id)

        # --- CONTEXT ---
        context.update({
            "exemplaire": exemplaire,
            "types_maintenance": TYPES_MAINTENANCE,

            "total_admission": total_admission,
            "total_alternateur": total_alternateur,
            "total_courroie": total_courroie,
            "total_remplacement_moteur": total_remplacement_moteur,
            "total_turbo": total_turbo,

            "admission": admission,
            "alternateur": alternateur,
            "courroie": courroie,
            "moteur_remplacement": moteur_remplacement,
            "turbo": turbo,

            "total_int_moteur": total_int_moteur,

            "modeles": modeles,

        })

        return render(request, "moteur/dashboard_moteur.html", context)





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



