from decimal import Decimal

from django.http import JsonResponse, request
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_GET
from django.views.generic import ListView
from django_tenants.utils import tenant_context
from .forms import FuelForm
from .models import Fuel
from voiture.voiture_exemplaire.models import VoitureExemplaire
from voiture.voiture_marque.models import VoitureMarque
from voiture.voiture_modele.models import VoitureModele
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, Avg, Count, Case, When, Value, DecimalField
from django.db.models.functions import TruncMonth
from django.db.models.functions import TruncYear
from django.db.models import Min, Max, F, FloatField, ExpressionWrapper
from fuel.models import Fuel



@never_cache
@login_required
class FuelListView(ListView):
    model = Fuel
    template_name = "fuel/fuel_list.html"
    context_object_name = "fuels"   # ⚠️ important : pluriel
    paginate_by = 20
    ordering = ["-date"]

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
            .order_by("-date")
            .filter(societe=societe)
        )



@login_required
def ajouter_fuel_all(request):
    tenant = request.user.societe  # récupère le tenant de l'utilisateur

    with tenant_context(tenant):
        if request.method == "POST":
            form = FuelForm(request.POST)

            # --- Auto-remplissage de voiture_exemplaire via immatriculation si absent ---
            immatriculation = request.POST.get("immatriculation")
            if not request.POST.get("voiture_exemplaire") and immatriculation:
                try:
                    voiture = VoitureExemplaire.objects.get(immatriculation=immatriculation)
                    form.data = form.data.copy()
                    form.data["voiture_exemplaire"] = str(voiture.id)
                except VoitureExemplaire.DoesNotExist:
                    form.add_error("voiture_exemplaire", _("Voiture introuvable."))

            if form.is_valid():
                fuel = form.save(commit=False)


                fuel.utilisateur = request.user
                fuel.societe = request.user.societe

                fuel.save()
                messages.success(request, _("Carburant ajouté avec succès."))
            else:
                print(form.errors)  # utile pour debug
                messages.error(request, _("Veuillez corriger les erreurs ci-dessous."))
        else:
            form = FuelForm()

        type_carburant_choices = Fuel._meta.get_field("type_carburant").choices

        return render(
            request,
            "fuel/fuel_form.html",
            {
                "form": form,
                "fuel": form.instance,
                "type_carburant_choices": type_carburant_choices,
            },
        )



@never_cache
@login_required
def fuel_list(request):
    # On sélectionne les relations nécessaires pour éviter les requêtes supplémentaires
    tenant = request.user.societe

    with tenant_context(tenant):
        fuels = Fuel.objects.select_related(
            "utilisateur",
            "voiture_exemplaire",
            "voiture_exemplaire__voiture_modele",
            "voiture_exemplaire__voiture_modele__voiture_marque",
        ).order_by("-date").filter(societe=tenant)

        return render(request, "fuel/fuel_list.html", {
            "fuels": fuels
        })



@login_required
def fuel_detail(request, fuel_id):
    tenant = request.user.societe

    with tenant_context(tenant):
        fuel = get_object_or_404(Fuel, id=fuel_id)

    return render(
        request,
        "fuel/fuel_detail.html",
        {
            "fuel": fuel,
            "exemplaire" : fuel.voiture_exemplaire,
         },
    )


