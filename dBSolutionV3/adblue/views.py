from django.core.exceptions import ValidationError

from django.db import transaction
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from django.utils.translation import gettext_lazy as _, gettext_noop
from django.views.decorators.http import require_GET
from django_tenants.utils import tenant_context
from utilisateurs.models import UserLog
from .forms import AdBlueForm
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
from .models import AdBlue







@method_decorator(login_required, name="dispatch")
@method_decorator(never_cache, name="dispatch")
class AdBlueListView(ListView):
    model = AdBlue
    template_name = "adblue/adblue_list.html"
    context_object_name = "adblues"

    def get_queryset(self):
        societe = self.request.user.societe


        return (
            AdBlue.objects
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
        pays_labels = dict(AdBlue.PAYS_CHOICES)

        totaux_par_pays = (
            AdBlue.objects
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
def ajouter_adblue_all(request, exemplaire_id=None):

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

        form = AdBlueForm(data)

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

                    km = form.cleaned_data.get("kilometrage_adblue")
                    variation = 0

                    if km is not None:
                        km = int(km)

                        if km < ancien_chassis:
                            form.add_error(
                                "kilometrage_adblue",
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
                    adblue = form.save(commit=False)

                    adblue.voiture_exemplaire = vehicule
                    adblue.utilisateur = request.user
                    adblue.societe = tenant
                    # Technicien (seulement si le modèle a ces champs)
                    if hasattr(adblue, "tech_technicien"):
                        adblue.tech_technicien = request.user
                    if hasattr(adblue, "tech_nom_technicien"):
                        adblue.tech_nom_technicien = f"{request.user.prenom} {request.user.nom}"
                    if hasattr(adblue, "tech_role_technicien"):
                        adblue.tech_role_technicien = request.user.role
                    if hasattr(adblue, "tech_societe"):
                        adblue.tech_societe = request.user.societe

                    adblue.kilometrage_adblue = km
                    adblue.kilometrage_variation = variation

                    # Kilométrages AVANT le plein
                    adblue.kilometres_chassis = ancien_chassis
                    adblue.kilometres_moteur = ancien_moteur
                    adblue.kilometres_boite = ancien_boite
                    adblue.kilometres_embrayage = ancien_embrayage

                    adblue.save()
                    form.save_m2m()

                    # ==========================================
                    # LOG
                    # ==========================================
                    ACTION_AJOUT_ADBLUE = gettext_noop("Ajout d'AdBlue")

                    UserLog.objects.create(
                        utilisateur=request.user,
                        action=f"{ACTION_AJOUT_ADBLUE} - {vehicule.immatriculation}",
                    )

                messages.success(request, _("AdBlue ajouté avec succès."))
                return redirect("adblue:adblue_list")

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

        form = AdBlueForm(initial=initial)

    return render(request, "adblue/adblue_form.html", {
        "form": form,
        "exemplaire": exemplaire,
    })




@never_cache
@login_required
def adblue_list(request):
    tenant = request.user.societe

    adblues = (
        AdBlue.objects
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
        "adblue/adblue_list.html",
        {
            "adblues": adblues,
        },
    )


@never_cache
@login_required
def adblue_detail(request, adblue_id):
    tenant = request.user.societe

    adblue = get_object_or_404(
        AdBlue.objects.select_related("voiture_exemplaire"),
        id=adblue_id,
        societe=tenant,
    )

    return render(
        request,
        "adblue/adblue_detail.html",
        {
            "adblue": adblue,
            "exemplaire": adblue.voiture_exemplaire,
        },
    )




@login_required
def modifier_adblue(request, adblue_id):

    tenant = request.user.societe

    adblue = get_object_or_404(
        AdBlue.objects.select_related("voiture_exemplaire"),
        pk=adblue_id,
        societe=tenant,
    )

    vehicule = adblue.voiture_exemplaire

    # ==================================================
    # VALEURS ENREGISTRÉES (lues en base, avant le formulaire)
    # ==================================================
    original = AdBlue.objects.get(pk=adblue.pk)

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

    ancien_km_adblue = original.kilometrage_adblue

    # ==================================================
    # POST
    # ==================================================
    if request.method == "POST":

        form = AdBlueForm(request.POST, request.FILES, instance=adblue)

        if form.is_valid():
            try:
                with transaction.atomic():

                    km = form.cleaned_data.get("kilometrage_adblue")
                    km = int(km) if km is not None else ancien_km_adblue

                    # Ce plein est-il la dernière intervention sur le véhicule ?
                    est_dernier = (
                        vehicule is not None
                        and ancien_km_adblue is not None
                        and (vehicule.kilometres_chassis or 0) == ancien_km_adblue
                    )

                    if km is not None:

                        if km < avant_chassis:
                            form.add_error(
                                "kilometrage_adblue",
                                _("Le kilométrage ne peut pas être inférieur à %(km)s km.")
                                % {"km": avant_chassis},
                            )
                            raise ValidationError("km_inferieur")

                        if km != ancien_km_adblue and not est_dernier:
                            form.add_error(
                                "kilometrage_adblue",
                                _("Une intervention a été enregistrée après ce plein : "
                                  "son kilométrage ne peut plus être modifié."),
                            )
                            raise ValidationError("pas_dernier")

                    variation = (km - avant_chassis) if km is not None else 0

                    # ==========================================
                    # PLEIN
                    # ==========================================
                    adblue = form.save(commit=False)

                    adblue.voiture_exemplaire = vehicule  # le véhicule ne change pas
                    adblue.societe = tenant
                    adblue.utilisateur = request.user

                    adblue.kilometrage_adblue = km
                    adblue.kilometrage_variation = variation

                    # Kilométrages AVANT le plein (jamais modifiés)
                    adblue.kilometres_chassis = avant_chassis
                    adblue.kilometres_moteur = avant_moteur
                    adblue.kilometres_boite = avant_boite
                    adblue.kilometres_embrayage = avant_embrayage

                    # Sauvegardes (remplies aussi pour les anciens pleins)
                    adblue.kilometres_rollback = avant_chassis
                    adblue.kilometres_moteur_rollback = avant_moteur
                    adblue.kilometres_boite_rollback = avant_boite
                    adblue.kilometres_embrayage_rollback = avant_embrayage

                    adblue.save()
                    form.save_m2m()

                    # ==========================================
                    # VÉHICULE (seulement si dernier plein
                    # et kilométrage modifié)
                    # ==========================================
                    if est_dernier and km is not None and km != ancien_km_adblue:
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
                    ACTION_MODIFICATION_ADBLUE = gettext_noop("Modification d'un plein d'AdBlue")

                    UserLog.objects.create(
                        utilisateur=request.user,
                        action=f"{ACTION_MODIFICATION_ADBLUE} - {vehicule.immatriculation if vehicule else '-'}",
                    )

                messages.success(request, _("Le plein d'AdBlue a été mis à jour avec succès."))
                return redirect("adblue:adblue_detail", adblue_id=adblue.id)

            except ValidationError:
                pass  # l'erreur est déjà attachée au champ

            except Exception as e:
                messages.error(request, _("Erreur lors de la modification : %(erreur)s") % {"erreur": str(e)})

        messages.error(request, _("Le formulaire contient des erreurs."))

    else:
        form = AdBlueForm(instance=adblue)

    return render(request, "adblue/modifier_adblue.html", {
        "form": form,
        "adblue": adblue,
        "exemplaire": vehicule,
    })






def adblue_edit(request, pk):
    adblue = get_object_or_404(AdBlue, pk=pk)
    if request.method == "POST":
        form = AdBlueForm(request.POST, instance=adblue)
        if form.is_valid():
            form.save()
            messages.success(request, _("AdBlue modifié avec succès."))
            return redirect("adblue_list")
        else:
            messages.error(request, _("Veuillez corriger les erreurs ci-dessous."))
    else:
        form = AdBlueForm(instance=adblue)
    return render(request, "adblue/adblue_form.html", {"form": form, "title": _("Modifier un plein")})





@never_cache
@login_required
def adblue_delete(request, adblue_id):

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
    adblue = get_object_or_404(
        AdBlue.objects.select_related("voiture_exemplaire"),
        id=adblue_id,
        societe=tenant,
    )

    exemplaire = adblue.voiture_exemplaire

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

                if exemplaire and adblue.kilometrage_adblue is not None:

                    # ------------------------------------------
                    # Valeurs AVANT le plein
                    # ------------------------------------------
                    if adblue.kilometres_rollback:
                        km_chassis = adblue.kilometres_rollback
                        km_moteur = adblue.kilometres_moteur_rollback or 0
                        km_boite = adblue.kilometres_boite_rollback or 0
                        km_embrayage = adblue.kilometres_embrayage_rollback or 0
                    else:
                        km_chassis = adblue.kilometres_chassis or 0
                        km_moteur = adblue.kilometres_moteur or 0
                        km_boite = adblue.kilometres_boite or 0
                        km_embrayage = adblue.kilometres_embrayage or 0

                    # ------------------------------------------
                    # Ce plein est-il la dernière intervention ?
                    # ------------------------------------------
                    est_dernier = (exemplaire.kilometres_chassis or 0) == adblue.kilometrage_adblue

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

                adblue.delete()

                ACTION_SUPPRESSION_ADBLUE = gettext_noop("Suppression d'un plein d'AdBlue")

                UserLog.objects.create(
                    utilisateur=request.user,
                    action=f"{ACTION_SUPPRESSION_ADBLUE} - {immatriculation}",
                )

            messages.success(request, _("AdBlue supprimé avec succès."))
            return redirect("adblue:adblue_list")

        except Exception as e:
            messages.error(
                request,
                _("Erreur lors de la suppression : %(erreur)s") % {"erreur": str(e)}
            )

    # ==========================================================
    # PAGE DE CONFIRMATION
    # ==========================================================
    return render(request, "adblue/adblue_delete.html", {
        "adblue": adblue,
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











class AdBlueStatView(LoginRequiredMixin, TemplateView):
    template_name = "adblue/adblue_stat.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        societe = self.request.user.societe

        adblues = (
            AdBlue.objects
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
        agregats_globaux = adblues.aggregate(
            total_litres=Sum("litres"),
            total_cout=Sum("prix_adblue"),
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
        pays_labels = dict(AdBlue.PAYS_CHOICES)

        totaux_par_pays_qs = (
            adblues
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
            adblues
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
                total_cout=Sum("prix_adblue"),
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
            adblues
            .annotate(mois=TruncMonth("date"))
            .values("mois")
            .annotate(
                nb_pleins=Count("id"),
                total_litres=Sum("litres"),
                total_cout=Sum("prix_adblue"),
                total_tva=Sum("montant_tva"),
                km_min=Min("kilometrage_adblue"),
                km_max=Max("kilometrage_adblue"),
            )
            .order_by("mois")
        )

        # ==========================================================
        # PAR ANNÉE
        # ==========================================================
        context["par_an"] = (
            adblues
            .annotate(an=ExtractYear("date"))
            .values("an")
            .annotate(
                nb_pleins=Count("id"),
                total_litres=Sum("litres"),
                total_cout=Sum("prix_adblue"),
                total_tva=Sum("montant_tva"),
                km_min=Min("kilometrage_adblue"),
                km_max=Max("kilometrage_adblue"),
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
            adblues
            .exclude(voiture_exemplaire_id__isnull=True)
            .values_list(
                "voiture_exemplaire_id",
                flat=True,
            )
            .distinct()
        )

        for vehicule_id in vehicule_ids:
            adblues_vehicule = (
                adblues
                .filter(
                    voiture_exemplaire_id=vehicule_id,
                )
                .order_by(
                    "date",
                    "kilometrage_adblue",
                )
            )

            ancien_km = None

            for adblue in adblues_vehicule:
                if adblue.kilometrage_adblue is None:
                    continue

                km_actuel = Decimal(
                    str(adblue.kilometrage_adblue)
                )

                litres = Decimal(
                    str(adblue.litres or 0)
                )

                if ancien_km is not None:
                    km_parcourus = (
                        km_actuel - ancien_km
                    )

                    if km_parcourus > 0:
                        total_litres_consommation += litres
                        total_km += km_parcourus

                        if adblue.date:
                            mois = adblue.date.replace(
                                day=1,
                                hour=0,
                                minute=0,
                                second=0,
                                microsecond=0,
                            )

                            annee = adblue.date.year

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










class AdBlueExemplaireStatView(LoginRequiredMixin, TemplateView):
    template_name = "adblue/adblue_exemplaire_stat.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        societe = self.request.user.societe
        exemplaire_id = self.kwargs.get("exemplaire_id")

        exemplaire = get_object_or_404(
            VoitureExemplaire,
            pk=exemplaire_id,
        )

        adblues = (
            AdBlue.objects
            .filter(
                societe=societe,
                voiture_exemplaire=exemplaire,
            )
            .select_related(
                "voiture_exemplaire",
                "voiture_exemplaire__voiture_modele",
                "voiture_exemplaire__voiture_modele__voiture_marque",
            )
            .order_by("date", "kilometrage_adblue")
        )

        context["exemplaire"] = exemplaire

        # ==========================================================
        # CONSOMMATION GLOBALE
        # ==========================================================
        total_litres_consommation = Decimal("0.0")
        total_km = Decimal("0.0")
        kilometrage_precedent = None

        for adblue in adblues:
            kilometrage = adblue.kilometrage_adblue
            litres = adblue.litres or Decimal("0.0")

            if kilometrage is None:
                continue

            if kilometrage_precedent is not None:
                difference_km = kilometrage - kilometrage_precedent

                if difference_km > 0:
                    total_litres_consommation += litres
                    total_km += difference_km

            kilometrage_precedent = kilometrage

        kilometrages = adblues.aggregate(
            minimum=Min("kilometrage_adblue"),
            maximum=Max("kilometrage_adblue"),
        )

        km_min = Decimal(str(kilometrages["minimum"] or 0))
        km_max = Decimal(str(kilometrages["maximum"] or 0))
        km_total = km_max - km_min

        agregats_globaux = adblues.aggregate(
            total_litres=Sum("litres"),
            total_cout=Sum("prix_adblue"),
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
            "total_pleins": adblues.count(),
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
        pays_labels = dict(AdBlue.PAYS_CHOICES)

        totaux_par_pays_qs = (
            adblues
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
            adblues
            .annotate(mois=TruncMonth("date"))
            .values("mois")
            .annotate(
                total_litres=Sum("litres"),
                total_prix=Sum("prix_adblue"),
                total_tva=Sum("montant_tva"),
                nb_pleins=Count("id"),
                km_min=Min("kilometrage_adblue"),
                km_max=Max("kilometrage_adblue"),
            )
            .order_by("mois")
        )

        par_mois = []
        conso_moyenne_mois = {}

        for mois_data in par_mois_qs:
            mois = mois_data["mois"]

            if mois is None:
                continue

            adblues_mois = adblues.filter(
                date__year=mois.year,
                date__month=mois.month,
            )

            total_litres_mois = Decimal("0.0")
            total_km_mois = Decimal("0.0")
            kilometrage_precedent = None

            for adblue in adblues_mois:
                kilometrage = adblue.kilometrage_adblue
                litres = adblue.litres or Decimal("0.0")

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
            adblues
            .annotate(an=TruncYear("date"))
            .values("an")
            .annotate(
                total_litres=Sum("litres"),
                total_prix=Sum("prix_adblue"),
                total_tva=Sum("montant_tva"),
                nb_pleins=Count("id"),
                km_min=Min("kilometrage_adblue"),
                km_max=Max("kilometrage_adblue"),
            )
            .order_by("an")
        )

        par_an = []
        conso_moyenne_an = {}

        for an_data in par_an_qs:
            annee = an_data["an"]

            if annee is None:
                continue

            adblues_annee = adblues.filter(
                date__year=annee.year,
            )

            total_litres_annee = Decimal("0.0")
            total_km_annee = Decimal("0.0")
            kilometrage_precedent = None

            for adblue in adblues_annee:
                kilometrage = adblue.kilometrage_adblue
                litres = adblue.litres or Decimal("0.0")

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
            "plaque_html": render_to_string(
                "maintenance/partials/plaque.html",
                {
                    "pays_plaque": voiture.pays,
                    "immat_plaque": voiture.immatriculation,
                    "taille": "petite",
                },
                request=request,
            ),
        })

    return JsonResponse(resultats, safe=False)