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
from django.db.models import Sum, Avg, Count, Case, When, Value
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

            # 📊 Statistiques globales
            global_stats = fuels.aggregate(
                total_litres=Sum("litres"),
                total_cout=Sum("prix_refuelling"),
                total_tva=Sum("montant_tva"),
                prix_moyen_litre=Avg("prix_litre"),
                total_pleins=Count("id"),
            )
            context["global"] = global_stats

            # 🔹 Totaux TVA par pays
            PAYS_CHOICES = [
                ('BE', "Belgique"),
                ('LU', "Luxembourg"),
                ('DE', "Allemagne"),
            ]
            totaux_par_pays = {}
            for code, _ in PAYS_CHOICES:
                totaux_par_pays[code] = fuels.filter(pays=code).aggregate(total=Sum("montant_tva"))["total"] or 0
            context["totaux_par_pays"] = totaux_par_pays

            # 🔹 Total TVA global
            total_global = fuels.aggregate(total=Sum("montant_tva"))["total"] or 0
            context["total_global"] = total_global

            # 🚗 Stats par voiture
            par_voiture = (
                fuels.values(
                    "voiture_exemplaire__id",
                    "voiture_exemplaire__voiture_modele__nom_modele",
                    "voiture_exemplaire__voiture_modele__voiture_marque__nom_marque",
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
                .annotate(
                    km_parcourus=F("km_max") - F("km_min"),
                )
                .annotate(
                    conso_moyenne=Case(
                        When(
                            km_parcourus__gt=0,
                            then=ExpressionWrapper(
                                F("total_litres") * 100.0 / F("km_parcourus"),
                                output_field=FloatField(),
                            ),
                        ),
                        default=Value(0.0),
                        output_field=FloatField(),
                    ),
                    cout_km=Case(
                        When(
                            km_parcourus__gt=0,
                            then=ExpressionWrapper(
                                F("total_cout") / F("km_parcourus"),
                                output_field=FloatField(),
                            ),
                        ),
                        default=Value(0.0),
                        output_field=FloatField(),
                    ),
                )
                .order_by("-total_cout")
            )
            context["par_voiture"] = par_voiture

            # 📅 Stats par mois
            par_mois = (
                fuels.annotate(mois=TruncMonth("date"))
                .values("mois")
                .annotate(
                    total_litres=Sum("litres"),
                    total_cout=Sum("prix_refuelling"),
                    nb_pleins=Count("id"),
                )
                .order_by("mois")
            )
            context["par_mois"] = par_mois

            # 📅 Stats par année
            par_an = (
                fuels.annotate(an=TruncYear("date"))
                .values("an")
                .annotate(
                    total_litres=Sum("litres"),
                    total_cout=Sum("prix_refuelling"),
                    nb_pleins=Count("id"),
                )
                .order_by("an")
            )
            context["par_an"] = par_an

            return context





class FuelExemplaireStatView(LoginRequiredMixin, TemplateView):
    template_name = "fuel/fuel_exemplaire_stat.html"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Récupère l'ID depuis l'URL
        exemplaire_id = self.kwargs.get("exemplaire_id")

        # Récupère l'exemplaire en tenant compte du tenant
        tenant = self.request.user.societe
        with tenant_context(tenant):
            exemplaire = get_object_or_404(VoitureExemplaire, pk=exemplaire_id)
            fuels = Fuel.objects.filter(voiture_exemplaire=exemplaire)

            # 🔹 Stats globales pour cet exemplaire
            context["global"] = {
                "total_pleins": fuels.count(),
                "total_litres": Fuel.total_litres_all_exemplaire(exemplaire),
                "total_cout": Fuel.total_prix_all_exemplaire(exemplaire),
                "total_tva": Fuel.total_tva_all_exemplaire(exemplaire),
                "prix_moyen_litre": fuels.aggregate(avg=Avg("prix_litre"))["avg"] or 0,
            }

            # 🔹 Totaux TVA par pays
            context["totaux_par_pays"] = Fuel.total_tva_par_pays_exemplaire(exemplaire)

            total_global = fuels.aggregate(total=Sum("montant_tva"))["total"] or 0
            context["total_global"] = total_global

            # 🔹 Stats par mois
            context["par_mois"] = [
                {
                    "mois": m["mois"],
                    "nb_pleins": m["nb_pleins"],
                    "total_litres": m["total_litres"],
                    "total_cout": m["total_prix"],
                    "total_tva": m["total_tva"],
                }
                for m in fuels.annotate(mois=TruncMonth("date"))
                                 .values("mois")
                                 .annotate(
                                    total_litres=Sum("litres"),
                                    total_prix=Sum("prix_refuelling"),
                                    total_tva=Sum("montant_tva"),
                                    nb_pleins=Count("id"),
                                 )
                                 .order_by("mois")
            ]

            # 🔹 Stats par année
            context["par_an"] = [
                {
                    "an": a["an"],
                    "nb_pleins": a["nb_pleins"],
                    "total_litres": a["total_litres"],
                    "total_cout": a["total_prix"],
                    "total_tva": a["total_tva"],
                }
                for a in fuels.annotate(an=TruncYear("date"))
                               .values("an")
                               .annotate(
                                   total_litres=Sum("litres"),
                                   total_prix=Sum("prix_refuelling"),
                                   total_tva=Sum("montant_tva"),
                                   nb_pleins=Count("id"),
                               )
                               .order_by("an")
            ]

            return context