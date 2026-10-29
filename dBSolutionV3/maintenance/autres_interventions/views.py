from datetime import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.cache import never_cache
from django_tenants.utils import schema_context, tenant_context
from maintenance.autres_interventions.cardan.models import Cardan
from maintenance.autres_interventions.roulement.models import Roulement
from maintenance.autres_interventions.climatisation.models import Climatisation
from maintenance.autres_interventions.courroie_accessoires.models import CourroieAccessoires
from maintenance.autres_interventions.echappement.models import Echappement
from maintenance.autres_interventions.echappement.composants import total_composants_echappement
from maintenance.autres_interventions.batterie.models import Batterie
from maintenance.autres_interventions.embrayage.models import Embrayage
from maintenance.autres_interventions.moteur.allumage.models import Allumage
from maintenance.autres_interventions.refroidissement.models import Refroidissement
from maintenance.models import Maintenance
from maintenance.types_maintenances import TYPES_MAINTENANCE
from voiture.voiture_exemplaire.models import VoitureExemplaire
from voiture.voiture_modele.models import VoitureModele
from maintenance.autres_interventions.boite_de_vitesse.models import ControleBoite
from utilisateurs.models import Mecanicien
from maintenance.autres_interventions.bte_vitesse_auto.models import ControleBteVitesseAuto
from maintenance.autres_interventions.geometrie.models import GeometrieVoiture
from maintenance.autres_interventions.moteur.admission.models import Admission
from maintenance.autres_interventions.moteur.alternateur.models import Alternateur
from maintenance.autres_interventions.abs.models import Abs
from maintenance.autres_interventions.moteur.courroie.models import CourroieDistribution
from maintenance.autres_interventions.moteur.chaine_distribution.models import ChaineDistribution
from maintenance.autres_interventions.moteur.culasse.models import Culasse
from maintenance.autres_interventions.moteur.bas_moteur.models import BasMoteur
from maintenance.autres_interventions.moteur.metrologie_moteur.models import MetrologieMoteur
from maintenance.autres_interventions.moteur.casse_moteur.models import CasseMoteur
from maintenance.autres_interventions.moteur.montage_turbo.models import MontageTurbo
from maintenance.autres_interventions.boite_de_vitesse.casse_boite.models import CasseBoite
from maintenance.autres_interventions.moteur.bougies.composants import total_bougies
from maintenance.autres_interventions.moteur.electronique_moteur.models import ElectroniqueMoteur
from maintenance.autres_interventions.moteur.lubrification.models import Lubrification
from maintenance.autres_interventions.moteur.remplacement_moteur.models import RemplacementMoteur
from maintenance.autres_interventions.boite_de_vitesse.remplacement_boite.models import RemplacementBoite
from maintenance.autres_interventions.bte_vitesse_auto.remplacement_bte_auto.models import RemplacementBteAuto
from maintenance.autres_interventions.moteur.turbo.models import Turbo





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
    tenant = user.societe

    # ✅ EXEMPLAIRE SÉCURISÉ TENANT
    exemplaire = get_object_or_404(
        VoitureExemplaire.objects.filter(societe=tenant),
        id=exemplaire_id
    )

    schema_name = getattr(
        getattr(request, "tenant", None),
        "schema_name",
        None
    )

    # -----------------------------
    # QUERYSETS VIDES PAR DÉFAUT
    # -----------------------------
    boite = ControleBoite.objects.none()
    bte_auto = ControleBteVitesseAuto.objects.none()
    geometrie = GeometrieVoiture.objects.none()
    abs_qs = Abs.objects.none()
    remplacement_boite = RemplacementBoite.objects.none()
    remplacement_bte_auto = RemplacementBteAuto.objects.none()
    courroie_access = CourroieAccessoires.objects.none()
    admission = Admission.objects.none()
    alternateur = Alternateur.objects.none()
    courroie = CourroieDistribution.objects.none()
    chaine = ChaineDistribution.objects.none()
    culasse = Culasse.objects.none()
    bas_moteur = BasMoteur.objects.none()
    electronique = ElectroniqueMoteur.objects.none()
    lubrification = Lubrification.objects.none()
    turbo = Turbo.objects.none()
    remplacement_moteur = RemplacementMoteur.objects.none()
    echappement = Echappement.objects.none()
    composants_ech_total = 0
    batterie = Batterie.objects.none()
    climatisation = Climatisation.objects.none()
    refroidissement = Refroidissement.objects.none()
    embrayage = Embrayage.objects.none()
    cardan = Cardan.objects.none()
    roulement = Roulement.objects.none()


    # -----------------------------
    # TOTALS
    # -----------------------------
    total_boite = 0
    total_bte_auto = 0
    total_geometrie = 0
    total_abs = 0
    total_esp = 0
    total_aide_stationnement = 0
    total_ventilation = 0
    total_securite = 0
    total_fusibles = 0
    total_plans_cablage = 0
    total_demarreur = 0
    total_remplacement_boite = 0
    total_remplacement_bte_auto = 0
    total_int_bte_auto = 0
    total_access = 0
    total_echappement = 0
    total_batterie = 0
    total_clim = 0
    total_ref = 0
    total_embrayage = 0

    total_int_moteur = 0
    total_int_boite = 0
    total_turbo = 0

    total_cardan = 0
    total_arbre_transmission = 0
    total_boite_transfert = 0
    total_banc_puissance = 0
    total_accident = 0
    total_geometrie_course = 0
    total_vitrage = 0
    total_roulement = 0
    total_suspension = 0
    total_preparation_course = 0

    modeles = VoitureModele.objects.none()

    # -----------------------------
    # TENANT SCHEMA
    # -----------------------------
    if schema_name:

        with schema_context(schema_name):

            # ---------------- BOITE / CHASSIS ----------------
            # ---------------- BOITE / CHASSIS ----------------

            boite = ControleBoite.objects.filter(
                voiture_exemplaire=exemplaire
            )

            bte_auto = ControleBteVitesseAuto.objects.filter(
                voiture_exemplaire=exemplaire
            )

            geometrie = GeometrieVoiture.objects.filter(
                voiture_exemplaire=exemplaire
            )

            abs_qs = Abs.objects.filter(
                voiture_exemplaire=exemplaire
            )

            remplacement_boite = RemplacementBoite.objects.filter(
                voiture_exemplaire=exemplaire
            )

            remplacement_bte_auto = RemplacementBteAuto.objects.filter(
                voiture_exemplaire=exemplaire
            )

            courroie_access = CourroieAccessoires.objects.filter(
                voiture_exemplaire=exemplaire
            )

            echappement = Echappement.objects.filter(
                voiture_exemplaire=exemplaire
            )
            composants_ech_total = total_composants_echappement(exemplaire)

            batterie = Batterie.objects.filter(
                voiture_exemplaire=exemplaire
            )

            refroidissement = Refroidissement.objects.filter(
                voiture_exemplaire=exemplaire
            )

            climatisation = Climatisation.objects.filter(
                voiture_exemplaire=exemplaire
            )
            embrayage = Embrayage.objects.filter(
                voiture_exemplaire=exemplaire
            )
            cardan = Cardan.objects.filter(
                voiture_exemplaire=exemplaire
            )
            roulement = Roulement.objects.filter(
                voiture_exemplaire=exemplaire
            )
            allumage = Allumage.objects.filter(
                voiture_exemplaire=exemplaire
            )

            # ---------------- TOTALS ----------------

            total_boite = boite.count()
            total_bte_auto = bte_auto.count()
            total_geometrie = geometrie.count()
            total_abs = abs_qs.count()
            from maintenance.autres_interventions.esp.models import Esp
            total_esp = Esp.objects.filter(voiture_exemplaire=exemplaire).count()
            from maintenance.autres_interventions.aide_stationnement.models import AideStationnement
            total_aide_stationnement = AideStationnement.objects.filter(voiture_exemplaire=exemplaire).count()
            from maintenance.autres_interventions.ventilation.models import Ventilation
            total_ventilation = Ventilation.objects.filter(voiture_exemplaire=exemplaire).count()
            from maintenance.autres_interventions.securite.models import Securite
            total_securite = Securite.objects.filter(voiture_exemplaire=exemplaire).count()
            from maintenance.autres_interventions.fusibles.models import Fusibles
            total_fusibles = Fusibles.objects.filter(voiture_exemplaire=exemplaire).count()
            from maintenance.autres_interventions.plan_cablage.models import PlanCablage
            total_plans_cablage = PlanCablage.objects.filter(voiture_exemplaire=exemplaire).count()
            from maintenance.autres_interventions.demarreur.models import Demarreur
            total_demarreur = Demarreur.objects.filter(voiture_exemplaire=exemplaire).count()
            total_remplacement_boite = remplacement_boite.count()
            total_remplacement_bte_auto = remplacement_bte_auto.count()
            total_int_bte_auto = total_bte_auto + total_remplacement_bte_auto
            total_access = courroie_access.count()
            total_echappement = echappement.count() + composants_ech_total
            total_batterie = batterie.count()
            total_clim = climatisation.count()
            total_ref = refroidissement.count()
            total_turbo = turbo.count()
            total_embrayage = embrayage.count()
            total_allumage = allumage.count()
            total_cardan = cardan.count()
            from maintenance.autres_interventions.arbre_transmission.models import ArbreTransmission
            total_arbre_transmission = ArbreTransmission.objects.filter(voiture_exemplaire=exemplaire).count()
            from maintenance.autres_interventions.boite_transfert.models import BoiteTransfert
            from maintenance.autres_interventions.banc_puissance.models import BancPuissance
            total_banc_puissance = BancPuissance.objects.filter(voiture_exemplaire=exemplaire).count()
            from maintenance.autres_interventions.accident.models import RapportAccident
            total_accident = RapportAccident.objects.filter(voiture_exemplaire=exemplaire).count()
            total_boite_transfert = BoiteTransfert.objects.filter(voiture_exemplaire=exemplaire).count()
            from maintenance.autres_interventions.geometrie_course.models import GeometrieCourse
            total_geometrie_course = GeometrieCourse.objects.filter(voiture_exemplaire=exemplaire).count()
            from maintenance.autres_interventions.vitres.models import Vitrage
            total_vitrage = Vitrage.objects.filter(voiture_exemplaire=exemplaire).count()
            total_roulement = roulement.count()
            from maintenance.autres_interventions.suspension.composants import total_suspension as _total_suspension
            total_suspension = _total_suspension(exemplaire)
            from maintenance.autres_interventions.preparation_course.composants import total_preparation_course as _total_pc
            total_preparation_course = _total_pc(exemplaire)

            # ---------------- MOTEUR ----------------

            admission = Admission.objects.filter(
                voiture_exemplaire=exemplaire
            )

            alternateur = Alternateur.objects.filter(
                voiture_exemplaire=exemplaire
            )

            courroie = CourroieDistribution.objects.filter(
                voiture_exemplaire=exemplaire
            )

            chaine = ChaineDistribution.objects.filter(
                voiture_exemplaire=exemplaire
            )

            culasse = Culasse.objects.filter(
                voiture_exemplaire=exemplaire
            )

            bas_moteur = BasMoteur.objects.filter(
                voiture_exemplaire=exemplaire
            )

            electronique = ElectroniqueMoteur.objects.filter(
                voiture_exemplaire=exemplaire
            )

            lubrification = Lubrification.objects.filter(
                voiture_exemplaire=exemplaire
            )

            turbo = Turbo.objects.filter(
                voiture_exemplaire=exemplaire
            )

            remplacement_moteur = RemplacementMoteur.objects.filter(
                voiture_exemplaire=exemplaire
            )
          

            total_turbo = turbo.count()

            total_int_moteur = (
                    admission.count()
                    + alternateur.count()
                    + courroie.count()
                    + chaine.count()
                    + culasse.count()
                    + bas_moteur.count()
                    + MetrologieMoteur.objects.filter(voiture_exemplaire=exemplaire).count()
                    + CasseMoteur.objects.filter(voiture_exemplaire=exemplaire).count()
                    + total_bougies(exemplaire)
                    + electronique.count()
                    + lubrification.count()
                    + turbo.count()
                    + MontageTurbo.objects.filter(voiture_exemplaire=exemplaire).count()
                    + remplacement_moteur.count()
                    + allumage.count()
            )

            total_int_boite = (
                    total_boite
                    + total_remplacement_boite
                    + CasseBoite.objects.filter(voiture_exemplaire=exemplaire).count()
            )

            modeles = VoitureModele.objects.all()

            total_int_moteur = (
                admission.count()
                + alternateur.count()
                + courroie.count()
                + chaine.count()
                    + culasse.count()
                    + bas_moteur.count()
                    + MetrologieMoteur.objects.filter(voiture_exemplaire=exemplaire).count()
                    + CasseMoteur.objects.filter(voiture_exemplaire=exemplaire).count()
                    + total_bougies(exemplaire)
                + electronique.count()
                + lubrification.count()
                + turbo.count()
                + MontageTurbo.objects.filter(voiture_exemplaire=exemplaire).count()
                + remplacement_moteur.count()
                + allumage.count()
                + total_demarreur      # démarreur et courroie d'accessoires : dans les interventions moteur
                + total_access
            )

            total_int_boite = (
                total_boite
                + total_remplacement_boite
                + CasseBoite.objects.filter(voiture_exemplaire=exemplaire).count()
            )

            modeles = VoitureModele.objects.all()

    # -----------------------------
    # POST
    # -----------------------------
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
                description=description,
            )

            return redirect(
                "maintenance:list",
                modele_id=exemplaire.voiture_modele.id
            )

    # -----------------------------
    # CONTEXT
    # -----------------------------
    context = {
        "exemplaire": exemplaire,
        "types_maintenance": TYPES_MAINTENANCE,

        "total_boite": total_boite,
        "total_bte_auto": total_bte_auto,
        "total_geometrie": total_geometrie,
        "total_abs": total_abs,
        "total_esp": total_esp,
        "total_aide_stationnement": total_aide_stationnement,
        "total_ventilation": total_ventilation,
        "total_securite": total_securite,
        "total_fusibles": total_fusibles,
        "total_plans_cablage": total_plans_cablage,
        "total_demarreur": total_demarreur,
        "total_remplacement_boite": total_remplacement_boite,
        "total_remplacement_bte_auto": total_remplacement_bte_auto,
        "total_int_bte_auto": total_int_bte_auto,
        "total_access": total_access,
        "total_echappement": total_echappement,
        "total_batterie": total_batterie,
        "total_transmission": total_cardan + total_arbre_transmission + total_roulement,
        "total_adblue": sum(r["total"] for r in _rubriques_adblue(exemplaire)),
        "total_aide_conduite": total_abs + total_esp + total_aide_stationnement,
        "total_geometrie_groupe": total_geometrie + total_geometrie_course,
        "total_electricite": total_batterie + total_fusibles + total_plans_cablage,
        "total_clim": total_clim,

        "total_int_moteur": total_int_moteur,
        "total_int_boite": total_int_boite,
        "total_turbo": total_turbo,
        "total_ref": total_ref,
        "total_embrayage": total_embrayage,
        "total_allumage" : total_allumage,
        "total_cardan": total_cardan,
        "total_arbre_transmission": total_arbre_transmission,
        "total_boites": total_int_boite + total_int_bte_auto + total_boite_transfert,
        "total_banc_puissance": total_banc_puissance,
        "total_accident": total_accident,
        "total_geometrie_course": total_geometrie_course,
        "total_vitrage": total_vitrage,
        "total_roulement": total_roulement,
        "total_suspension": total_suspension,
        "total_preparation_course": total_preparation_course,



        "boite": boite,
        "bte_auto": bte_auto,
        "geometrie": geometrie,
        "abs_qs": abs_qs,
        "climatisation": climatisation,
        "refroidissement": refroidissement,

        "remplacement_boite": remplacement_boite,
        "echappement": echappement,
        "embrayage": embrayage,

        "turbo": turbo,
        "alternateur": alternateur,
        "courroie": courroie,
        "remplacement_moteur": remplacement_moteur,
        "admission": admission,
        "courroie_access": courroie_access,
        "allumage": allumage,
        "modeles": modeles,
    }

    return render(
        request,
        "autres_interventions/choisir_autre.html",
        context
    )




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
            "maintenances": maintenances,
            "is_mecanicien": request.user.role in [
                "mecanicien",
                "chef_mecanicien",
                "direction",
                "magasinier",
            ],
        }
    )





