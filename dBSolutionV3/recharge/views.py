
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


from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _

from voiture.voiture_exemplaire.models import VoitureExemplaire

from .forms import ElectriciteForm


@login_required
def ajouter_recharge_all(request):
    societe = request.user.societe

    if request.method == "POST":
        form = ElectriciteForm(
            request.POST,
            societe=societe,
        )

        immatriculation = (
            request.POST.get("immatriculation", "")
            .strip()
        )

        voiture_exemplaire_id = request.POST.get(
            "voiture_exemplaire"
        )

        # Recherche du véhicule si le champ caché n'a pas été rempli.
        if immatriculation and not voiture_exemplaire_id:
            voiture = (
                VoitureExemplaire.objects
                .filter(
                    immatriculation__iexact=immatriculation,
                    societe=societe,
                )
                .first()
            )

            if voiture:
                data = request.POST.copy()
                data["voiture_exemplaire"] = str(voiture.pk)

                form = ElectriciteForm(
                    data,
                    societe=societe,
                )
            else:
                form.add_error(
                    "immatriculation",
                    _("Voiture introuvable."),
                )

        if form.is_valid():
            recharge = form.save(commit=False)

            recharge.utilisateur = request.user
            recharge.societe = societe

            voiture = recharge.voiture_exemplaire

            if voiture:
                recharge.immatriculation = (
                    voiture.immatriculation or ""
                )

                if hasattr(recharge, "kilometres_chassis"):
                    recharge.kilometres_chassis = (
                        voiture.kilometres_chassis or 0
                    )

            recharge.save()

            messages.success(
                request,
                _("Recharge ajoutée avec succès."),
            )

            langue = get_language() or "fr"
            schema_name = societe.schema_name

            return redirect(
                f"/tenant/{schema_name}/{langue}/"
                "recharge/recharge/"
            )

        messages.error(
            request,
            _("Veuillez corriger les erreurs ci-dessous."),
        )

    else:
        form = ElectriciteForm(
            societe=societe,
        )

    return render(
        request,
        "recharge/electricite_form.html",
        {
            "form": form,
        },
    )




from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from .models import Electricite


@login_required
def electricite_detail(request, electricite_id):
    societe = request.user.societe

    electricite = get_object_or_404(
        Electricite.objects.select_related(
            "voiture_exemplaire",
            "voiture_exemplaire__voiture_modele",
            "voiture_exemplaire__voiture_modele__voiture_marque",
            "utilisateur",
        ),
        id=electricite_id,
        societe=societe,
    )

    return render(
        request,
        "recharge/electricite_detail.html",
        {
            "electricite": electricite,
            "exemplaire": electricite.voiture_exemplaire,
        },
    )


from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _

from .forms import ElectriciteForm
from .models import Electricite


@login_required
def modifier_electricite(request, electricite_id):
    societe = request.user.societe

    electricite = get_object_or_404(
        Electricite.objects.select_related(
            "voiture_exemplaire",
            "voiture_exemplaire__voiture_modele",
            "voiture_exemplaire__voiture_modele__voiture_marque",
        ),
        pk=electricite_id,
        societe=societe,
    )

    if request.method == "POST":
        form = ElectriciteForm(
            request.POST,
            request.FILES,
            instance=electricite,
            societe=societe,
        )

        if form.is_valid():
            recharge = form.save(commit=False)

            # Garantir que la société et l’utilisateur ne changent pas.
            recharge.societe = societe

            if not recharge.utilisateur_id:
                recharge.utilisateur = request.user

            recharge.save()

            messages.success(
                request,
                _("La recharge a été mise à jour avec succès."),
            )

            langue = get_language() or "fr"

            return redirect(
                f"/tenant/{societe.schema_name}/{langue}/"
                "recharge/recharge/"
            )

        messages.error(
            request,
            _("Le formulaire contient des erreurs."),
        )

    else:
        form = ElectriciteForm(
            instance=electricite,
            societe=societe,
        )

    return render(
        request,
        "recharge/modifier_electricite.html",
        {
            "form": form,
            "electricite": electricite,
            "exemplaire": electricite.voiture_exemplaire,
        },
    )



@login_required
def check_immatriculation_elect(request):
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




