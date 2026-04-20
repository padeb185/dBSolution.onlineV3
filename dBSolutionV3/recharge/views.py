
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, FloatField, Value, ExpressionWrapper, F, When, Case, Max, Min, Avg
from django.db.models.functions import TruncYear, TruncMonth, Coalesce
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_GET
from django.views.generic import ListView, TemplateView
from django.utils.translation import gettext_lazy as _
from django_tenants.utils import tenant_context
from guardian.mixins import LoginRequiredMixin
from recharge.models import Electricite
from recharge.forms import ElectriciteForm
from voiture.voiture_exemplaire.models import VoitureExemplaire
from voiture.voiture_marque.models import VoitureMarque
from voiture.voiture_modele.models import VoitureModele
from decimal import Decimal





@method_decorator([login_required, never_cache], name="dispatch")
class ElectriciteListView(ListView):
    model = Electricite
    template_name = "recharge/recharge_list.html"
    context_object_name = "recharges"
    paginate_by = 20
    ordering = ["-date"]

    def get_queryset(self):
        societe = self.request.user.societe

        return (
            Electricite.objects
            .select_related(
                "utilisateur",
                "voiture_exemplaire",
                "voiture_exemplaire__voiture_modele",
                "voiture_exemplaire__voiture_modele__voiture_marque",
            )
            .filter(societe=societe)
            .order_by("-date_recharge")
        )


@login_required
def ajouter_recharge_all(request):
    tenant = request.user.societe

    with tenant_context(tenant):

        if request.method == "POST":

            form = ElectriciteForm(request.POST)

            # 🔎 Auto-détection du véhicule via immatriculation
            immatriculation = request.POST.get("immatriculation")

            if not request.POST.get("voiture_exemplaire") and immatriculation:

                try:
                    voiture = VoitureExemplaire.objects.get(
                        immatriculation__iexact=immatriculation
                    )

                    form.data = form.data.copy()
                    form.data["voiture_exemplaire"] = str(voiture.id)

                except VoitureExemplaire.DoesNotExist:
                    form.add_error("voiture_exemplaire", _("Voiture introuvable."))

            if form.is_valid():

                recharge = form.save(commit=False)

                recharge.utilisateur = request.user
                recharge.societe = request.user.societe

                # ⚡ récupération automatique capacité batterie
                if recharge.voiture_exemplaire:
                    recharge.volume_max = (
                        recharge.voiture_exemplaire.voiture_modele.capacite_batterie
                    )
                else:
                    form.add_error(
                        "voiture_exemplaire",
                        _("Véhicule obligatoire."),
                    )

                    return render(
                        request,
                        "recharge/electricite_form.html",
                        {"form": form},
                    )

                recharge.save()

                messages.success(
                    request,
                    _("Recharge ajoutée avec succès.")
                )

            else:

                print(form.errors)
                messages.error(
                    request,
                    _("Veuillez corriger les erreurs ci-dessous.")
                )

        else:

            form = ElectriciteForm()

        type_carburant_choices = (
            Electricite._meta.get_field("type_carburant").choices
        )

        return render(
            request,
            "recharge/electricite_form.html",
            {
                "form": form,
                "recharge": form.instance,
                "type_carburant_choices": type_carburant_choices,
            },
        )


@login_required
def electricite_detail(request, electricite_id):
    tenant = request.user.societe
    with tenant_context(tenant):

        electricite = get_object_or_404(Electricite,id=electricite_id)

    return render(request,"recharge/electricite_detail.html",
        {
            "electricite": electricite,
            "exemplaire": electricite.voiture_exemplaire
        },
    )


@login_required
def modifier_electricite(request, electricite_id):

    tenant = request.user.societe

    with tenant_context(tenant):

        electricite = get_object_or_404(
            Electricite,
            pk=electricite_id
        )

        if request.method == "POST":

            form = ElectriciteForm(
                request.POST,
                request.FILES,
                instance=electricite
            )

            if form.is_valid():

                electricite = form.save()

                messages.success(
                    request,
                    _("La recharge a été mise à jour avec succès.")
                )

                return redirect("recharge:recharge_list")

            else:

                messages.error(
                    request,
                    _("Le formulaire contient des erreurs.")
                )

        else:

            form = ElectriciteForm(instance=electricite)

    return render(
        request,
        "recharge/modifier_electricite.html",
        {
            "form": form,
            "electricite": electricite,
            "exemplaire" : electricite.voiture_exemplaire
        }
    )