@login_required
def modifier_fuel(request, fuel_id):
    tenant = request.user.societe

    with tenant_context(tenant):
        fuel = get_object_or_404(Fuel, pk=fuel_id)

        if request.method == "POST":
            form = FuelForm(
                request.POST,
                request.FILES,
                instance=fuel  # ✅ utiliser l'objet complet
            )

            if form.is_valid():
                fuel = form.save()
                messages.success(request, _("Le plein de carburant a été mis à jour avec succès."))
            else:
                messages.error(request, _("Le formulaire contient des erreurs."))
                print(form.errors)  # utile pour debug

        else:
            form = FuelForm(instance=fuel)

    return render(
        request,
        "fuel/modifier_fuel.html",
        {
            "form": form,
            "fuel": fuel,
            "exemplaire": fuel.voiture_exemplaire,
        }
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





def fuel_delete(request, pk):
    fuel = get_object_or_404(Fuel, pk=pk)
    if request.method == "POST":
        fuel.delete()
        messages.success(request, _("Carburant supprimé avec succès."))
        return redirect("fuel_list")
    return render(request, "fuel/fuel_confirm_delete.html", {"fuel": fuel})









def check_immatriculation(request):
    immat = request.GET.get('immatriculation', '').strip()
    try:
        voiture = VoitureExemplaire.objects.get(immatriculation__iexact=immat)
        data = {
            'id': voiture.id,
            'marque': voiture.voiture_modele.voiture_marque.nom_marque,
            'modele': voiture.voiture_modele.nom_modele,
            'volume': voiture.voiture_modele.taille_reservoir,

        }
        return JsonResponse(data)
    except VoitureExemplaire.DoesNotExist:
        return JsonResponse({'error': 'not found'})






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





from decimal import Decimal
from django.db.models import Sum, Min, Max, Avg, Count
from django.db.models.functions import TruncMonth, TruncYear

class FuelStatView(LoginRequiredMixin, TemplateView):
    template_name = "fuel/fuel_stat.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tenant = self.request.user.societe

        with tenant_context(tenant):
            fuels = Fuel.objects.select_related(
                "voiture_exemplaire",
                "voiture_exemplaire__voiture_modele",
                "voiture_exemplaire__voiture_modele__voiture_marque",
            )

            # 🔹 Statistiques globales
            total_litres_global = Decimal('0')
            total_km_global = Decimal('0')

            voitures = fuels.values("voiture_exemplaire__id").annotate(
                km_min=Min("kilometrage_fuel"),
                km_max=Max("kilometrage_fuel"),
            )

            for v in voitures:
                km_min = v["km_min"] or 0
                km_max = v["km_max"] or 0
                km_total = km_max - km_min
                if km_total <= 0:
                    continue

                # litres N-1 : exclure le premier plein
                litres = fuels.filter(voiture_exemplaire__id=v["voiture_exemplaire__id"]) \
                              .exclude(kilometrage_fuel=km_min) \
                              .aggregate(total=Sum("litres"))["total"] or Decimal('0')

                total_litres_global += litres
                total_km_global += km_total

            conso_moyenne = (total_litres_global * 100 / total_km_global) if total_km_global > 0 else Decimal('0.0')
            context["conso_moyenne"] = conso_moyenne

            # 🔹 Statistiques globales additionnelles
            context["global"] = fuels.aggregate(
                total_litres=Sum("litres"),
                total_cout=Sum("prix_refuelling"),
                total_tva=Sum("montant_tva"),
                prix_moyen_litre=Avg("prix_litre"),
                total_pleins=Count("id"),
                km_min=Min("kilometrage_fuel"),
                km_max=Max("kilometrage_fuel"),
            )
            context["global"]["conso_moyenne"] = conso_moyenne

            # 🔹 Totaux TVA par pays
            PAYS_CHOICES = [('BE', "Belgique"), ('LU', "Luxembourg"), ('DE', "Allemagne")]
            context["totaux_par_pays"] = {
                code: fuels.filter(pays=code).aggregate(total=Sum("montant_tva"))["total"] or Decimal("0.0")
                for code, _ in PAYS_CHOICES
            }
            context["total_global"] = fuels.aggregate(total=Sum("montant_tva"))["total"] or Decimal("0.0")

            # 🔹 Stats par voiture
            par_voiture = (
                fuels.values(
                    "voiture_exemplaire__id",
                    "voiture_exemplaire__voiture_modele__nom_modele",
                    "voiture_exemplaire__voiture_modele__voiture_marque__nom_marque",
                    "voiture_exemplaire__voiture_modele__nom_variante",
                    "voiture_exemplaire__immatriculation",
                    "voiture_exemplaire__pays",
                )
                .annotate(
                    total_litres=Sum("litres"),
                    total_cout=Sum("prix_refuelling"),
                    prix_moyen_litre=Avg("prix_litre"),
                    nb_pleins=Count("id"),
                    km_min=Min("kilometrage_fuel"),
                    km_max=Max("kilometrage_fuel"),
                )
            )

            for v in par_voiture:
                km = (v["km_max"] or 0) - (v["km_min"] or 0)
                if km > 0:
                    # litres N-1 pour cette voiture
                    litres_n_1 = fuels.filter(voiture_exemplaire__id=v["voiture_exemplaire__id"]) \
                                      .exclude(kilometrage_fuel=v["km_min"]) \
                                      .aggregate(total=Sum("litres"))["total"] or Decimal("0.0")
                    v["conso_moyenne"] = (litres_n_1 * 100 / Decimal(km))
                    v["cout_km"] = (Decimal(v["total_cout"]) / Decimal(km))
                else:
                    v["conso_moyenne"] = Decimal("0.0")
                    v["cout_km"] = Decimal("0.0")

            context["par_voiture"] = par_voiture

            # 🔹 Stats par mois
            par_mois = fuels.annotate(mois=TruncMonth("date")).values("mois").order_by("mois")
            context["conso_moyenne_mois"] = {}
            for m in par_mois:
                fuels_mois = fuels.filter(date__month=m["mois"].month, date__year=m["mois"].year)
                voitures_mois = fuels_mois.values("voiture_exemplaire__id").annotate(
                    km_min=Min("kilometrage_fuel"),
                    km_max=Max("kilometrage_fuel"),
                )

                total_litres_mois = Decimal("0")
                total_km_mois = Decimal("0")
                for v in voitures_mois:
                    km_min = v["km_min"] or 0
                    km_max = v["km_max"] or 0
                    km_total = km_max - km_min
                    if km_total <= 0:
                        continue
                    litres = fuels_mois.filter(voiture_exemplaire__id=v["voiture_exemplaire__id"]) \
                                       .exclude(kilometrage_fuel=km_min) \
                                       .aggregate(total=Sum("litres"))["total"] or Decimal("0.0")
                    total_litres_mois += litres
                    total_km_mois += km_total

                context["conso_moyenne_mois"][m["mois"]] = (total_litres_mois * 100 / total_km_mois) if total_km_mois > 0 else Decimal("0.0")

            # 🔹 Stats par année
            par_an = fuels.annotate(an=TruncYear("date")).values("an").order_by("an")
            context["conso_moyenne_an"] = {}
            for a in par_an:
                fuels_an = fuels.filter(date__year=a["an"].year)
                voitures_an = fuels_an.values("voiture_exemplaire__id").annotate(
                    km_min=Min("kilometrage_fuel"),
                    km_max=Max("kilometrage_fuel"),
                )

                total_litres_an = Decimal("0")
                total_km_an = Decimal("0")
                for v in voitures_an:
                    km_min = v["km_min"] or 0
                    km_max = v["km_max"] or 0
                    km_total = km_max - km_min
                    if km_total <= 0:
                        continue
                    litres = fuels_an.filter(voiture_exemplaire__id=v["voiture_exemplaire__id"]) \
                                     .exclude(kilometrage_fuel=km_min) \
                                     .aggregate(total=Sum("litres"))["total"] or Decimal("0.0")
                    total_litres_an += litres
                    total_km_an += km_total

                context["conso_moyenne_an"][a["an"]] = (total_litres_an * 100 / total_km_an) if total_km_an > 0 else Decimal("0.0")

        return context




class FuelExemplaireStatView(LoginRequiredMixin, TemplateView):
    template_name = "fuel/fuel_exemplaire_stat.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        exemplaire_id = self.kwargs.get("exemplaire_id")

        tenant = self.request.user.societe
        with tenant_context(tenant):
            exemplaire = get_object_or_404(VoitureExemplaire, pk=exemplaire_id)
            fuels = Fuel.objects.filter(voiture_exemplaire=exemplaire).order_by("date")
            context["exemplaire"] = exemplaire

            # 🔹 Consommation globale en utilisant N-1 km
            total_litres = Decimal('0.0')
            total_km = Decimal('0.0')
            prev_km = None
            for f in fuels:
                if prev_km is not None:
                    km_diff = f.kilometrage_fuel - prev_km
                    if km_diff > 0:
                        total_litres += f.litres
                        total_km += km_diff
                prev_km = f.kilometrage_fuel

            conso_moyenne = (total_litres * Decimal('100') / total_km) if total_km > 0 else Decimal('0.0')

            context["global"] = {
                "total_pleins": fuels.count(),
                "total_litres": Fuel.total_litres_all_exemplaire(exemplaire) or Decimal('0.0'),
                "total_cout": Fuel.total_prix_all_exemplaire(exemplaire) or Decimal('0.0'),
                "total_tva": Fuel.total_tva_all_exemplaire(exemplaire) or Decimal('0.0'),
                "prix_moyen_litre": fuels.aggregate(avg=Avg("prix_litre"))["avg"] or Decimal('0.0'),
                "conso_moyenne": conso_moyenne,
            }
            context["conso_moyenne"] = conso_moyenne

            # 🔹 Totaux TVA par pays
            context["totaux_par_pays"] = Fuel.total_tva_par_pays_exemplaire(exemplaire)
            context["total_global"] = fuels.aggregate(total=Sum("montant_tva"))["total"] or Decimal('0.0')

            # 🔹 Stats par mois
            par_mois_qs = fuels.annotate(mois=TruncMonth("date")).values("mois").annotate(
                total_litres=Sum("litres"),
                total_prix=Sum("prix_refuelling"),
                total_tva=Sum("montant_tva"),
                nb_pleins=Count("id"),
                km_min=Min("kilometrage_fuel"),
                km_max=Max("kilometrage_fuel"),
            ).order_by("mois")

            par_mois = []
            conso_moyenne_mois = {}
            for m in par_mois_qs:
                fuels_mois = fuels.filter(date__month=m["mois"].month, date__year=m["mois"].year)
                total_litres_mois = Decimal('0.0')
                total_km_mois = Decimal('0.0')
                prev_km = None
                for f in fuels_mois:
                    if prev_km is not None:
                        km_diff = f.kilometrage_fuel - prev_km
                        if km_diff > 0:
                            total_litres_mois += f.litres
                            total_km_mois += km_diff
                    prev_km = f.kilometrage_fuel
                conso = (total_litres_mois * Decimal('100') / total_km_mois) if total_km_mois > 0 else Decimal('0.0')
                par_mois.append({
                    "mois": m["mois"],
                    "nb_pleins": m["nb_pleins"],
                    "total_litres": m["total_litres"] or Decimal('0.0'),
                    "total_cout": m["total_prix"] or Decimal('0.0'),
                    "total_tva": m["total_tva"] or Decimal('0.0'),
                    "conso_moyenne": conso,
                })
                conso_moyenne_mois[m["mois"]] = conso

            context["par_mois"] = par_mois
            context["conso_moyenne_mois"] = conso_moyenne_mois

            # 🔹 Stats par année (similaire)
            par_an_qs = fuels.annotate(an=TruncYear("date")).values("an").annotate(
                total_litres=Sum("litres"),
                total_prix=Sum("prix_refuelling"),
                total_tva=Sum("montant_tva"),
                nb_pleins=Count("id"),
                km_min=Min("kilometrage_fuel"),
                km_max=Max("kilometrage_fuel"),
            ).order_by("an")

            par_an = []
            conso_moyenne_an = {}
            for a in par_an_qs:
                fuels_an = fuels.filter(date__year=a["an"].year)
                total_litres_an = Decimal('0.0')
                total_km_an = Decimal('0.0')
                prev_km = None
                for f in fuels_an:
                    if prev_km is not None:
                        km_diff = f.kilometrage_fuel - prev_km
                        if km_diff > 0:
                            total_litres_an += f.litres
                            total_km_an += km_diff
                    prev_km = f.kilometrage_fuel
                conso = (total_litres_an * Decimal('100') / total_km_an) if total_km_an > 0 else Decimal('0.0')
                par_an.append({
                    "an": a["an"],
                    "nb_pleins": a["nb_pleins"],
                    "total_litres": a["total_litres"] or Decimal('0.0'),
                    "total_cout": a["total_prix"] or Decimal('0.0'),
                    "total_tva": a["total_tva"] or Decimal('0.0'),
                    "conso_moyenne": conso,
                })
                conso_moyenne_an[a["an"]] = conso

            context["par_an"] = par_an
            context["conso_moyenne_an"] = conso_moyenne_an

        return context