# ======================================================
# DASHBOARD BOÎTES (manuelle + automatique + transfert)
# ======================================================
@never_cache
@login_required
def dashboard_boites_view(request, exemplaire_id):
    from .boites_composants import boites_vehicule

    tenant = request.user.societe
    exemplaire = get_object_or_404(
        VoitureExemplaire.objects.filter(
            Q(client__societe=tenant) | Q(client__isnull=True, societe=tenant)
        ),
        id=exemplaire_id,
    )
    boites = boites_vehicule(exemplaire)
    return render(request, "autres_interventions/dashboard_boites.html", {
        "exemplaire": exemplaire,
        "boites": boites,
        "total_boites": sum(b["total"] for b in boites),
    })



# ------------------------------------------------------------------
# Électricité : câblage, batterie, boîtes à fusibles
# ------------------------------------------------------------------
@never_cache
@login_required
def dashboard_electricite_view(request, exemplaire_id):
    from django.urls import reverse
    from django.utils.translation import gettext as _
    from maintenance.autres_interventions.fusibles.models import Fusibles
    from maintenance.autres_interventions.plan_cablage.models import PlanCablage

    tenant = request.user.societe
    exemplaire = get_object_or_404(
        VoitureExemplaire.objects.filter(
            Q(client__societe=tenant) | Q(client__isnull=True, societe=tenant)
        ),
        id=exemplaire_id,
    )
    rubriques = [
        {"label": _("Câblage"), "detail": _("Origine · Custom · Boîtier, connecteurs, fils"),
         "url": reverse("plan_cablage:plan_liste", args=[exemplaire.id]), "icone": "icons/em_faisceau.png",
         "total": PlanCablage.objects.filter(voiture_exemplaire=exemplaire).count()},
        {"label": _("Batterie"), "detail": "",
         "url": reverse("batterie:batterie_list", kwargs={"exemplaire_id": exemplaire.id}), "icone": "icons/batterie.png",
         "total": Batterie.objects.filter(voiture_exemplaire=exemplaire).count()},
        {"label": _("Boîtes à fusibles"), "detail": "",
         "url": reverse("fusibles:fusibles_list", args=[exemplaire.id]), "icone": "icons/fusibles.png",
         "total": Fusibles.objects.filter(voiture_exemplaire=exemplaire).count()},
    ]
    return render(request, "autres_interventions/dashboard_groupe.html", {
        "exemplaire": exemplaire,
        "rubriques": rubriques,
        "titre": _("Électricité"),
        "icone": "icons/electricite.png",
    })