def check_immatriculation_elect(request):
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
def get_marques_elect(request):
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
def get_modeles_elect(request):
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
from django.db.models import Sum, Count, Min, Max
from django.db.models.functions import TruncMonth, TruncYear
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.views.decorators.cache import never_cache

from .models import Electricite

@method_decorator([login_required, never_cache], name="dispatch")
class ElectriciteStatView(TemplateView):
    template_name = "recharge/electricite_stat.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        electricites = Electricite.objects.select_related(
            "voiture_exemplaire",
            "voiture_exemplaire__voiture_modele",
            "voiture_exemplaire__voiture_modele__voiture_marque",
        )

        # -----------------------------
        # 📊 Statistiques globales
        # -----------------------------
        total_kW_global = Decimal("0")
        total_km_global = Decimal("0")

        voitures = electricites.values("voiture_exemplaire__id").annotate(
            km_min=Min("kilometrage_electricite"),
            km_max=Max("kilometrage_electricite"),
        )

        for v in voitures:
            km_min = Decimal(v["km_min"] or 0)
            km_max = Decimal(v["km_max"] or 0)
            km_total = km_max - km_min
            if km_total <= 0:
                continue

            # kW total pour cette voiture en excluant le premier relevé
            kW = electricites.filter(voiture_exemplaire__id=v["voiture_exemplaire__id"])
            if km_min != km_max:
                kW = kW.exclude(kilometrage_electricite=km_min)
            kW = kW.aggregate(total=Sum("kW"))["total"]
            kW = Decimal(str(kW or 0))

            total_kW_global += kW
            total_km_global += km_total

        conso_moyenne_global = (total_kW_global * Decimal("100") / total_km_global) if total_km_global > 0 else Decimal("0.0")
        context["conso_moyenne"] = conso_moyenne_global

        # Stats globales additionnelles
        global_stats = electricites.aggregate(
            total_kW=Sum("kW"),
            total_cout=Sum("prix_recharge"),
            total_tva=Sum("montant_tva"),
            total_recharges=Count("id"),
        )

        total_kW = Decimal(str(global_stats["total_kW"] or 0))
        total_cout = Decimal(str(global_stats["total_cout"] or 0))
        global_stats["prix_moyen_kW"] = (total_cout / total_kW) if total_kW > 0 else Decimal("0.0")
        global_stats["conso_moyenne"] = conso_moyenne_global

        context["global"] = global_stats

        # -----------------------------
        # 🔹 Totaux TVA par pays
        # -----------------------------
        PAYS_CHOICES = [('BE', "Belgique"), ('LU', "Luxembourg"), ('DE', "Allemagne")]
        context["totaux_par_pays"] = {
            code: Decimal(str(
                electricites.filter(pays=code).aggregate(total=Sum("montant_tva"))["total"] or 0
            ))
            for code, _ in PAYS_CHOICES
        }
        context["total_global"] = Decimal(str(
            electricites.aggregate(total=Sum("montant_tva"))["total"] or 0
        ))

        # -----------------------------
        # 🚗 Stats par voiture
        # -----------------------------
        par_voiture = electricites.values(
            "voiture_exemplaire__id",
            "voiture_exemplaire__voiture_modele__nom_modele",
            "voiture_exemplaire__voiture_modele__voiture_marque__nom_marque",
            "voiture_exemplaire__immatriculation",
            "voiture_exemplaire__pays",
        ).annotate(
            nb_recharges=Count("id"),
            total_kW=Sum("kW"),
            total_cout=Sum("prix_recharge"),
            km_min=Min("kilometrage_electricite"),
            km_max=Max("kilometrage_electricite"),
        )

        for v in par_voiture:
            km_min = Decimal(v["km_min"] or 0)
            km_max = Decimal(v["km_max"] or 0)
            km_total = km_max - km_min

            total_kW_v = Decimal(str(v["total_kW"] or 0))
            total_cout_v = Decimal(str(v["total_cout"] or 0))

            if km_total > 0:
                kW_n_1 = electricites.filter(voiture_exemplaire__id=v["voiture_exemplaire__id"])
                if km_min != km_max:
                    kW_n_1 = kW_n_1.exclude(kilometrage_electricite=km_min)
                kW_n_1 = Decimal(str(kW_n_1.aggregate(total=Sum("kW"))["total"] or 0))

                km_total_decimal = Decimal(str(km_total))

                v["conso_moyenne"] = (kW_n_1 * Decimal("100") / km_total_decimal)
                v["cout_km"] = (total_cout_v / km_total_decimal)
                v["prix_moyen_kW"] = (total_cout_v / total_kW_v) if total_kW_v > 0 else Decimal("0.0")
            else:
                v["conso_moyenne"] = Decimal("0.0")
                v["cout_km"] = Decimal("0.0")
                v["prix_moyen_kW"] = Decimal("0.0")

        context["par_voiture"] = par_voiture

        # -----------------------------
        # 📅 Stats par mois
        # -----------------------------
        par_mois = electricites.annotate(mois=TruncMonth("date")).values("mois").order_by("mois")
        context["conso_moyenne_mois"] = {}
        for m in par_mois:
            e_mois = electricites.filter(date__month=m["mois"].month, date__year=m["mois"].year)
            voitures_mois = e_mois.values("voiture_exemplaire__id").annotate(
                km_min=Min("kilometrage_electricite"),
                km_max=Max("kilometrage_electricite"),
            )

            total_kW_mois = Decimal("0")
            total_km_mois = Decimal("0")

            for v in voitures_mois:
                km_min = Decimal(v["km_min"] or 0)
                km_max = Decimal(v["km_max"] or 0)
                km_total = km_max - km_min

                if km_total <= 0:
                    continue

                kW = e_mois.filter(voiture_exemplaire__id=v["voiture_exemplaire__id"])
                if km_min != km_max:
                    kW = kW.exclude(kilometrage_electricite=km_min)
                kW = Decimal(str(kW.aggregate(total=Sum("kW"))["total"] or 0))

                total_kW_mois += kW
                total_km_mois += km_total

            context["conso_moyenne_mois"][m["mois"]] = (
                total_kW_mois * Decimal("100") / Decimal(str(total_km_mois))
            ) if total_km_mois > 0 else Decimal("0.0")

        # -----------------------------
        # 📅 Stats par année
        # -----------------------------
        par_an = electricites.annotate(an=TruncYear("date")).values("an").order_by("an")
        context["conso_moyenne_an"] = {}
        for a in par_an:
            e_an = electricites.filter(date__year=a["an"].year)
            voitures_an = e_an.values("voiture_exemplaire__id").annotate(
                km_min=Min("kilometrage_electricite"),
                km_max=Max("kilometrage_electricite"),
            )

            total_kW_an = Decimal("0")
            total_km_an = Decimal("0")

            for v in voitures_an:
                km_min = Decimal(v["km_min"] or 0)
                km_max = Decimal(v["km_max"] or 0)
                km_total = km_max - km_min

                if km_total <= 0:
                    continue

                kW = e_an.filter(voiture_exemplaire__id=v["voiture_exemplaire__id"])
                if km_min != km_max:
                    kW = kW.exclude(kilometrage_electricite=km_min)
                kW = Decimal(str(kW.aggregate(total=Sum("kW"))["total"] or 0))

                total_kW_an += kW
                total_km_an += km_total

            context["conso_moyenne_an"][a["an"]] = (
                total_kW_an * Decimal("100") / Decimal(str(total_km_an))
            ) if total_km_an > 0 else Decimal("0.0")

        return context



