from django.core.exceptions import ValidationError
from django.db import transaction

from django.http import JsonResponse
from django.utils import timezone
from django.views.generic import ListView
from django_tenants.utils import tenant_context
from guardian.mixins import LoginRequiredMixin
from decimal import Decimal
from django.db.models import Count, Max, Min, Sum, Q
from django.db.models.functions import TruncMonth, TruncYear
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView
from utilisateurs.models import UserLog
from voiture.voiture_exemplaire.models import VoitureExemplaire
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import get_language, gettext_noop
from django.utils.translation import gettext_lazy as _
from .forms import ElectriciteForm
from .models import Electricite, RechargeCarburant





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




def _definir(obj, champ, valeur):
    """Affecte la valeur seulement si le modèle possède ce champ."""
    if hasattr(obj, champ):
        setattr(obj, champ, valeur)


@login_required
def ajouter_recharge_all(request, exemplaire_id=None):

    societe = request.user.societe

    vehicules_societe = VoitureExemplaire.objects.filter(
        Q(client__societe=societe) | Q(client__isnull=True, societe=societe)
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
                data["voiture_exemplaire"] = str(voiture.pk)
            except VoitureExemplaire.DoesNotExist:
                erreur_immat = _("Voiture introuvable.")
            except VoitureExemplaire.MultipleObjectsReturned:
                erreur_immat = _("Plusieurs véhicules possèdent cette immatriculation.")

        form = ElectriciteForm(data, societe=societe)

        if erreur_immat:
            form.add_error("immatriculation", erreur_immat)

        if form.is_valid():
            try:
                with transaction.atomic():

                    # ==========================================
                    # VÉHICULE CONCERNÉ
                    # ==========================================
                    vehicule = form.cleaned_data.get("voiture_exemplaire") or exemplaire

                    if vehicule is None:
                        form.add_error("immatriculation", _("Veuillez indiquer une immatriculation."))
                        raise ValidationError("vehicule_manquant")

                    if not vehicules_societe.filter(pk=vehicule.pk).exists():
                        form.add_error("immatriculation", _("Véhicule non autorisé."))
                        raise ValidationError("vehicule_interdit")

                    # ==========================================
                    # VALEURS AVANT LA RECHARGE
                    # ==========================================
                    ancien_chassis = vehicule.kilometres_chassis or 0
                    ancien_moteur = vehicule.kilometres_moteur or 0
                    ancien_boite = vehicule.kilometres_boite or 0
                    ancien_embrayage = vehicule.kilometres_embrayage or 0

                    km = form.cleaned_data.get("kilometrage_electricite")
                    variation = 0

                    if km is not None:
                        km = int(km)

                        if km < ancien_chassis:
                            form.add_error(
                                "kilometrage_electricite",
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
                    # RECHARGE
                    # ==========================================
                    recharge = form.save(commit=False)

                    recharge.voiture_exemplaire = vehicule
                    recharge.utilisateur = request.user
                    recharge.societe = societe
                    recharge.kilometrage_electricite = km

                    _definir(recharge, "immatriculation", vehicule.immatriculation or "")
                    _definir(recharge, "voiture_modele", vehicule.voiture_modele)

                    if vehicule.voiture_modele:
                        _definir(recharge, "voiture_marque", vehicule.voiture_modele.voiture_marque)

                    _definir(recharge, "kilometrage_variation", variation)

                    # Kilométrages AVANT la recharge
                    _definir(recharge, "kilometres_chassis", ancien_chassis)
                    _definir(recharge, "kilometres_moteur", ancien_moteur)
                    _definir(recharge, "kilometres_boite", ancien_boite)
                    _definir(recharge, "kilometres_embrayage", ancien_embrayage)

                    # Sauvegardes
                    _definir(recharge, "kilometres_rollback", ancien_chassis)
                    _definir(recharge, "kilometres_moteur_rollback", ancien_moteur)
                    _definir(recharge, "kilometres_boite_rollback", ancien_boite)
                    _definir(recharge, "kilometres_embrayage_rollback", ancien_embrayage)

                    # Technicien
                    _definir(recharge, "tech_technicien", request.user)
                    _definir(recharge, "tech_nom_technicien", f"{request.user.prenom} {request.user.nom}")
                    _definir(recharge, "tech_role_technicien", request.user.role)
                    _definir(recharge, "tech_societe", societe)

                    recharge.save()
                    form.save_m2m()

                    # ==========================================
                    # LOG
                    # ==========================================
                    ACTION_AJOUT_RECHARGE = gettext_noop("Ajout d'une recharge électrique")

                    UserLog.objects.create(
                        utilisateur=request.user,
                        action=f"{ACTION_AJOUT_RECHARGE} - {vehicule.immatriculation}",
                    )

                messages.success(request, _("Recharge ajoutée avec succès."))

                langue = get_language() or "fr"

                return redirect(f"/tenant/{societe.schema_name}/{langue}/recharge/recharge/")

            except ValidationError:
                messages.error(request, _("Veuillez corriger les erreurs ci-dessous."))

            except Exception as e:
                messages.error(request, _("Erreur lors de l'enregistrement : %(erreur)s") % {"erreur": str(e)})

        else:
            messages.error(request, _("Veuillez corriger les erreurs ci-dessous."))

    else:
        initial = {}
        if exemplaire:
            initial = {
                "voiture_exemplaire": exemplaire.pk,
                "immatriculation": exemplaire.immatriculation,
            }
        form = ElectriciteForm(initial=initial, societe=societe)

    return render(request, "recharge/electricite_form.html", {
        "form": form,
        "exemplaire": exemplaire,
    })







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

            recharge.societe = societe

            if not recharge.utilisateur_id:
                recharge.utilisateur = request.user

            # Date introduite dans le formulaire
            recharge.date_recharge = form.cleaned_data.get("date_recharge")

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





@never_cache
@login_required
def electricite_delete(request, electricite_id):

    societe = request.user.societe

    # ==========================================================
    # AUTORISATIONS
    # ==========================================================
    roles_autorises = ["direction", "chef_mecanicien"]

    if request.user.role not in roles_autorises and not request.user.is_superuser:
        messages.error(request, _("Accès refusé"))
        return redirect("utilisateurs:dashboard")

    # ==========================================================
    # RÉCUPÉRATION DE LA RECHARGE
    # ==========================================================
    electricite = get_object_or_404(
        Electricite.objects.select_related("voiture_exemplaire"),
        id=electricite_id,
        societe=societe,
    )

    exemplaire = electricite.voiture_exemplaire

    # ==========================================================
    # SÉCURITÉ TENANT (véhicule société ou véhicule client)
    # ==========================================================
    if exemplaire and not (
        (exemplaire.client and exemplaire.client.societe == societe)
        or (exemplaire.client is None and exemplaire.societe == societe)
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
                km_recharge = electricite.kilometrage_electricite

                if exemplaire and km_recharge is not None:

                    # ------------------------------------------
                    # Valeurs AVANT la recharge
                    # ------------------------------------------
                    if getattr(electricite, "kilometres_rollback", None):
                        km_chassis = electricite.kilometres_rollback
                        km_moteur = getattr(electricite, "kilometres_moteur_rollback", None) or 0
                        km_boite = getattr(electricite, "kilometres_boite_rollback", None) or 0
                        km_embrayage = getattr(electricite, "kilometres_embrayage_rollback", None) or 0
                    else:
                        km_chassis = getattr(electricite, "kilometres_chassis", None) or 0
                        km_moteur = getattr(electricite, "kilometres_moteur", None) or 0
                        km_boite = getattr(electricite, "kilometres_boite", None) or 0
                        km_embrayage = getattr(electricite, "kilometres_embrayage", None) or 0

                    # ------------------------------------------
                    # Cette recharge est-elle la dernière intervention ?
                    # (km_chassis > 0 : on ne restaure jamais un compteur à 0
                    #  pour une ancienne recharge sans sauvegarde)
                    # ------------------------------------------
                    est_derniere = (exemplaire.kilometres_chassis or 0) == km_recharge

                    if est_derniere and km_chassis > 0:
                        VoitureExemplaire.objects.filter(pk=exemplaire.pk).update(
                            kilometres_chassis=km_chassis,
                            kilometres_moteur=km_moteur,
                            kilometres_boite=km_boite,
                            kilometres_embrayage=km_embrayage,
                            variation_kilometres=0,
                        )

                    # Sinon : une intervention plus récente a fixé
                    # le kilométrage → on ne touche pas au véhicule

                electricite.delete()

                ACTION_SUPPRESSION_RECHARGE = gettext_noop("Suppression d'une recharge électrique")

                UserLog.objects.create(
                    utilisateur=request.user,
                    action=f"{ACTION_SUPPRESSION_RECHARGE} - {immatriculation}",
                )

            messages.success(request, _("Recharge électrique supprimée avec succès."))
            return redirect("recharge:recharge_list")

        except Exception as e:
            messages.error(
                request,
                _("Erreur lors de la suppression : %(erreur)s") % {"erreur": str(e)}
            )

    # ==========================================================
    # PAGE DE CONFIRMATION
    # ==========================================================
    return render(request, "recharge/electricite_delete.html", {
        "electricite": electricite,
        "exemplaire": exemplaire,
    })

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
        pays_labels = dict(RechargeCarburant.PAYS_CHOICES_ELECT)

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
        pays_labels = dict(RechargeCarburant.PAYS_CHOICES_ELECT)

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