# ------------------------------------------------------------------
# Géométrie : géométrie et géométrie course
# ------------------------------------------------------------------
@never_cache
@login_required
def dashboard_geometrie_view(request, exemplaire_id):
    from django.urls import reverse
    from django.utils.translation import gettext as _
    from maintenance.autres_interventions.geometrie_course.models import GeometrieCourse

    tenant = request.user.societe
    exemplaire = get_object_or_404(
        VoitureExemplaire.objects.filter(
            Q(client__societe=tenant) | Q(client__isnull=True, societe=tenant)
        ),
        id=exemplaire_id,
    )
    rubriques = [
        {"label": _("Géométrie"), "detail": "",
         "url": reverse("geometrie:geometrie_list", kwargs={"exemplaire_id": exemplaire.id}),
         "icone": "icons/geometrie-laser.png",
         "total": GeometrieVoiture.objects.filter(voiture_exemplaire=exemplaire).count()},
        {"label": _("Géométrie course"), "detail": "",
         "url": reverse("geometrie_course:geocourse_list", kwargs={"exemplaire_id": exemplaire.id}),
         "icone": "icons/geometrie-course.png",
         "total": GeometrieCourse.objects.filter(voiture_exemplaire=exemplaire).count()},
    ]
    return render(request, "autres_interventions/dashboard_groupe.html", {
        "exemplaire": exemplaire,
        "rubriques": rubriques,
        "titre": _("Géométrie"),
        "icone": "icons/geometrie-laser.png",
    })



