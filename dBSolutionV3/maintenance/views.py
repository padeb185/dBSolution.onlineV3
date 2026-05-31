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
from django.utils.translation import gettext as _
from voiture.voiture_marque.models import VoitureMarque
from voiture.voiture_exemplaire.models import TypeUtilisation
from django.utils import timezone
from maintenance.types_maintenances import TYPES_MAINTENANCE
from utilisateurs.models import Mecanicien
from maintenance.jeux_pieces.models import ControleJeuxPieces
from maintenance.nettoyage_exterieur.models import NettoyageExterieur
from maintenance.nettoyage_interieur.models import NettoyageInterieur
from maintenance.freins.models import ControleFreins
from maintenance.niveaux.models import Niveau
from maintenance.entretien.models import Entretien
from maintenance.silent_blocs.models import SilentBloc
from maintenance.pneus.models import ControlePneus
from maintenance.autres_interventions.models import AutresInterventions
from maintenance.carrosserie_interne.models import CarrosserieInterne
from maintenance.checkup_track.models import CheckupTrack
from maintenance.autres_interventions.boite_de_vitesse.models import ControleBoite
from maintenance.autres_interventions.bte_vitesse_auto.models import ControleBteVitesseAuto
from maintenance.autres_interventions.geometrie.models import GeometrieVoiture
from maintenance.autres_interventions.moteur.admission.models import Admission
from maintenance.autres_interventions.moteur.alternateur.models import Alternateur
from maintenance.autres_interventions.abs.models import Abs
from maintenance.autres_interventions.moteur.courroie.models import CourroieDistribution
from maintenance.autres_interventions.moteur.remplacement_moteur.models import RemplacementMoteur
from maintenance.autres_interventions.moteur.turbo.models import Turbo
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

    # 🔹 Récupérer l'exemplaire AVANT
    exemplaire = get_object_or_404(VoitureExemplaire, id=exemplaire_id)

    # --- Sécurité tenant ---
    tenant_schema = getattr(request, 'tenant', None)
    schema_name = tenant_schema.schema_name if tenant_schema else None

    total_checkup = total_entretien = total_freins = total_pneus = \
    total_niveaux = total_nettoyage_exterieur = total_nettoyage_interieur = \
    total_autres = total_jeux_pieces = total_silent = total_carrosserie_interne = total_checkup_track =  0

    checkup = entretien = nettoyage_exterieur = jeux_pieces = nettoyage_interieur = \
        freins = niveaux = pneus = autres = silent = carrosserie_interne = checkup_track = []

    if schema_name:
        with (schema_context(schema_name)):

            # ✅ FILTRAGE PAR EXEMPLAIRE
            checkup = Checkup.objects.filter(voiture_exemplaire=exemplaire)
            entretien = Entretien.objects.filter(voiture_exemplaire=exemplaire)
            freins = ControleFreins.objects.filter(voiture_exemplaire=exemplaire)
            pneus = ControlePneus.objects.filter(voiture_exemplaire=exemplaire)
            niveaux = Niveau.objects.filter(voiture_exemplaire=exemplaire)
            nettoyage_exterieur = NettoyageExterieur.objects.filter(voiture_exemplaire=exemplaire)
            nettoyage_interieur = NettoyageInterieur.objects.filter(voiture_exemplaire=exemplaire)
            autres = AutresInterventions.objects.filter(voiture_exemplaire=exemplaire)
            jeux_pieces = ControleJeuxPieces.objects.filter(voiture_exemplaire=exemplaire)
            silent = SilentBloc.objects.filter(voiture_exemplaire=exemplaire)
            carrosserie_interne = CarrosserieInterne.objects.filter(voiture_exemplaire=exemplaire)
            checkup_track = CheckupTrack.objects.filter(voiture_exemplaire=exemplaire)
            courroie = CourroieDistribution.objects.filter(voiture_exemplaire=exemplaire)
            turbo = Turbo.objects.filter(voiture_exemplaire=exemplaire)
            remplacement_moteur = RemplacementMoteur.objects.filter(voiture_exemplaire=exemplaire)


            # ✅ COUNTS CORRECTS
            total_checkup = checkup.count()
            total_entretien = entretien.count()
            total_freins = freins.count()
            total_pneus = pneus.count()
            total_niveaux = niveaux.count()
            total_nettoyage_exterieur = nettoyage_exterieur.count()
            total_nettoyage_interieur = nettoyage_interieur.count()

            boite = ControleBoite.objects.filter(voiture_exemplaire=exemplaire)
            boite_auto = ControleBteVitesseAuto.objects.filter(voiture_exemplaire=exemplaire)
            geometrie = GeometrieVoiture.objects.filter(voiture_exemplaire=exemplaire)

            admission = Admission.objects.filter(voiture_exemplaire=exemplaire)
            alternateur = Alternateur.objects.filter(voiture_exemplaire=exemplaire)
            abs_qs = Abs.objects.filter(voiture_exemplaire=exemplaire)




            total_autres = boite.count() + boite_auto.count() + geometrie.count() + admission.count() + alternateur.count() + courroie.count() + turbo.count() + remplacement_moteur.count() + abs_qs.count()
            total_jeux_pieces = jeux_pieces.count()
            total_silent = silent.count()
            total_carrosserie_interne = carrosserie_interne.count()
            total_checkup_track = checkup_track.count()

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
        "is_checkup_allowed": request.user.role in [
            "direction",
            "mecanicien",
            "chef_mecanicien",
            "magasinier",
        ],

        "types_maintenance": TYPES_MAINTENANCE,

        "total_checkup": total_checkup,
        "total_entretien": total_entretien,
        'total_freins': total_freins,
        'total_pneus': total_pneus,
        'total_niveaux': total_niveaux,
        'total_autres': total_autres,
        'total_nettoyage_exterieur': total_nettoyage_exterieur,
        'total_nettoyage_interieur': total_nettoyage_interieur,
        'total_jeux_pieces': total_jeux_pieces,
        'total_silent': total_silent,
        'total_carrosserie_interne': total_carrosserie_interne,
        'total_checkup_track': total_checkup_track,

        "checkup": checkup,
        "entretien": entretien,
        'freins': freins,
        'pneus': pneus,
        'niveaux': niveaux,
        'nettoyage_exterieur': nettoyage_exterieur,
        'nettoyage_interieur': nettoyage_interieur,
        'autres': autres,
        'jeux_pieces': jeux_pieces,
        'silent': silent,
        'carrosserie_interne': carrosserie_interne,
        'checkup_track': checkup_track,
        "modeles": modeles,


    })

    return render(request, "maintenance/choisir_type.html", context)

