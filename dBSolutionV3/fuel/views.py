from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_GET
from django_tenants.utils import tenant_context
from .forms import FuelForm
from voiture.voiture_marque.models import VoitureMarque
from voiture.voiture_modele.models import VoitureModele
from django.db.models.functions import TruncYear
from django.shortcuts import get_object_or_404
from voiture.voiture_exemplaire.models import VoitureExemplaire
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import ListView
from collections import defaultdict
from decimal import Decimal
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg, Count, Max, Min, Sum
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
def ajouter_fuel_all(request):
    tenant = request.user.societe



    if request.method == "POST":

        form = FuelForm(request.POST)

        # Auto-détection du véhicule avant validation
        immatriculation = request.POST.get("immatriculation")

        if immatriculation and not request.POST.get("voiture_exemplaire"):
            try:
                voiture = VoitureExemplaire.objects.get(
                    immatriculation__iexact=immatriculation.strip()
                )

                # Injection de l'identifiant du véhicule dans les données POST
                data = form.data.copy()
                data["voiture_exemplaire"] = str(voiture.id)

                form = FuelForm(data)

            except VoitureExemplaire.DoesNotExist:
                form.add_error(
                    "immatriculation",
                    _("Voiture introuvable."),
                )

            except VoitureExemplaire.MultipleObjectsReturned:
                form.add_error(
                    "immatriculation",
                    _("Plusieurs véhicules possèdent cette immatriculation."),
                )

        if form.is_valid():

            fuel = form.save(commit=False)

            fuel.utilisateur = request.user
            fuel.societe = tenant

            fuel.save()
            form.save_m2m()

            messages.success(
                request,
                _("Carburant ajouté avec succès."),
            )

            return redirect("fuel:fuel_list")

        messages.error(
            request,
            _("Veuillez corriger les erreurs ci-dessous."),
        )

    else:
        form = FuelForm()

    return render(
        request,
        "fuel/fuel_form.html",
        {
            "form": form,
        },
    )

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

    if request.method == "POST":
        form = FuelForm(
            request.POST,
            request.FILES,
            instance=fuel,
        )

        if form.is_valid():
            fuel = form.save(commit=False)
            fuel.societe = tenant
            fuel.utilisateur = request.user
            fuel.save()
            form.save_m2m()

            messages.success(
                request,
                _("Le plein de carburant a été mis à jour avec succès."),
            )

            return redirect(
                "fuel:fuel_detail",
                fuel_id=fuel.id,
            )

        messages.error(
            request,
            _("Le formulaire contient des erreurs."),
        )

    else:
        form = FuelForm(instance=fuel)

    return render(
        request,
        "fuel/modifier_fuel.html",
        {
            "form": form,
            "fuel": fuel,
            "exemplaire": fuel.voiture_exemplaire,
        },
    )



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




@login_required
def fuel_delete(request, fuel_id):

    if request.user.role not in ["direction", "chef_mecanicien"]:
        messages.error(
            request,
            _("Vous n'avez pas l'autorisation de supprimer ce plein.")
        )
        return redirect("fuel:fuel_list")

    fuel = get_object_or_404(Fuel, id=fuel_id)

    if request.method == "POST":
        fuel.delete()
        messages.success(request, _("Carburant supprimé avec succès."))



    return render(request, "fuel/fuel_delete.html", {"fuel": fuel})








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