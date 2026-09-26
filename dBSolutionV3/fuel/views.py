from django.core.exceptions import ValidationError

from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from django.utils.translation import gettext_lazy as _, gettext_noop
from django.views.decorators.http import require_GET
from django_tenants.utils import tenant_context
from utilisateurs.models import UserLog
from .forms import FuelForm
from voiture.voiture_marque.models import VoitureMarque
from voiture.voiture_modele.models import VoitureModele
from django.db.models.functions import TruncYear
from django.shortcuts import get_object_or_404
from voiture.voiture_exemplaire.models import VoitureExemplaire
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import ListView
from collections import defaultdict
from decimal import Decimal
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg, Count, Max, Min, Sum, Q
from django.db.models.functions import ExtractYear, TruncMonth
from django.views.generic import TemplateView
from .models import Fuel







@method_decorator(login_required, name="dispatch")
@method_decorator(never_cache, name="dispatch")
class FuelListView(ListView):
    model = Fuel
    template_name = "fuel/fuel_list.html"
    context_object_name = "fuels"

    def get_queryset(self):
        societe = self.request.user.societe


        return (
            Fuel.objects
            .select_related(
                "utilisateur",
                "voiture_exemplaire",
                "voiture_exemplaire__voiture_modele",
                "voiture_exemplaire__voiture_modele__voiture_marque",
            )
            .filter(societe=societe)
            .order_by("-date")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        societe = self.request.user.societe
        pays_labels = dict(Fuel.PAYS_CHOICES)

        totaux_par_pays = (
            Fuel.objects
            .filter(
                societe=societe,
                montant_tva__gt=0,
            )
            .values("pays")
            .annotate(
                total_tva=Sum("montant_tva")
            )
            .order_by("pays")
        )

        context["totaux_par_pays_affichage"] = [
            {
                "code": ligne["pays"],
                "nom": pays_labels.get(
                    ligne["pays"],
                    ligne["pays"],
                ),
                "tva": ligne["total_tva"],
            }
            for ligne in totaux_par_pays
            if ligne["total_tva"] and ligne["total_tva"] > 0
        ]

        return context





@login_required
def ajouter_fuel_all(request, exemplaire_id=None):

    tenant = request.user.societe

    vehicules_societe = VoitureExemplaire.objects.filter(
        Q(client__societe=tenant) | Q(client__isnull=True, societe=tenant)
    )

    # Véhicule de l'URL : facultatif
    exemplaire = (
        get_object_or_404(vehicules_societe, id=exemplaire_id)
        if exemplaire_id
        else None
    )


    if request.method == "POST":

        data = request.POST.copy()

        # ==================================================
        # AUTO-DÉTECTION DU VÉHICULE PAR IMMATRICULATION
        # ==================================================
        immatriculation = (data.get("immatriculation") or "").strip()
        erreur_immat = None

        if immatriculation and not data.get("voiture_exemplaire"):
            try:
                voiture = vehicules_societe.get(immatriculation__iexact=immatriculation)
                data["voiture_exemplaire"] = str(voiture.id)

            except VoitureExemplaire.DoesNotExist:
                erreur_immat = _("Voiture introuvable.")

            except VoitureExemplaire.MultipleObjectsReturned:
                erreur_immat = _("Plusieurs véhicules possèdent cette immatriculation.")

        form = FuelForm(data)

        if erreur_immat:
            form.add_error("immatriculation", erreur_immat)

        if form.is_valid():
            try:
                with transaction.atomic():

                    # ==========================================
                    # VÉHICULE CONCERNÉ
                    # (celui du formulaire, sinon celui de l'URL)
                    # ==========================================
                    vehicule = form.cleaned_data.get("voiture_exemplaire") or exemplaire

                    if vehicule is None:
                        form.add_error("immatriculation", _("Veuillez indiquer une immatriculation."))
                        raise ValidationError("vehicule_manquant")

                    if not vehicules_societe.filter(pk=vehicule.pk).exists():
                        form.add_error("immatriculation", _("Véhicule non autorisé."))
                        raise ValidationError("vehicule_interdit")

                    # ==========================================
                    # VALEURS AVANT LE PLEIN
                    # ==========================================
                    ancien_chassis = vehicule.kilometres_chassis or 0
                    ancien_moteur = vehicule.kilometres_moteur or 0
                    ancien_boite = vehicule.kilometres_boite or 0
                    ancien_embrayage = vehicule.kilometres_embrayage or 0

                    km = form.cleaned_data.get("kilometrage_fuel")
                    variation = 0

                    if km is not None:
                        km = int(km)

                        if km < ancien_chassis:
                            form.add_error(
                                "kilometrage_fuel",
                                _("Le kilométrage ne peut pas être inférieur au kilométrage "
                                  "actuel du véhicule (%(km)s km).") % {"km": ancien_chassis},
                            )
                            raise ValidationError("km_inferieur")

                        variation = km - ancien_chassis

                        # ======================================
                        # MISE À JOUR DU VÉHICULE
                        # ======================================
                        vehicule.kilometres_rollback = ancien_chassis
                        vehicule.kilometres_moteur_rollback = ancien_moteur
                        vehicule.kilometres_boite_rollback = ancien_boite
                        vehicule.kilometres_embrayage_rollback = ancien_embrayage

                        vehicule.kilometres_chassis = km
                        vehicule.date_derniere_intervention = timezone.localtime(timezone.now()).date()

                        # Recalcule moteur / boîte / embrayage / variation
                        vehicule.update_kilometres()

                        vehicule.save(update_fields=[
                            "kilometres_chassis",
                            "date_derniere_intervention",
                            "kilometres_rollback",
                            "kilometres_moteur_rollback",
                            "kilometres_boite_rollback",
                            "kilometres_embrayage_rollback",
                            "kilometres_moteur",
                            "kilometres_boite",
                            "kilometres_embrayage",
                            "variation_kilometres",
                        ])

                    # ==========================================
                    # CARBURANT
                    # ==========================================
                    fuel = form.save(commit=False)

                    fuel.voiture_exemplaire = vehicule
                    fuel.utilisateur = request.user
                    fuel.societe = tenant
                    # Technicien (seulement si le modèle a ces champs)
                    if hasattr(fuel, "tech_technicien"):
                        fuel.tech_technicien = request.user
                    if hasattr(fuel, "tech_nom_technicien"):
                        fuel.tech_nom_technicien = f"{request.user.prenom} {request.user.nom}"
                    if hasattr(fuel, "tech_role_technicien"):
                        fuel.tech_role_technicien = request.user.role
                    if hasattr(fuel, "tech_societe"):
                        fuel.tech_societe = request.user.societe

                    fuel.kilometrage_fuel = km
                    fuel.kilometrage_variation = variation

                    # Kilométrages AVANT le plein
                    fuel.kilometres_chassis = ancien_chassis
                    fuel.kilometres_moteur = ancien_moteur
                    fuel.kilometres_boite = ancien_boite
                    fuel.kilometres_embrayage = ancien_embrayage

                    fuel.save()
                    form.save_m2m()

                    # ==========================================
                    # LOG
                    # ==========================================
                    ACTION_AJOUT_FUEL = gettext_noop("Ajout de carburant")

                    UserLog.objects.create(
                        utilisateur=request.user,
                        action=f"{ACTION_AJOUT_FUEL} - {vehicule.immatriculation}",
                    )

                messages.success(request, _("Carburant ajouté avec succès."))
                return redirect("fuel:fuel_list")

            except ValidationError:
                # L'erreur est déjà attachée au champ concerné
                pass

            except Exception as e:
                messages.error(request, _("Erreur lors de l'enregistrement : %(erreur)s") % {"erreur": str(e)})

        messages.error(request, _("Veuillez corriger les erreurs ci-dessous."))


    else:

        initial = {}

        if exemplaire:
            initial = {

                "voiture_exemplaire": exemplaire.pk,

                "immatriculation": exemplaire.immatriculation,

            }

        form = FuelForm(initial=initial)

    return render(request, "fuel/fuel_form.html", {
        "form": form,
        "exemplaire": exemplaire,
    })



@never_cache
@login_required
def fuel_list(request):
    tenant = request.user.societe

    fuels = (
        Fuel.objects
        .filter(societe=tenant)
        .select_related(
            "utilisateur",
            "voiture_exemplaire",
            "voiture_exemplaire__voiture_modele",
            "voiture_exemplaire__voiture_modele__voiture_marque",
        )
        .order_by("-date")
    )

    return render(
        request,
        "fuel/fuel_list.html",
        {
            "fuels": fuels,
        },
    )


@login_required
def fuel_detail(request, fuel_id):
    tenant = request.user.societe

    fuel = get_object_or_404(
        Fuel.objects.select_related("voiture_exemplaire"),
        id=fuel_id,
        societe=tenant,
    )

    return render(
        request,
        "fuel/fuel_detail.html",
        {
            "fuel": fuel,
            "exemplaire": fuel.voiture_exemplaire,
        },
    )




@login_required
def modifier_fuel(request, fuel_id):

    tenant = request.user.societe

    fuel = get_object_or_404(
        Fuel.objects.select_related("voiture_exemplaire"),
        pk=fuel_id,
        societe=tenant,
    )

    vehicule = fuel.voiture_exemplaire

    # ==================================================
    # VALEURS ENREGISTRÉES (lues en base, avant le formulaire)
    # ==================================================
    original = Fuel.objects.get(pk=fuel.pk)

    if original.kilometres_rollback:
        avant_chassis = original.kilometres_rollback
        avant_moteur = original.kilometres_moteur_rollback or 0
        avant_boite = original.kilometres_boite_rollback or 0
        avant_embrayage = original.kilometres_embrayage_rollback or 0
    else:
        # Ancien plein : les champs contiennent les valeurs d'avant
        avant_chassis = original.kilometres_chassis or 0
        avant_moteur = original.kilometres_moteur or 0
        avant_boite = original.kilometres_boite or 0
        avant_embrayage = original.kilometres_embrayage or 0

    ancien_km_fuel = original.kilometrage_fuel

    # ==================================================
    # POST
    # ==================================================
    if request.method == "POST":

        form = FuelForm(request.POST, request.FILES, instance=fuel)

        if form.is_valid():
            try:
                with transaction.atomic():

                    km = form.cleaned_data.get("kilometrage_fuel")
                    km = int(km) if km is not None else ancien_km_fuel

                    # Ce plein est-il la dernière intervention sur le véhicule ?
                    est_dernier = (
                        vehicule is not None
                        and ancien_km_fuel is not None
                        and (vehicule.kilometres_chassis or 0) == ancien_km_fuel
                    )

                    if km is not None:

                        if km < avant_chassis:
                            form.add_error(
                                "kilometrage_fuel",
                                _("Le kilométrage ne peut pas être inférieur à %(km)s km.")
                                % {"km": avant_chassis},
                            )
                            raise ValidationError("km_inferieur")

                        if km != ancien_km_fuel and not est_dernier:
                            form.add_error(
                                "kilometrage_fuel",
                                _("Une intervention a été enregistrée après ce plein : "
                                  "son kilométrage ne peut plus être modifié."),
                            )
                            raise ValidationError("pas_dernier")

                    variation = (km - avant_chassis) if km is not None else 0

                    # ==========================================
                    # PLEIN
                    # ==========================================
                    fuel = form.save(commit=False)

                    fuel.voiture_exemplaire = vehicule  # le véhicule ne change pas
                    fuel.societe = tenant
                    fuel.utilisateur = request.user

                    fuel.kilometrage_fuel = km
                    fuel.kilometrage_variation = variation

                    # Kilométrages AVANT le plein (jamais modifiés)
                    fuel.kilometres_chassis = avant_chassis
                    fuel.kilometres_moteur = avant_moteur
                    fuel.kilometres_boite = avant_boite
                    fuel.kilometres_embrayage = avant_embrayage

                    # Sauvegardes (remplies aussi pour les anciens pleins)
                    fuel.kilometres_rollback = avant_chassis
                    fuel.kilometres_moteur_rollback = avant_moteur
                    fuel.kilometres_boite_rollback = avant_boite
                    fuel.kilometres_embrayage_rollback = avant_embrayage

                    fuel.save()
                    form.save_m2m()

                    # ==========================================
                    # VÉHICULE (seulement si dernier plein
                    # et kilométrage modifié)
                    # ==========================================
                    if est_dernier and km is not None and km != ancien_km_fuel:
                        VoitureExemplaire.objects.filter(pk=vehicule.pk).update(
                            kilometres_chassis=km,
                            kilometres_moteur=avant_moteur + variation,
                            kilometres_boite=avant_boite + variation,
                            kilometres_embrayage=avant_embrayage + variation,
                            kilometres_rollback=avant_chassis,
                            kilometres_moteur_rollback=avant_moteur,
                            kilometres_boite_rollback=avant_boite,
                            kilometres_embrayage_rollback=avant_embrayage,
                            variation_kilometres=variation,
                            date_derniere_intervention=timezone.localtime(timezone.now()).date(),
                        )

                    # ==========================================
                    # LOG
                    # ==========================================
                    ACTION_MODIFICATION_FUEL = gettext_noop("Modification d'un plein de carburant")

                    UserLog.objects.create(
                        utilisateur=request.user,
                        action=f"{ACTION_MODIFICATION_FUEL} - {vehicule.immatriculation if vehicule else '-'}",
                    )

                messages.success(request, _("Le plein de carburant a été mis à jour avec succès."))
                return redirect("fuel:fuel_detail", fuel_id=fuel.id)

            except ValidationError:
                pass  # l'erreur est déjà attachée au champ

            except Exception as e:
                messages.error(request, _("Erreur lors de la modification : %(erreur)s") % {"erreur": str(e)})

        messages.error(request, _("Le formulaire contient des erreurs."))

    else:
        form = FuelForm(instance=fuel)

    return render(request, "fuel/modifier_fuel.html", {
        "form": form,
        "fuel": fuel,
        "exemplaire": vehicule,
    })






def fuel_edit(request, pk):
    fuel = get_object_or_404(Fuel, pk=pk)
    if request.method == "POST":
        form = FuelForm(request.POST, instance=fuel)
        if form.is_valid():
            form.save()
            messages.success(request, _("Carburant modifié avec succès."))
            return redirect("fuel_list")
        else:
            messages.error(request, _("Veuillez corriger les erreurs ci-dessous."))
    else:
        form = FuelForm(instance=fuel)
    return render(request, "fuel/fuel_form.html", {"form": form, "title": _("Modifier un plein")})





@never_cache
@login_required
def fuel_delete(request, fuel_id):

    tenant = request.user.societe

    # ==========================================================
    # AUTORISATIONS
    # ==========================================================
    roles_autorises = ["direction", "chef_mecanicien"]

    if request.user.role not in roles_autorises and not request.user.is_superuser:
        messages.error(request, _("Accès refusé"))
        return redirect("utilisateurs:dashboard")

    # ==========================================================
    # RÉCUPÉRATION DU PLEIN
    # ==========================================================
    fuel = get_object_or_404(
        Fuel.objects.select_related("voiture_exemplaire"),
        id=fuel_id,
        societe=tenant,
    )

    exemplaire = fuel.voiture_exemplaire

    # ==========================================================
    # SÉCURITÉ TENANT (véhicule société ou véhicule client)
    # ==========================================================
    if exemplaire and not (
        (exemplaire.client and exemplaire.client.societe == tenant)
        or (exemplaire.client is None and exemplaire.societe == tenant)
    ):
        messages.error(request, _("Accès refusé"))
        return redirect("utilisateurs:dashboard")

    # ==========================================================
    # SUPPRESSION
    # ==========================================================
    if request.method == "POST":

        try:
            with transaction.atomic():

                immatriculation = exemplaire.immatriculation if exemplaire else "-"

                if exemplaire and fuel.kilometrage_fuel is not None:

                    # ------------------------------------------
                    # Valeurs AVANT le plein
                    # ------------------------------------------
                    if fuel.kilometres_rollback:
                        km_chassis = fuel.kilometres_rollback
                        km_moteur = fuel.kilometres_moteur_rollback or 0
                        km_boite = fuel.kilometres_boite_rollback or 0
                        km_embrayage = fuel.kilometres_embrayage_rollback or 0
                    else:
                        km_chassis = fuel.kilometres_chassis or 0
                        km_moteur = fuel.kilometres_moteur or 0
                        km_boite = fuel.kilometres_boite or 0
                        km_embrayage = fuel.kilometres_embrayage or 0

                    # ------------------------------------------
                    # Ce plein est-il la dernière intervention ?
                    # ------------------------------------------
                    est_dernier = (exemplaire.kilometres_chassis or 0) == fuel.kilometrage_fuel

                    if est_dernier:
                        VoitureExemplaire.objects.filter(pk=exemplaire.pk).update(
                            kilometres_chassis=km_chassis,
                            kilometres_moteur=km_moteur,
                            kilometres_boite=km_boite,
                            kilometres_embrayage=km_embrayage,
                            variation_kilometres=0,
                        )

                    # Sinon : une intervention plus récente a fixé
                    # le kilométrage → on ne touche pas au véhicule

                fuel.delete()

                ACTION_SUPPRESSION_FUEL = gettext_noop("Suppression d'un plein de carburant")

                UserLog.objects.create(
                    utilisateur=request.user,
                    action=f"{ACTION_SUPPRESSION_FUEL} - {immatriculation}",
                )

            messages.success(request, _("Carburant supprimé avec succès."))
            return redirect("fuel:fuel_list")

        except Exception as e:
            messages.error(
                request,
                _("Erreur lors de la suppression : %(erreur)s") % {"erreur": str(e)}
            )

    # ==========================================================
    # PAGE DE CONFIRMATION
    # ==========================================================
    return render(request, "fuel/fuel_delete.html", {
        "fuel": fuel,
        "exemplaire": exemplaire,
    })






@login_required
def check_immatriculation(request):
    tenant = request.user.societe
    immatriculation = request.GET.get("immatriculation", "").strip()

    if not immatriculation:
        return JsonResponse(
            {
                "error": True,
                "message": "Immatriculation manquante.",
            },
            status=400,
        )

    with tenant_context(tenant):
        voiture = (
            VoitureExemplaire.objects
            .select_related(
                "voiture_marque",
                "voiture_modele",
            )
            .filter(
                immatriculation__iexact=immatriculation,
            )
            .first()
        )

        if voiture is None:
            return JsonResponse(
                {
                    "error": True,
                    "message": "Véhicule introuvable.",
                },
                status=404,
            )

        marque = ""
        modele = ""
        volume_max = 0
        kilometres_chassis = 0

        if voiture.voiture_marque:
            marque = voiture.voiture_marque.nom_marque or ""

        if voiture.voiture_modele:
            modele = voiture.voiture_modele.nom_modele or ""

            # Adapte ce champ au nom réel présent dans VoitureModele
            volume_max = (
                getattr(voiture.voiture_modele, "taille_reservoir", None)
                or 0
            )

        # Adapte selon le nom exact de ton champ
        kilometres_chassis = (
            getattr(voiture, "kilometres_chassis", None)
            or 0
        )

        return JsonResponse(
            {
                "error": False,
                "id": str(voiture.pk),
                "immatriculation": voiture.immatriculation or "",
                "marque": marque,
                "modele": modele,
                "kilometres_chassis": kilometres_chassis,
                "volume_max": volume_max,
            }
        )




@require_GET
def get_marques(request):
    query = request.GET.get("q", "").strip()

    if not query:
        return JsonResponse([], safe=False)

    marques = (
        VoitureMarque.objects
        .filter(nom_marque__icontains=query)
        .values_list("nom_marque", flat=True)
        .distinct()[:10]
    )

    return JsonResponse(list(marques), safe=False)


@require_GET
def get_modeles(request):
    query = request.GET.get("q", "").strip()

    if not query:
        return JsonResponse([], safe=False)

    modeles = (
        VoitureModele.objects
        .filter(nom_modele__icontains=query)
        .values_list("nom_modele", flat=True)
        .distinct()[:10]
    )

    return JsonResponse(list(modeles), safe=False)











class FuelStatView(LoginRequiredMixin, TemplateView):
    template_name = "fuel/fuel_stat.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        societe = self.request.user.societe

        fuels = (
            Fuel.objects
            .filter(societe=societe)
            .select_related(
                "voiture_exemplaire",
                "voiture_exemplaire__voiture_modele",
                "voiture_exemplaire__voiture_modele__voiture_marque",
            )
        )

        # ==========================================================
        # GLOBAL
        # ==========================================================
        agregats_globaux = fuels.aggregate(
            total_litres=Sum("litres"),
            total_cout=Sum("prix_refuelling"),
            total_tva=Sum("montant_tva"),
            prix_moyen_litre=Avg("prix_litre"),
            total_pleins=Count("id"),
        )

        context["global"] = {
            "total_litres": (
                agregats_globaux["total_litres"]
                or Decimal("0.0")
            ),
            "total_cout": (
                agregats_globaux["total_cout"]
                or Decimal("0.0")
            ),
            "total_tva": (
                agregats_globaux["total_tva"]
                or Decimal("0.0")
            ),
            "prix_moyen_litre": (
                agregats_globaux["prix_moyen_litre"]
                or Decimal("0.0")
            ),
            "total_pleins": (
                agregats_globaux["total_pleins"]
                or 0
            ),
        }

        # ==========================================================
        # TVA PAR PAYS
        # ==========================================================
        pays_labels = dict(Fuel.PAYS_CHOICES)

        totaux_par_pays_qs = (
            fuels
            .exclude(pays__isnull=True)
            .exclude(pays="")
            .values("pays")
            .annotate(total_tva=Sum("montant_tva"))
            .order_by("pays")
        )

        totaux_par_pays_affichage = []

        for ligne in totaux_par_pays_qs:
            code_pays = ligne["pays"]
            montant_tva = (
                ligne["total_tva"]
                or Decimal("0.0")
            )

            if montant_tva > 0:
                totaux_par_pays_affichage.append(
                    {
                        "code": code_pays,
                        "nom": pays_labels.get(
                            code_pays,
                            code_pays,
                        ),
                        "tva": montant_tva,
                    }
                )

        context["totaux_par_pays_affichage"] = (
            totaux_par_pays_affichage
        )

        # Conservation éventuelle de l'ancien dictionnaire.
        context["totaux_par_pays"] = {
            pays["code"]: pays["tva"]
            for pays in totaux_par_pays_affichage
        }

        context["total_global"] = (
            agregats_globaux["total_tva"]
            or Decimal("0.0")
        )

        # ==========================================================
        # PAR VOITURE
        # ==========================================================
        context["par_voiture"] = (
            fuels
            .values(
                "voiture_exemplaire__id",
                "voiture_exemplaire__immatriculation",
                "voiture_exemplaire__pays",
                "voiture_exemplaire__voiture_modele__nom_modele",
                "voiture_exemplaire__voiture_modele__voiture_marque__nom_marque",
                "voiture_exemplaire__voiture_modele__nom_variante",
            )
            .annotate(
                total_litres=Sum("litres"),
                total_cout=Sum("prix_refuelling"),
                total_tva=Sum("montant_tva"),
                prix_moyen_litre=Avg("prix_litre"),
                nb_pleins=Count("id"),
            )
            .order_by("-total_cout")
        )

        # ==========================================================
        # PAR MOIS
        # ==========================================================
        context["par_mois"] = (
            fuels
            .annotate(mois=TruncMonth("date"))
            .values("mois")
            .annotate(
                nb_pleins=Count("id"),
                total_litres=Sum("litres"),
                total_cout=Sum("prix_refuelling"),
                total_tva=Sum("montant_tva"),
                km_min=Min("kilometrage_fuel"),
                km_max=Max("kilometrage_fuel"),
            )
            .order_by("mois")
        )

        # ==========================================================
        # PAR ANNÉE
        # ==========================================================
        context["par_an"] = (
            fuels
            .annotate(an=ExtractYear("date"))
            .values("an")
            .annotate(
                nb_pleins=Count("id"),
                total_litres=Sum("litres"),
                total_cout=Sum("prix_refuelling"),
                total_tva=Sum("montant_tva"),
                km_min=Min("kilometrage_fuel"),
                km_max=Max("kilometrage_fuel"),
            )
            .order_by("an")
        )

        # ==========================================================
        # CONSOMMATION MOYENNE MULTI-VÉHICULES
        # ==========================================================
        total_litres_consommation = Decimal("0.0")
        total_km = Decimal("0.0")

        stats_mois = defaultdict(
            lambda: {
                "litres": Decimal("0.0"),
                "km": Decimal("0.0"),
            }
        )

        stats_an = defaultdict(
            lambda: {
                "litres": Decimal("0.0"),
                "km": Decimal("0.0"),
            }
        )

        vehicule_ids = (
            fuels
            .exclude(voiture_exemplaire_id__isnull=True)
            .values_list(
                "voiture_exemplaire_id",
                flat=True,
            )
            .distinct()
        )

        for vehicule_id in vehicule_ids:
            fuels_vehicule = (
                fuels
                .filter(
                    voiture_exemplaire_id=vehicule_id,
                )
                .order_by(
                    "date",
                    "kilometrage_fuel",
                )
            )

            ancien_km = None

            for fuel in fuels_vehicule:
                if fuel.kilometrage_fuel is None:
                    continue

                km_actuel = Decimal(
                    str(fuel.kilometrage_fuel)
                )

                litres = Decimal(
                    str(fuel.litres or 0)
                )

                if ancien_km is not None:
                    km_parcourus = (
                        km_actuel - ancien_km
                    )

                    if km_parcourus > 0:
                        total_litres_consommation += litres
                        total_km += km_parcourus

                        if fuel.date:
                            mois = fuel.date.replace(
                                day=1,
                                hour=0,
                                minute=0,
                                second=0,
                                microsecond=0,
                            )

                            annee = fuel.date.year

                            stats_mois[mois]["litres"] += litres
                            stats_mois[mois]["km"] += km_parcourus

                            stats_an[annee]["litres"] += litres
                            stats_an[annee]["km"] += km_parcourus

                ancien_km = km_actuel

        context["conso_moyenne"] = (
            total_litres_consommation
            * Decimal("100")
            / total_km
            if total_km > 0
            else Decimal("0.0")
        )

        context["conso_moyenne_mois"] = {
            mois: (
                data["litres"]
                * Decimal("100")
                / data["km"]
            )
            for mois, data in stats_mois.items()
            if data["km"] > 0
        }

        context["conso_moyenne_an"] = {
            annee: (
                data["litres"]
                * Decimal("100")
                / data["km"]
            )
            for annee, data in stats_an.items()
            if data["km"] > 0
        }

        return context










class FuelExemplaireStatView(LoginRequiredMixin, TemplateView):
    template_name = "fuel/fuel_exemplaire_stat.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        societe = self.request.user.societe
        exemplaire_id = self.kwargs.get("exemplaire_id")

        exemplaire = get_object_or_404(
            VoitureExemplaire,
            pk=exemplaire_id,
        )

        fuels = (
            Fuel.objects
            .filter(
                societe=societe,
                voiture_exemplaire=exemplaire,
            )
            .select_related(
                "voiture_exemplaire",
                "voiture_exemplaire__voiture_modele",
                "voiture_exemplaire__voiture_modele__voiture_marque",
            )
            .order_by("date", "kilometrage_fuel")
        )

        context["exemplaire"] = exemplaire

        # ==========================================================
        # CONSOMMATION GLOBALE
        # ==========================================================
        total_litres_consommation = Decimal("0.0")
        total_km = Decimal("0.0")
        kilometrage_precedent = None

        for fuel in fuels:
            kilometrage = fuel.kilometrage_fuel
            litres = fuel.litres or Decimal("0.0")

            if kilometrage is None:
                continue

            if kilometrage_precedent is not None:
                difference_km = kilometrage - kilometrage_precedent

                if difference_km > 0:
                    total_litres_consommation += litres
                    total_km += difference_km

            kilometrage_precedent = kilometrage

        kilometrages = fuels.aggregate(
            minimum=Min("kilometrage_fuel"),
            maximum=Max("kilometrage_fuel"),
        )

        km_min = Decimal(str(kilometrages["minimum"] or 0))
        km_max = Decimal(str(kilometrages["maximum"] or 0))
        km_total = km_max - km_min

        agregats_globaux = fuels.aggregate(
            total_litres=Sum("litres"),
            total_cout=Sum("prix_refuelling"),
            total_tva=Sum("montant_tva"),
            prix_moyen_litre=Avg("prix_litre"),
        )

        total_cout = Decimal(
            str(agregats_globaux["total_cout"] or 0)
        )

        conso_moyenne = (
            total_litres_consommation
            * Decimal("100")
            / total_km
            if total_km > 0
            else Decimal("0.0")
        )

        cout_km = (
            total_cout / km_total
            if km_total > 0
            else Decimal("0.0")
        )

        context["global"] = {
            "total_pleins": fuels.count(),
            "total_litres": agregats_globaux["total_litres"]
            or Decimal("0.0"),
            "total_cout": total_cout,
            "total_tva": agregats_globaux["total_tva"]
            or Decimal("0.0"),
            "prix_moyen_litre": agregats_globaux[
                "prix_moyen_litre"
            ]
            or Decimal("0.0"),
            "conso_moyenne": conso_moyenne,
            "cout_km": cout_km,
        }

        context["conso_moyenne"] = conso_moyenne

        # ==========================================================
        # TVA PAR PAYS
        # ==========================================================
        pays_labels = dict(Fuel.PAYS_CHOICES)

        totaux_par_pays_qs = (
            fuels
            .exclude(pays__isnull=True)
            .exclude(pays="")
            .values("pays")
            .annotate(total_tva=Sum("montant_tva"))
            .order_by("pays")
        )

        totaux_par_pays_affichage = []

        for ligne in totaux_par_pays_qs:
            code_pays = ligne["pays"]
            montant_tva = ligne["total_tva"] or Decimal("0.0")

            if montant_tva > 0:
                totaux_par_pays_affichage.append(
                    {
                        "code": code_pays,
                        "nom": pays_labels.get(
                            code_pays,
                            code_pays,
                        ),
                        "tva": montant_tva,
                    }
                )

        context["totaux_par_pays_affichage"] = (
            totaux_par_pays_affichage
        )

        context["total_global"] = (
            agregats_globaux["total_tva"]
            or Decimal("0.0")
        )

        # Facultatif si une autre partie du template utilise encore
        # l'ancien dictionnaire.
        context["totaux_par_pays"] = {
            pays["code"]: pays["tva"]
            for pays in totaux_par_pays_affichage
        }

        # ==========================================================
        # STATISTIQUES PAR MOIS
        # ==========================================================
        par_mois_qs = (
            fuels
            .annotate(mois=TruncMonth("date"))
            .values("mois")
            .annotate(
                total_litres=Sum("litres"),
                total_prix=Sum("prix_refuelling"),
                total_tva=Sum("montant_tva"),
                nb_pleins=Count("id"),
                km_min=Min("kilometrage_fuel"),
                km_max=Max("kilometrage_fuel"),
            )
            .order_by("mois")
        )

        par_mois = []
        conso_moyenne_mois = {}

        for mois_data in par_mois_qs:
            mois = mois_data["mois"]

            if mois is None:
                continue

            fuels_mois = fuels.filter(
                date__year=mois.year,
                date__month=mois.month,
            )

            total_litres_mois = Decimal("0.0")
            total_km_mois = Decimal("0.0")
            kilometrage_precedent = None

            for fuel in fuels_mois:
                kilometrage = fuel.kilometrage_fuel
                litres = fuel.litres or Decimal("0.0")

                if kilometrage is None:
                    continue

                if kilometrage_precedent is not None:
                    difference_km = (
                        kilometrage
                        - kilometrage_precedent
                    )

                    if difference_km > 0:
                        total_litres_mois += litres
                        total_km_mois += difference_km

                kilometrage_precedent = kilometrage

            consommation_mois = (
                total_litres_mois
                * Decimal("100")
                / total_km_mois
                if total_km_mois > 0
                else Decimal("0.0")
            )

            km_min_mois = Decimal(
                str(mois_data["km_min"] or 0)
            )

            km_max_mois = Decimal(
                str(mois_data["km_max"] or 0)
            )

            km_mois = km_max_mois - km_min_mois

            total_cout_mois = Decimal(
                str(mois_data["total_prix"] or 0)
            )

            cout_km_mois = (
                total_cout_mois / km_mois
                if km_mois > 0
                else Decimal("0.0")
            )

            par_mois.append(
                {
                    "mois": mois,
                    "nb_pleins": mois_data["nb_pleins"],
                    "total_litres": mois_data[
                        "total_litres"
                    ]
                    or Decimal("0.0"),
                    "total_cout": total_cout_mois,
                    "total_tva": mois_data["total_tva"]
                    or Decimal("0.0"),
                    "conso_moyenne": consommation_mois,
                    "cout_km": cout_km_mois,
                }
            )

            conso_moyenne_mois[mois] = consommation_mois

        context["par_mois"] = par_mois
        context["conso_moyenne_mois"] = (
            conso_moyenne_mois
        )

        # ==========================================================
        # STATISTIQUES PAR ANNÉE
        # ==========================================================
        par_an_qs = (
            fuels
            .annotate(an=TruncYear("date"))
            .values("an")
            .annotate(
                total_litres=Sum("litres"),
                total_prix=Sum("prix_refuelling"),
                total_tva=Sum("montant_tva"),
                nb_pleins=Count("id"),
                km_min=Min("kilometrage_fuel"),
                km_max=Max("kilometrage_fuel"),
            )
            .order_by("an")
        )

        par_an = []
        conso_moyenne_an = {}

        for an_data in par_an_qs:
            annee = an_data["an"]

            if annee is None:
                continue

            fuels_annee = fuels.filter(
                date__year=annee.year,
            )

            total_litres_annee = Decimal("0.0")
            total_km_annee = Decimal("0.0")
            kilometrage_precedent = None

            for fuel in fuels_annee:
                kilometrage = fuel.kilometrage_fuel
                litres = fuel.litres or Decimal("0.0")

                if kilometrage is None:
                    continue

                if kilometrage_precedent is not None:
                    difference_km = (
                        kilometrage
                        - kilometrage_precedent
                    )

                    if difference_km > 0:
                        total_litres_annee += litres
                        total_km_annee += difference_km

                kilometrage_precedent = kilometrage

            consommation_annee = (
                total_litres_annee
                * Decimal("100")
                / total_km_annee
                if total_km_annee > 0
                else Decimal("0.0")
            )

            par_an.append(
                {
                    "an": annee,
                    "nb_pleins": an_data["nb_pleins"],
                    "total_litres": an_data[
                        "total_litres"
                    ]
                    or Decimal("0.0"),
                    "total_cout": an_data["total_prix"]
                    or Decimal("0.0"),
                    "total_tva": an_data["total_tva"]
                    or Decimal("0.0"),
                    "conso_moyenne": consommation_annee,
                }
            )

            conso_moyenne_an[annee.year] = (
                consommation_annee
            )

        context["par_an"] = par_an
        context["conso_moyenne_an"] = (
            conso_moyenne_an
        )

        return context





@login_required
def autocomplete_immatriculation(request):

    terme = request.GET.get("term", "").strip()
    societe = request.user.societe

    if not terme:
        return JsonResponse([], safe=False)

    voitures = (
        VoitureExemplaire.objects
        .filter(
            societe=societe,
            immatriculation__icontains=terme,
        )
        .select_related(
            "voiture_modele",
            "voiture_modele__voiture_marque",
        )
        .order_by("immatriculation")[:20]
    )

    resultats = []

    for voiture in voitures:

        modele = voiture.voiture_modele
        marque = modele.voiture_marque if modele else None

        resultats.append({
            "id": voiture.pk,
            "immatriculation": voiture.immatriculation,
            "marque": marque.nom_marque if marque else "",
            "modele": modele.nom_modele if modele else "",
            "volume": modele.taille_reservoir if modele else "",
            "kilometres_chassis": voiture.kilometres_chassis or 0,
        })

    return JsonResponse(resultats, safe=False)