@login_required
def maintenance_tenant_view(request, exemplaire_id):
    tenant = request.user.societe

    with tenant_context(tenant):

        exemplaire = get_object_or_404(
            VoitureExemplaire.objects.filter(
                Q(client__societe=tenant) | Q(client__isnull=True, societe=tenant)
            ),
            id=exemplaire_id
        )

        # 🔴 AUTORISATION CORRIGÉE
        if request.user.role not in ["mecanicien", "chef_mecanicien", "apprenti"]:
            messages.error(request, "Vous n'êtes pas autorisé à effectuer un check-up.")
            return redirect("maintenance:choisir_type", exemplaire.id)

        mecanicien = get_object_or_404(Mecanicien, id=request.user.id)

        if request.method == "POST":
            try:
                with transaction.atomic():

                    maintenance = Maintenance.objects.create(
                        voiture_exemplaire=exemplaire,
                        immatriculation=exemplaire.immatriculation,
                        date_intervention=timezone.now().date(),
                        kilometres_total=exemplaire.kilometres_total,
                        kilometres_derniere_entretien=exemplaire.kilometres_derniere_entretien,
                        type_maintenance="checkup",
                        tag=Maintenance.Tag.JAUNE,
                    )

                    # 🔴 ASSIGNATION SELON RÔLE
                    if request.user.role == "mecanicien":
                        maintenance.mecanicien = request.user

                    elif request.user.role == "chef_mecanicien":
                        maintenance.chef_mecanicien = request.user

                    maintenance.save()

                    # 🔴 M2M APPRENTI
                    if request.user.role == "apprenti":
                        maintenance.apprentis.add(request.user)

                    # 🔧 contrôle général
                    Checkup.objects.create(
                        maintenance=maintenance
                    )

                    # 👤 tracking
                    exemplaire.last_maintained_by = request.user
                    exemplaire.save(update_fields=["last_maintained_by"])

                messages.success(request, "Check-up créé avec succès.")

                return redirect(
                    "maintenance:controle_total_view",
                    exemplaire_id=exemplaire.id
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

    context = {
        "maintenances": maintenances,
        "is_mecanicien": request.user.role in [
            "mecanicien",
            "chef_mecanicien",
            "direction",
            "magasinier",
        ],
    }

    return render(request, "maintenance/liste.html", context)