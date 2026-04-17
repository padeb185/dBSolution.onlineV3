
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
        global_stats = electricites.aggregate(
            total_kW=Sum("kW"),
            total_cout=Sum("prix_recharge"),
            total_tva=Sum("montant_tva"),
            total_recharges=Count("id"),
        )

        # 🔹 Totaux TVA par pays
        PAYS_CHOICES = [
            ('BE', "Belgique"),
            ('LU', "Luxembourg"),
            ('DE', "Allemagne"),
        ]
        totaux_par_pays = {}
        for code, _ in PAYS_CHOICES:
            totaux_par_pays[code] = electricites.filter(pays=code).aggregate(total=Sum("montant_tva"))["total"] or 0
        context["totaux_par_pays"] = totaux_par_pays

        # 🔹 Total TVA global
        total_global = electricites.aggregate(total=Sum("montant_tva"))["total"] or 0
        context["total_global"] = total_global

        # Calcul du prix moyen au kW (en Python pour éviter FieldError)
        total_kW = float(global_stats["total_kW"] or 0)
        total_cout = float(global_stats["total_cout"] or 0)
        global_stats["prix_moyen_kW"] = (total_cout / total_kW) if total_kW > 0 else 0.0

        context["global"] = global_stats

        # -----------------------------
        # 🚗 Stats par voiture
        # -----------------------------
        par_voiture_queryset = electricites.values(
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
        ).annotate(
            km_parcourus=ExpressionWrapper(F("km_max") - F("km_min"), output_field=FloatField()),
        ).annotate(
            conso_moyenne=Case(
                When(km_parcourus__gt=0,
                     then=ExpressionWrapper(F("total_kW") * 100.0 / F("km_parcourus"), output_field=FloatField())),
                default=Value(0.0),
                output_field=FloatField(),
            ),
            cout_km=Case(
                When(km_parcourus__gt=0,
                     then=ExpressionWrapper(F("total_cout") / F("km_parcourus"), output_field=FloatField())),
                default=Value(0.0),
                output_field=FloatField(),
            ),
            prix_moyen_kW=Case(
                When(total_kW__gt=0,
                     then=ExpressionWrapper(F("total_cout") / F("total_kW"), output_field=FloatField())),
                default=Value(0.0),
                output_field=FloatField(),
            ),
        ).order_by("-total_cout")

        # Calcul en Python pour plus de sécurité
        par_voiture = []
        for v in par_voiture_queryset:
            total_kW = float(v["total_kW"] or 0)
            total_cout = float(v["total_cout"] or 0)
            km_parcourus = float(v["km_parcourus"] or 0)
            v["conso_moyenne"] = (total_kW * 100 / km_parcourus) if km_parcourus > 0 else 0.0
            v["cout_km"] = (total_cout / km_parcourus) if km_parcourus > 0 else 0.0
            v["prix_moyen_kW"] = (total_cout / total_kW) if total_kW > 0 else 0.0
            par_voiture.append(v)

        context["par_voiture"] = par_voiture

        # -----------------------------
        # 📅 Stats par mois
        # -----------------------------
        par_mois = (
            electricites.annotate(mois=TruncMonth("date"))
            .values("mois")
            .annotate(
                nb_recharges=Count("id"),
                total_kW=Sum("kW"),
                total_cout=Sum("prix_recharge"),
            )
            .order_by("mois")
        )
        context["par_mois"] = par_mois

        # -----------------------------
        # 📅 Stats par année
        # -----------------------------
        par_an = (
            electricites.annotate(an=TruncYear("date"))
            .values("an")
            .annotate(
                nb_recharges=Count("id"),
                total_kW=Sum("kW"),
                total_cout=Sum("prix_recharge"),
            )
            .order_by("an")
        )
        context["par_an"] = par_an

        return context


class ElectriciteExemplaireStatView(LoginRequiredMixin, TemplateView):
    template_name = "recharge/electricite_exemplaire_stat.html"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Récupère l'ID depuis l'URL
        exemplaire_id = self.kwargs.get("exemplaire_id")

        # Récupère l'exemplaire en tenant compte du tenant
        tenant = self.request.user.societe
        with tenant_context(tenant):
            exemplaire = get_object_or_404(VoitureExemplaire, pk=exemplaire_id)
            recharges = Electricite.objects.filter(voiture_exemplaire=exemplaire)

            # 🔹 Stats globales pour cet exemplaire
            context["global"] = {
                "total_recharges": recharges.count(),
                "total_kW": Electricite.total_kW_all_exemplaire(exemplaire),
                "total_cout": Electricite.total_prix_all_exemplaire(exemplaire),
                "total_tva": Electricite.total_tva_all_exemplaire(exemplaire),
                "prix_moyen_kW": recharges.aggregate(avg=Avg("prix_watt"))["avg"] or 0,
            }

            # 🔹 Totaux TVA par pays
            context["totaux_par_pays"] = Electricite.total_tva_par_pays_exemplaire(exemplaire)

            total_global = recharges.aggregate(total=Sum("montant_tva"))["total"] or 0
            context["total_global"] = total_global

            # 🔹 Stats par mois
            context["par_mois"] = [
                {
                    "mois": m["mois"],
                    "nb_recharges": m["nb_recharges"],
                    "total_kW": m["total_kW"],
                    "total_cout": m["total_prix"],
                    "total_tva": m["total_tva"],
                }
                for m in recharges.annotate(mois=TruncMonth("date"))
                                 .values("mois")
                                 .annotate(
                                    total_litres=Sum("kW"),
                                    total_prix=Sum("prix_recharge"),
                                    total_tva=Sum("montant_tva"),
                                    nb_pleins=Count("id"),
                                 )
                                 .order_by("mois")
            ]

            # 🔹 Stats par année
            context["par_an"] = [
                {
                    "an": a["an"],
                    "nb_recharges": a["nb_recharges"],
                    "total_kW": a["total_kW"],
                    "total_cout": a["total_prix"],
                    "total_tva": a["total_tva"],
                }
                for a in recharges.annotate(an=TruncYear("date"))
                               .values("an")
                               .annotate(
                                   total_litres=Sum("kW"),
                                   total_prix=Sum("prix_recharge"),
                                   total_tva=Sum("montant_tva"),
                                   nb_pleins=Count("id"),
                               )
                               .order_by("an")
            ]

            return context