from decimal import Decimal
from django.db.models import Sum, Min, Max
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.functions import TruncMonth, TruncYear

class ElectriciteExemplaireStatView(LoginRequiredMixin, TemplateView):
    template_name = "recharge/electricite_exemplaire_stat.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        exemplaire_id = self.kwargs.get("exemplaire_id")
        tenant = self.request.user.societe

        with tenant_context(tenant):
            exemplaire = get_object_or_404(VoitureExemplaire, pk=exemplaire_id)
            recharges = Electricite.objects.filter(voiture_exemplaire=exemplaire)
            context["exemplaire"] = exemplaire

            # 🔹 Statistiques globales
            km_min = Decimal(recharges.aggregate(Min("kilometrage_electricite"))["kilometrage_electricite__min"] or 0)
            km_max = Decimal(recharges.aggregate(Max("kilometrage_electricite"))["kilometrage_electricite__max"] or 0)
            km_total = km_max - km_min

            total_kW = Decimal(recharges.exclude(kilometrage_electricite=km_min).aggregate(Sum("kW"))["kW__sum"] or 0)
            total_cout = Decimal(recharges.aggregate(Sum("prix_recharge"))["prix_recharge__sum"] or 0)
            total_kW_all = Decimal(recharges.aggregate(Sum("kW"))["kW__sum"] or 1)

            conso_moyenne = (total_kW * Decimal("100") / km_total) if km_total > 0 else Decimal("0.0")
            cout_km = (total_cout / km_total) if km_total > 0 else Decimal("0.0")
            prix_moyen_kW = (total_cout / total_kW_all) if total_kW_all > 0 else Decimal("0.0")

            context["global"] = {
                "total_recharges": recharges.count(),
                "total_kW": total_kW_all,
                "total_cout": total_cout,
                "total_tva": Decimal(recharges.aggregate(Sum("montant_tva"))["montant_tva__sum"] or 0),
                "prix_moyen_kW": prix_moyen_kW,
                "conso_moyenne": conso_moyenne,
                "cout_km": cout_km,
            }

            # 🔹 Totaux TVA par pays
            context["totaux_par_pays"] = Electricite.total_tva_par_pays_exemplaire(exemplaire)

            # 🔹 Total TVA global
            context["total_global"] = Decimal(recharges.aggregate(Sum("montant_tva"))["montant_tva__sum"] or 0)

            # 🔹 Stats par mois
            context["par_mois"] = []

            # obtenir un queryset unique par mois
            mois_groupes = (
                recharges
                .annotate(mois=TruncMonth("date"))
                .values("mois")
                .distinct()
                .order_by("mois")
            )

            for m in mois_groupes:
                e_mois = recharges.filter(date__month=m["mois"].month, date__year=m["mois"].year)
                km_min_mois = Decimal(
                    e_mois.aggregate(Min("kilometrage_electricite"))["kilometrage_electricite__min"] or 0)
                km_max_mois = Decimal(
                    e_mois.aggregate(Max("kilometrage_electricite"))["kilometrage_electricite__max"] or 0)
                km_total_mois = km_max_mois - km_min_mois

                total_kW_mois = Decimal(
                    e_mois.exclude(kilometrage_electricite=km_min_mois).aggregate(Sum("kW"))["kW__sum"] or 0)
                total_kW_mois_all = Decimal(e_mois.aggregate(Sum("kW"))["kW__sum"] or 1)
                total_cout_mois = Decimal(e_mois.aggregate(Sum("prix_recharge"))["prix_recharge__sum"] or 0)

                context["par_mois"].append({
                    "mois": m["mois"],
                    "nb_recharges": e_mois.count(),
                    "total_kW": total_kW_mois,
                    "total_cout": total_cout_mois,
                    "total_tva": Decimal(e_mois.aggregate(Sum("montant_tva"))["montant_tva__sum"] or 0),
                    "conso_moyenne": (total_kW_mois * Decimal("100") / km_total_mois) if km_total_mois > 0 else Decimal(
                        "0.0"),
                    "cout_km": (total_cout_mois / km_total_mois) if km_total_mois > 0 else Decimal("0.0"),
                    "prix_moyen_kW": (total_cout_mois / total_kW_mois_all) if total_kW_mois_all > 0 else Decimal("0.0"),
                })

            # 🔹 Stats par année
            context["par_an"] = []

            an_groupes = (
                recharges
                .annotate(an=TruncYear("date"))
                .values("an")
                .distinct()
                .order_by("an")
            )

            for a in an_groupes:
                e_an = recharges.filter(date__year=a["an"].year)
                km_min_an = Decimal(e_an.aggregate(Min("kilometrage_electricite"))["kilometrage_electricite__min"] or 0)
                km_max_an = Decimal(e_an.aggregate(Max("kilometrage_electricite"))["kilometrage_electricite__max"] or 0)
                km_total_an = km_max_an - km_min_an

                total_kW_an = Decimal(
                    e_an.exclude(kilometrage_electricite=km_min_an).aggregate(Sum("kW"))["kW__sum"] or 0)
                total_kW_an_all = Decimal(e_an.aggregate(Sum("kW"))["kW__sum"] or 1)
                total_cout_an = Decimal(e_an.aggregate(Sum("prix_recharge"))["prix_recharge__sum"] or 0)

                context["par_an"].append({
                    "an": a["an"],
                    "nb_recharges": e_an.count(),
                    "total_kW": total_kW_an,
                    "total_cout": total_cout_an,
                    "total_tva": Decimal(e_an.aggregate(Sum("montant_tva"))["montant_tva__sum"] or 0),
                    "conso_moyenne": (total_kW_an * Decimal("100") / km_total_an) if km_total_an > 0 else Decimal(
                        "0.0"),
                    "cout_km": (total_cout_an / km_total_an) if km_total_an > 0 else Decimal("0.0"),
                    "prix_moyen_kW": (total_cout_an / total_kW_an_all) if total_kW_an_all > 0 else Decimal("0.0"),
                })


        return context