# ------------------------------------------------------------------
# Aide à la conduite : ABS, ESP, aide au stationnement
# ------------------------------------------------------------------
@never_cache
@login_required
def dashboard_aide_conduite_view(request, exemplaire_id):
    from django.urls import reverse
    from django.utils.translation import gettext as _
    from maintenance.autres_interventions.aide_stationnement.models import AideStationnement
    from maintenance.autres_interventions.esp.models import Esp

    tenant = request.user.societe
    exemplaire = get_object_or_404(
        VoitureExemplaire.objects.filter(
            Q(client__societe=tenant) | Q(client__isnull=True, societe=tenant)
        ),
        id=exemplaire_id,
    )
    rubriques = [
        {"label": _("Système ABS"), "detail": "",
         "url": reverse("abs:abs_list", kwargs={"exemplaire_id": exemplaire.id}), "icone": "icons/abs.png",
         "total": Abs.objects.filter(voiture_exemplaire=exemplaire).count()},
        {"label": _("ESP"), "detail": "",
         "url": reverse("esp:esp_list", args=[exemplaire.id]), "icone": "icons/esp.png",
         "total": Esp.objects.filter(voiture_exemplaire=exemplaire).count()},
        {"label": _("Aide au stationnement"), "detail": _("Capteurs avant / arrière, caméra de recul, Park Assist"),
         "url": reverse("aide_stationnement:aide_stationnement_list", args=[exemplaire.id]),
         "icone": "icons/aide_stationnement.png",
         "total": AideStationnement.objects.filter(voiture_exemplaire=exemplaire).count()},
    ]
    return render(request, "autres_interventions/dashboard_groupe.html", {
        "exemplaire": exemplaire,
        "rubriques": rubriques,
        "titre": _("Aide à la conduite"),
        "icone": "icons/esp.png",
    })