@login_required
def electricite_delete(request, electricite_id):
    if request.user.role not in ["direction", "chef_mecanicien"]:
        messages.error(
            request,
            _("Vous n'avez pas l'autorisation de supprimer cette recharge.")
        )
        return redirect("recharge:electricite_list")

    electricite = get_object_or_404(Electricite, id=electricite_id)

    if request.method == "POST":
        electricite.delete()
        messages.success(request, _("Recharge électrique supprimée avec succès."))


    return render(request, "recharge/electricite_delete.html", {"electricite": electricite})



from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.db.models import Count, Max, Min, Sum
from django.db.models.functions import TruncMonth, TruncYear
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView

from .models import Electricite


@method_decorator([login_required, never_cache], name="dispatch")
class ElectriciteStatView(TemplateView):
    template_name = "recharge/electricite_stat.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        societe = self.request.user.societe

        electricites = (
            Electricite.objects
            .filter(societe=societe)
            .select_related(
                "voiture_exemplaire",
                "voiture_exemplaire__voiture_modele",
                "voiture_exemplaire__voiture_modele__voiture_marque",
            )
        )

        # ==========================================================
        # STATISTIQUES GLOBALES
        # ==========================================================
        total_kw_consommation = Decimal("0.0")
        total_km_global = Decimal("0.0")

        voitures = (
            electricites
            .exclude(voiture_exemplaire_id__isnull=True)
            .values("voiture_exemplaire_id")
            .annotate(
                km_min=Min("kilometrage_electricite"),
                km_max=Max("kilometrage_electricite"),
            )
        )

        for voiture in voitures:
            voiture_id = voiture["voiture_exemplaire_id"]

            km_min = Decimal(str(voiture["km_min"] or 0))
            km_max = Decimal(str(voiture["km_max"] or 0))
            km_total = km_max - km_min

            if km_total <= 0:
                continue

            recharges_voiture = electricites.filter(
                voiture_exemplaire_id=voiture_id,
            )

            # Exclusion du premier relevé kilométrique.
            if km_min != km_max:
                recharges_voiture = recharges_voiture.exclude(
                    kilometrage_electricite=km_min,
                )

            total_kw_voiture = Decimal(
                str(
                    recharges_voiture.aggregate(
                        total=Sum("kW")
                    )["total"]
                    or 0
                )
            )

            total_kw_consommation += total_kw_voiture
            total_km_global += km_total

        conso_moyenne_global = (
            total_kw_consommation
            * Decimal("100")
            / total_km_global
            if total_km_global > 0
            else Decimal("0.0")
        )

        agregats_globaux = electricites.aggregate(
            total_kW=Sum("kW"),
            total_cout=Sum("prix_recharge"),
            total_tva=Sum("montant_tva"),
            total_recharges=Count("id"),
        )

        total_kw_global = Decimal(
            str(agregats_globaux["total_kW"] or 0)
        )

        total_cout_global = Decimal(
            str(agregats_globaux["total_cout"] or 0)
        )

        total_tva_global = Decimal(
            str(agregats_globaux["total_tva"] or 0)
        )

        prix_moyen_kw = (
            total_cout_global / total_kw_global
            if total_kw_global > 0
            else Decimal("0.0")
        )

        context["global"] = {
            "total_kW": total_kw_global,
            "total_cout": total_cout_global,
            "total_tva": total_tva_global,
            "total_recharges": agregats_globaux["total_recharges"] or 0,
            "prix_moyen_kW": prix_moyen_kw,
            "conso_moyenne": conso_moyenne_global,
        }

        context["conso_moyenne"] = conso_moyenne_global

        # ==========================================================
        # TVA PAR PAYS
        # ==========================================================
        pays_labels = dict(Electricite.PAYS_CHOICES)

        totaux_par_pays_qs = (
            electricites
            .exclude(pays__isnull=True)
            .exclude(pays="")
            .values("pays")
            .annotate(total_tva=Sum("montant_tva"))
            .order_by("pays")
        )

        totaux_par_pays_affichage = []

        for ligne in totaux_par_pays_qs:
            code_pays = ligne["pays"]
            montant_tva = Decimal(
                str(ligne["total_tva"] or 0)
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

        # Maintien de l’ancien dictionnaire si le template l’utilise encore.
        context["totaux_par_pays"] = {
            pays["code"]: pays["tva"]
            for pays in totaux_par_pays_affichage
        }

        context["total_global"] = total_tva_global

        # ==========================================================
        # STATISTIQUES PAR VOITURE
        # ==========================================================
        par_voiture = list(
            electricites
            .exclude(voiture_exemplaire_id__isnull=True)
            .values(
                "voiture_exemplaire__id",
                "voiture_exemplaire__voiture_modele__nom_modele",
                "voiture_exemplaire__voiture_modele__voiture_marque__nom_marque",
                "voiture_exemplaire__immatriculation",
                "voiture_exemplaire__pays",
            )
            .annotate(
                nb_recharges=Count("id"),
                total_kW=Sum("kW"),
                total_cout=Sum("prix_recharge"),
                total_tva=Sum("montant_tva"),
                km_min=Min("kilometrage_electricite"),
                km_max=Max("kilometrage_electricite"),
            )
            .order_by("-total_cout")
        )

        for voiture in par_voiture:
            voiture_id = voiture["voiture_exemplaire__id"]

            km_min = Decimal(str(voiture["km_min"] or 0))
            km_max = Decimal(str(voiture["km_max"] or 0))
            km_total = km_max - km_min

            total_kw_voiture = Decimal(
                str(voiture["total_kW"] or 0)
            )

            total_cout_voiture = Decimal(
                str(voiture["total_cout"] or 0)
            )

            voiture["total_kW"] = total_kw_voiture
            voiture["total_cout"] = total_cout_voiture
            voiture["total_tva"] = Decimal(
                str(voiture["total_tva"] or 0)
            )

            if km_total > 0:
                recharges_voiture = electricites.filter(
                    voiture_exemplaire_id=voiture_id,
                )

                if km_min != km_max:
                    recharges_voiture = recharges_voiture.exclude(
                        kilometrage_electricite=km_min,
                    )

                kw_consommation = Decimal(
                    str(
                        recharges_voiture.aggregate(
                            total=Sum("kW")
                        )["total"]
                        or 0
                    )
                )

                voiture["conso_moyenne"] = (
                    kw_consommation
                    * Decimal("100")
                    / km_total
                )

                voiture["cout_km"] = (
                    total_cout_voiture / km_total
                )

                voiture["prix_moyen_kW"] = (
                    total_cout_voiture / total_kw_voiture
                    if total_kw_voiture > 0
                    else Decimal("0.0")
                )

            else:
                voiture["conso_moyenne"] = Decimal("0.0")
                voiture["cout_km"] = Decimal("0.0")
                voiture["prix_moyen_kW"] = Decimal("0.0")

        context["par_voiture"] = par_voiture

        # ==========================================================
        # STATISTIQUES PAR MOIS
        # ==========================================================
        par_mois = []

        mois_groupes = (
            electricites
            .annotate(mois=TruncMonth("date"))
            .values("mois")
            .distinct()
            .order_by("mois")
        )

        for mois_data in mois_groupes:
            mois = mois_data["mois"]

            if mois is None:
                continue

            electricites_mois = electricites.filter(
                date__year=mois.year,
                date__month=mois.month,
            )

            agregats_mois = electricites_mois.aggregate(
                nb_recharges=Count("id"),
                total_kW=Sum("kW"),
                total_cout=Sum("prix_recharge"),
                total_tva=Sum("montant_tva"),
            )

            total_kw_mois = Decimal(
                str(agregats_mois["total_kW"] or 0)
            )

            total_cout_mois = Decimal(
                str(agregats_mois["total_cout"] or 0)
            )

            total_tva_mois = Decimal(
                str(agregats_mois["total_tva"] or 0)
            )

            total_km_mois = Decimal("0.0")
            total_kw_effectif_mois = Decimal("0.0")

            voitures_mois = (
                electricites_mois
                .exclude(voiture_exemplaire_id__isnull=True)
                .values("voiture_exemplaire_id")
                .annotate(
                    km_min=Min("kilometrage_electricite"),
                    km_max=Max("kilometrage_electricite"),
                )
            )

            for voiture in voitures_mois:
                voiture_id = voiture["voiture_exemplaire_id"]

                km_min = Decimal(str(voiture["km_min"] or 0))
                km_max = Decimal(str(voiture["km_max"] or 0))
                km_total = km_max - km_min

                if km_total <= 0:
                    continue

                recharges_voiture = electricites_mois.filter(
                    voiture_exemplaire_id=voiture_id,
                )

                if km_min != km_max:
                    recharges_voiture = recharges_voiture.exclude(
                        kilometrage_electricite=km_min,
                    )

                kw_voiture = Decimal(
                    str(
                        recharges_voiture.aggregate(
                            total=Sum("kW")
                        )["total"]
                        or 0
                    )
                )

                total_kw_effectif_mois += kw_voiture
                total_km_mois += km_total

            conso_moyenne_mois = (
                total_kw_effectif_mois
                * Decimal("100")
                / total_km_mois
                if total_km_mois > 0
                else Decimal("0.0")
            )

            par_mois.append(
                {
                    "mois": mois,
                    "nb_recharges": (
                        agregats_mois["nb_recharges"]
                        or 0
                    ),
                    "total_kW": total_kw_mois,
                    "total_cout": total_cout_mois,
                    "total_tva": total_tva_mois,
                    "prix_moyen_kW": (
                        total_cout_mois / total_kw_mois
                        if total_kw_mois > 0
                        else Decimal("0.0")
                    ),
                    "conso_moyenne": conso_moyenne_mois,
                    "cout_km": (
                        total_cout_mois / total_km_mois
                        if total_km_mois > 0
                        else Decimal("0.0")
                    ),
                }
            )

        context["par_mois"] = par_mois

        # ==========================================================
        # STATISTIQUES PAR ANNÉE
        # ==========================================================
        par_an = []

        annees_groupees = (
            electricites
            .annotate(an=TruncYear("date"))
            .values("an")
            .distinct()
            .order_by("an")
        )

        for an_data in annees_groupees:
            annee = an_data["an"]

            if annee is None:
                continue

            electricites_annee = electricites.filter(
                date__year=annee.year,
            )

            agregats_annee = electricites_annee.aggregate(
                nb_recharges=Count("id"),
                total_kW=Sum("kW"),
                total_cout=Sum("prix_recharge"),
                total_tva=Sum("montant_tva"),
            )

            total_kw_annee = Decimal(
                str(agregats_annee["total_kW"] or 0)
            )

            total_cout_annee = Decimal(
                str(agregats_annee["total_cout"] or 0)
            )

            total_tva_annee = Decimal(
                str(agregats_annee["total_tva"] or 0)
            )

            total_km_annee = Decimal("0.0")
            total_kw_effectif_annee = Decimal("0.0")

            voitures_annee = (
                electricites_annee
                .exclude(voiture_exemplaire_id__isnull=True)
                .values("voiture_exemplaire_id")
                .annotate(
                    km_min=Min("kilometrage_electricite"),
                    km_max=Max("kilometrage_electricite"),
                )
            )

            for voiture in voitures_annee:
                voiture_id = voiture["voiture_exemplaire_id"]

                km_min = Decimal(str(voiture["km_min"] or 0))
                km_max = Decimal(str(voiture["km_max"] or 0))
                km_total = km_max - km_min

                if km_total <= 0:
                    continue

                recharges_voiture = electricites_annee.filter(
                    voiture_exemplaire_id=voiture_id,
                )

                if km_min != km_max:
                    recharges_voiture = recharges_voiture.exclude(
                        kilometrage_electricite=km_min,
                    )

                kw_voiture = Decimal(
                    str(
                        recharges_voiture.aggregate(
                            total=Sum("kW")
                        )["total"]
                        or 0
                    )
                )

                total_kw_effectif_annee += kw_voiture
                total_km_annee += km_total

            conso_moyenne_annee = (
                total_kw_effectif_annee
                * Decimal("100")
                / total_km_annee
                if total_km_annee > 0
                else Decimal("0.0")
            )

            par_an.append(
                {
                    "an": annee,
                    "nb_recharges": (
                        agregats_annee["nb_recharges"]
                        or 0
                    ),
                    "total_kW": total_kw_annee,
                    "total_cout": total_cout_annee,
                    "total_tva": total_tva_annee,
                    "prix_moyen_kW": (
                        total_cout_annee / total_kw_annee
                        if total_kw_annee > 0
                        else Decimal("0.0")
                    ),
                    "conso_moyenne": conso_moyenne_annee,
                    "cout_km": (
                        total_cout_annee / total_km_annee
                        if total_km_annee > 0
                        else Decimal("0.0")
                    ),
                }
            )

        context["par_an"] = par_an

        return context



class ElectriciteExemplaireStatView(
    LoginRequiredMixin,
    TemplateView,
):
    template_name = "recharge/electricite_exemplaire_stat.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        societe = self.request.user.societe
        exemplaire_id = self.kwargs.get("exemplaire_id")

        exemplaire = get_object_or_404(
            VoitureExemplaire,
            pk=exemplaire_id,
            societe=societe,
        )

        recharges = (
            Electricite.objects
            .filter(
                societe=societe,
                voiture_exemplaire=exemplaire,
            )
            .select_related(
                "voiture_exemplaire",
                "voiture_exemplaire__voiture_modele",
                "voiture_exemplaire__voiture_modele__voiture_marque",
            )
            .order_by("date", "kilometrage_electricite")
        )

        context["exemplaire"] = exemplaire

        # ==========================================================
        # STATISTIQUES GLOBALES
        # ==========================================================
        agregats = recharges.aggregate(
            km_min=Min("kilometrage_electricite"),
            km_max=Max("kilometrage_electricite"),
            total_kW=Sum("kW"),
            total_cout=Sum("prix_recharge"),
            total_tva=Sum("montant_tva"),
        )

        km_min = Decimal(str(agregats["km_min"] or 0))
        km_max = Decimal(str(agregats["km_max"] or 0))
        km_total = km_max - km_min

        total_kW_all = Decimal(
            str(agregats["total_kW"] or 0)
        )

        total_cout = Decimal(
            str(agregats["total_cout"] or 0)
        )

        total_tva = Decimal(
            str(agregats["total_tva"] or 0)
        )

        total_kW_consommation = Decimal(
            str(
                recharges
                .exclude(
                    kilometrage_electricite=km_min,
                )
                .aggregate(total=Sum("kW"))["total"]
                or 0
            )
        )

        conso_moyenne = (
            total_kW_consommation
            * Decimal("100")
            / km_total
            if km_total > 0
            else Decimal("0.0")
        )

        cout_km = (
            total_cout / km_total
            if km_total > 0
            else Decimal("0.0")
        )

        prix_moyen_kW = (
            total_cout / total_kW_all
            if total_kW_all > 0
            else Decimal("0.0")
        )

        context["global"] = {
            "total_recharges": recharges.count(),
            "total_kW": total_kW_all,
            "total_cout": total_cout,
            "total_tva": total_tva,
            "prix_moyen_kW": prix_moyen_kW,
            "conso_moyenne": conso_moyenne,
            "cout_km": cout_km,
        }

        # ==========================================================
        # TVA PAR PAYS
        # ==========================================================
        pays_labels = dict(Electricite.PAYS_CHOICES)

        totaux_par_pays_qs = (
            recharges
            .exclude(pays__isnull=True)
            .exclude(pays="")
            .values("pays")
            .annotate(total_tva=Sum("montant_tva"))
            .order_by("pays")
        )

        totaux_par_pays_affichage = []

        for ligne in totaux_par_pays_qs:
            code_pays = ligne["pays"]
            montant_tva = Decimal(
                str(ligne["total_tva"] or 0)
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

        # Compatibilité avec ton ancien template éventuel.
        context["totaux_par_pays"] = {
            pays["code"]: pays["tva"]
            for pays in totaux_par_pays_affichage
        }

        context["total_global"] = total_tva

        # ==========================================================
        # STATISTIQUES PAR MOIS
        # ==========================================================
        context["par_mois"] = []

        mois_groupes = (
            recharges
            .annotate(mois=TruncMonth("date"))
            .values("mois")
            .distinct()
            .order_by("mois")
        )

        for mois_data in mois_groupes:
            mois = mois_data["mois"]

            if mois is None:
                continue

            e_mois = recharges.filter(
                date__year=mois.year,
                date__month=mois.month,
            )

            agregats_mois = e_mois.aggregate(
                km_min=Min("kilometrage_electricite"),
                km_max=Max("kilometrage_electricite"),
                total_kW=Sum("kW"),
                total_cout=Sum("prix_recharge"),
                total_tva=Sum("montant_tva"),
            )

            km_min_mois = Decimal(
                str(agregats_mois["km_min"] or 0)
            )

            km_max_mois = Decimal(
                str(agregats_mois["km_max"] or 0)
            )

            km_total_mois = (
                km_max_mois - km_min_mois
            )

            total_kW_mois_all = Decimal(
                str(agregats_mois["total_kW"] or 0)
            )

            total_kW_mois_consommation = Decimal(
                str(
                    e_mois
                    .exclude(
                        kilometrage_electricite=km_min_mois,
                    )
                    .aggregate(total=Sum("kW"))["total"]
                    or 0
                )
            )

            total_cout_mois = Decimal(
                str(agregats_mois["total_cout"] or 0)
            )

            total_tva_mois = Decimal(
                str(agregats_mois["total_tva"] or 0)
            )

            context["par_mois"].append(
                {
                    "mois": mois,
                    "nb_recharges": e_mois.count(),
                    "total_kW": total_kW_mois_all,
                    "total_cout": total_cout_mois,
                    "total_tva": total_tva_mois,
                    "conso_moyenne": (
                        total_kW_mois_consommation
                        * Decimal("100")
                        / km_total_mois
                        if km_total_mois > 0
                        else Decimal("0.0")
                    ),
                    "cout_km": (
                        total_cout_mois / km_total_mois
                        if km_total_mois > 0
                        else Decimal("0.0")
                    ),
                    "prix_moyen_kW": (
                        total_cout_mois
                        / total_kW_mois_all
                        if total_kW_mois_all > 0
                        else Decimal("0.0")
                    ),
                }
            )

        # ==========================================================
        # STATISTIQUES PAR ANNÉE
        # ==========================================================
        context["par_an"] = []

        annees_groupees = (
            recharges
            .annotate(an=TruncYear("date"))
            .values("an")
            .distinct()
            .order_by("an")
        )

        for an_data in annees_groupees:
            annee = an_data["an"]

            if annee is None:
                continue

            e_an = recharges.filter(
                date__year=annee.year,
            )

            agregats_an = e_an.aggregate(
                km_min=Min("kilometrage_electricite"),
                km_max=Max("kilometrage_electricite"),
                total_kW=Sum("kW"),
                total_cout=Sum("prix_recharge"),
                total_tva=Sum("montant_tva"),
            )

            km_min_an = Decimal(
                str(agregats_an["km_min"] or 0)
            )

            km_max_an = Decimal(
                str(agregats_an["km_max"] or 0)
            )

            km_total_an = km_max_an - km_min_an

            total_kW_an_all = Decimal(
                str(agregats_an["total_kW"] or 0)
            )

            total_kW_an_consommation = Decimal(
                str(
                    e_an
                    .exclude(
                        kilometrage_electricite=km_min_an,
                    )
                    .aggregate(total=Sum("kW"))["total"]
                    or 0
                )
            )

            total_cout_an = Decimal(
                str(agregats_an["total_cout"] or 0)
            )

            total_tva_an = Decimal(
                str(agregats_an["total_tva"] or 0)
            )

            context["par_an"].append(
                {
                    "an": annee,
                    "nb_recharges": e_an.count(),
                    "total_kW": total_kW_an_all,
                    "total_cout": total_cout_an,
                    "total_tva": total_tva_an,
                    "conso_moyenne": (
                        total_kW_an_consommation
                        * Decimal("100")
                        / km_total_an
                        if km_total_an > 0
                        else Decimal("0.0")
                    ),
                    "cout_km": (
                        total_cout_an / km_total_an
                        if km_total_an > 0
                        else Decimal("0.0")
                    ),
                    "prix_moyen_kW": (
                        total_cout_an / total_kW_an_all
                        if total_kW_an_all > 0
                        else Decimal("0.0")
                    ),
                }
            )

        return context