# ------------------------------------------------------------------
# Transmission : arbre de transmission, cardans et roulements de roue
# ------------------------------------------------------------------
@never_cache
@login_required
def dashboard_transmission_view(request, exemplaire_id):
    from django.urls import reverse
    from django.utils.translation import gettext as _
    from maintenance.autres_interventions.arbre_transmission.models import ArbreTransmission

    tenant = request.user.societe
    exemplaire = get_object_or_404(
        VoitureExemplaire.objects.filter(
            Q(client__societe=tenant) | Q(client__isnull=True, societe=tenant)
        ),
        id=exemplaire_id,
    )
    rubriques = [
        {"label": _("Arbre de transmission"), "detail": "",
         "url": reverse("arbre_transmission:arbre_list", kwargs={"exemplaire_id": exemplaire.id}),
         "icone": "icons/arbre-transmission.png",
         "total": ArbreTransmission.objects.filter(voiture_exemplaire=exemplaire).count()},
        {"label": _("Contrôle des cardans"), "detail": "",
         "url": reverse("cardan:cardan_list", kwargs={"exemplaire_id": exemplaire.id}),
         "icone": "icons/cardan.png",
         "total": Cardan.objects.filter(voiture_exemplaire=exemplaire).count()},
        {"label": _("Roulements de roue"), "detail": "",
         "url": reverse("roulement:roulement_list", kwargs={"exemplaire_id": exemplaire.id}),
         "icone": "icons/roulement-roue-moyeu.png",
         "total": Roulement.objects.filter(voiture_exemplaire=exemplaire).count()},
    ]
    return render(request, "autres_interventions/dashboard_groupe.html", {
        "exemplaire": exemplaire,
        "rubriques": rubriques,
        "titre": _("Transmission"),
        "icone": "icons/arbre-transmission.png",
    })


# ======================================================
# ADBLUE / SCR : injecteur, réservoir, pompe, ajout, tuyaux, diagnostic, pot DeNOx
# ======================================================
def _rubriques_adblue(exemplaire):
    from django.urls import reverse
    from django.utils.translation import gettext as _
    from maintenance.autres_interventions.echappement.injecteur_adblue.models import InjecteurAdblue
    from maintenance.autres_interventions.echappement.pot_denox.models import PotDenox
    from maintenance.autres_interventions.systeme_adblue.reservoir_adblue.models import ReservoirAdblue
    from maintenance.autres_interventions.systeme_adblue.pompe_adblue.models import PompeAdblue
    from maintenance.autres_interventions.systeme_adblue.tuyaux_adblue.models import TuyauxAdblue
    from maintenance.autres_interventions.systeme_adblue.ajout_adblue.models import AjoutAdblue
    from maintenance.autres_interventions.systeme_adblue.diagnostic_adblue.models import DiagnosticAdblue

    elements = [
        (_("Injecteur AdBlue"), "injecteur_adblue", InjecteurAdblue, "icons/ech_injecteur_adblue.png"),
        (_("Réservoir AdBlue"), "reservoir_adblue", ReservoirAdblue, "icons/fmh_reservoir.png"),
        (_("Pompe AdBlue"), "pompe_adblue", PompeAdblue, "icons/pompe.png"),
        (_("Ajout d'AdBlue"), "ajout_adblue", AjoutAdblue, "icons/adblue.png"),
        (_("Tuyaux AdBlue"), "tuyaux_adblue", TuyauxAdblue, "icons/tuyau-flexible.png"),
        (_("Diagnostic AdBlue"), "diagnostic_adblue", DiagnosticAdblue, "icons/diagnostic.png"),
        (_("Pot DeNOx (SCR)"), "pot_denox", PotDenox, "icons/ech_pot_denox.png"),
    ]
    return [
        {"label": label, "detail": "",
         "url": reverse(f"{code}:{code}_list", kwargs={"exemplaire_id": exemplaire.id}),
         "icone": icone,
         "total": modele.objects.filter(voiture_exemplaire=exemplaire).count()}
        for label, code, modele, icone in elements
    ]


@login_required
@never_cache
def dashboard_adblue_view(request, exemplaire_id):
    from django.utils.translation import gettext as _

    tenant = request.user.societe
    exemplaire = get_object_or_404(
        VoitureExemplaire.objects.filter(
            Q(client__societe=tenant) | Q(client__isnull=True, societe=tenant)
        ),
        id=exemplaire_id,
    )
    return render(request, "autres_interventions/dashboard_groupe.html", {
        "exemplaire": exemplaire,
        "rubriques": _rubriques_adblue(exemplaire),
        "titre": _("AdBlue"),
        "icone": "icons/adblue.png",
    })
