from datetime import datetime

from django.core.exceptions import ValidationError

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import ListView
from maintenance.models import Maintenance
from utilisateurs.models import UserLog
from voiture.voiture_exemplaire.models import VoitureExemplaire
from django.db.models import Q
from django.utils.translation import gettext_lazy as _, gettext_noop
from weasyprint import HTML
from .forms import EmbrayageForm
from .models import Embrayage
from django.db import connection, transaction





@method_decorator([login_required, never_cache], name="dispatch")
class EmbrayageListView(ListView):
    model = Embrayage
    template_name = "embrayage/embrayage_list.html"
    context_object_name = "embrayages"


    def get_queryset(self):
        user = self.request.user
        tenant = user.societe

        exemplaire_id = self.kwargs.get("exemplaire_id")

        queryset = Embrayage.objects.select_related(
            "voiture_exemplaire",
            "maintenance",
            "tech_societe",
            "tech_technicien",
        )

        # =========================
        # FILTRE PAR VÉHICULE
        # =========================
        if exemplaire_id:
            queryset = queryset.filter(
                voiture_exemplaire_id=exemplaire_id
            )

        # =========================
        # SÉCURITÉ SOCIÉTÉ
        # =========================
        queryset = queryset.filter(
            Q(voiture_exemplaire__client__societe=tenant)
            |
            Q(
                voiture_exemplaire__client__isnull=True,
                voiture_exemplaire__societe=tenant,
            )
        )

        return queryset.order_by("-id")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        tenant = self.request.user.societe
        exemplaire_id = self.kwargs.get("exemplaire_id")

        if exemplaire_id:
            context["exemplaire"] = get_object_or_404(
                VoitureExemplaire.objects.filter(
                    Q(client__societe=tenant)
                    |
                    Q(
                        client__isnull=True,
                        societe=tenant,
                    )
                ),
                id=exemplaire_id,
            )

        roles_autorises = [
            "mecanicien",
            "apprenti",
            "magasinier",
            "chef_mecanicien",
            "direction",
        ]

        context["is_checkup_allowed"] = (
            self.request.user.role
            in roles_autorises
        )

        return context

@never_cache
@login_required
def embrayage_form_view(request, exemplaire_id):

    tenant = request.user.societe
    role = request.user.role
    maintenance = None

    exemplaire = get_object_or_404(
        VoitureExemplaire.objects.filter(
            Q(client__societe=tenant) | Q(client__isnull=True, societe=tenant)
        ),
        id=exemplaire_id,
    )

    roles_autorises = ["mecanicien", "apprenti", "magasinier", "chef_mecanicien", "direction"]

    if role not in roles_autorises:
        messages.error(request, _("Accès refusé."))
        return redirect("utilisateurs:dashboard")

    # =========================================================
    # POST
    # =========================================================
    if request.method == "POST":

        instance_embrayage = Embrayage(
            voiture_exemplaire=exemplaire,
            kilometres_chassis=exemplaire.kilometres_chassis,
        )
        instance_embrayage.assign_technicien(request.user)

        form = EmbrayageForm(
            request.POST,
            instance=instance_embrayage,
            user=request.user,
            exemplaire=exemplaire,
        )

        if form.is_valid():
            try:
                with transaction.atomic():

                    # ==========================================
                    # VALEURS AVANT INTERVENTION
                    # ==========================================
                    ancien_chassis = exemplaire.kilometres_chassis or 0
                    ancien_moteur = exemplaire.kilometres_moteur or 0
                    ancien_boite = exemplaire.kilometres_boite or 0
                    ancien_embrayage = exemplaire.kilometres_embrayage or 0

                    # ==========================================
                    # NOUVEAU KILOMÉTRAGE
                    # ==========================================
                    km = form.cleaned_data.get("kilometres_remplacement_embrayage")

                    if km is None:
                        form.add_error("kilometres_remplacement_embrayage", _("Le kilométrage est obligatoire."))
                        raise ValidationError("km_obligatoire")

                    km = int(km)

                    if km < ancien_chassis:
                        form.add_error(
                            "kilometres_remplacement_embrayage",
                            _("Le kilométrage du remplacement de l'embrayage ne peut pas être "
                              "inférieur au kilométrage actuel du véhicule."),
                        )
                        raise ValidationError("km_inferieur")

                    variation = km - ancien_chassis

                    # ==========================================
                    # EXEMPLAIRE
                    # ==========================================
                    exemplaire.kilometres_rollback = ancien_chassis
                    exemplaire.kilometres_moteur_rollback = ancien_moteur
                    exemplaire.kilometres_boite_rollback = ancien_boite
                    exemplaire.kilometres_embrayage_rollback = ancien_embrayage

                    exemplaire.date_derniere_intervention = timezone.localtime(timezone.now()).date()
                    exemplaire.kilometres_chassis = km
                    exemplaire.kilometres_remplacement_embrayage = km  # embrayage neuf → 0

                    exemplaire.update_kilometres()

                    exemplaire.save(update_fields=[
                        "kilometres_chassis",
                        "date_derniere_intervention",
                        "kilometres_rollback",
                        "kilometres_moteur_rollback",
                        "kilometres_boite_rollback",
                        "kilometres_embrayage_rollback",
                        "kilometres_remplacement_embrayage",
                        "kilometres_moteur",
                        "kilometres_boite",
                        "kilometres_embrayage",
                        "variation_kilometres",
                    ])

                    # ==========================================
                    # MAINTENANCE
                    # ==========================================
                    maintenance = Maintenance.objects.create(
                        societe=request.user.societe,
                        voiture_exemplaire=exemplaire,
                        immatriculation=exemplaire.immatriculation,
                        date_intervention=timezone.now().date(),
                        kilometres_chassis=exemplaire.kilometres_chassis,
                        kilometres_dernier_entretien=exemplaire.kilometres_dernier_entretien,
                        type_maintenance=Maintenance.TypeMaintenance.EMBRAYAGE,
                        tag=Maintenance.Tag.JAUNE,
                        tech_technicien=request.user,
                        tech_societe=request.user.societe,
                        tech_nom_technicien=f"{request.user.prenom} {request.user.nom}",
                        tech_role_technicien=request.user.role,
                    )

                    if role == "mecanicien":
                        maintenance.mecanicien = request.user
                    elif role == "chef_mecanicien":
                        maintenance.chef_mecanicien = request.user
                    elif role == "apprenti":
                        maintenance.apprentis.add(request.user)
                    elif role == "magasinier":
                        maintenance.magasinier = request.user
                    elif role == "direction":
                        maintenance.direction = request.user

                    maintenance.save()

                    # ==========================================
                    # EMBRAYAGE
                    # ==========================================
                    embrayage = form.save(commit=False)
                    embrayage.voiture_exemplaire = exemplaire
                    embrayage.maintenance = maintenance

                    embrayage_depose = ancien_embrayage + variation

                    # Kilométrages au moment de l'intervention
                    embrayage.kilometres_chassis = ancien_chassis
                    embrayage.kilometres_moteur = ancien_moteur
                    embrayage.kilometres_boite = ancien_boite
                    embrayage.kilometres_embrayage = embrayage_depose

                    embrayage.kilometres_remplacement_embrayage = km
                    embrayage.kilometrage_embrayage = km  # colonne NOT NULL
                    embrayage.kilometrage_variation = variation

                    # Sauvegardes pour la suppression (valeurs AVANT)
                    embrayage.kilometres_rollback = ancien_chassis
                    embrayage.kilometres_moteur_rollback = ancien_moteur
                    embrayage.kilometres_boite_rollback = ancien_boite
                    embrayage.kilometres_embrayage_rollback = ancien_embrayage

                    embrayage.assign_technicien(request.user)
                    embrayage.tech_last_maintained_by = request.user

                    embrayage.save()
                    form.save_m2m()

                    # ==========================================
                    # ÉCRITURE FINALE (après les save() des modèles)
                    # ==========================================
                    Embrayage.objects.filter(pk=embrayage.pk).update(
                        kilometres_embrayage=embrayage_depose
                    )

                    VoitureExemplaire.objects.filter(pk=exemplaire.pk).update(
                        kilometres_chassis=km,
                        kilometres_remplacement_embrayage=km,
                        kilometres_embrayage=0,
                    )

                    ACTION_REMPLACEMENT_EMBRAYAGE = gettext_noop("Remplacement de l'embrayage")

                    UserLog.objects.create(
                        utilisateur=request.user,
                        action=f"{ACTION_REMPLACEMENT_EMBRAYAGE} - {exemplaire.immatriculation}",
                    )

                messages.success(request, _("Le remplacement de l'embrayage a été enregistré avec succès."))

                return redirect(
                    f"{reverse('embrayage:embrayage_list', kwargs={'exemplaire_id': exemplaire.id})}?saved=1"
                )

            except ValidationError:
                messages.error(request, _("Le formulaire contient des erreurs."))

            except Exception as e:
                messages.error(request, _("Erreur lors de l'enregistrement : %(erreur)s") % {"erreur": str(e)})

        else:
            messages.error(request, _("Le formulaire contient des erreurs."))

    # =========================================================
    # GET
    # =========================================================
    else:
        instance_embrayage = Embrayage(
            voiture_exemplaire=exemplaire,
            kilometres_chassis=exemplaire.kilometres_chassis or 0,
            kilometres_moteur=exemplaire.kilometres_moteur or 0,
            kilometres_boite=exemplaire.kilometres_boite or 0,
            kilometres_embrayage=exemplaire.kilometres_embrayage or 0,
        )
        instance_embrayage.assign_technicien(request.user)

        form = EmbrayageForm(
            instance=instance_embrayage,
            user=request.user,
            exemplaire=exemplaire,
        )

    return render(request, "embrayage/embrayage_form.html", {
        "exemplaire": exemplaire,
        "immatriculation": exemplaire.immatriculation,
        "maintenance": maintenance,
        "form": form,
        "sections": _sections_embrayage(form),
        "now": timezone.now(),
    })




# ------------
# Vue détail boite
# -----------------------------
@login_required
def embrayage_detail_view(request, embrayage_id):
    embrayage = get_object_or_404(
        Embrayage.objects.select_related("voiture_exemplaire"),
        id=embrayage_id
    )

    context = {
        "embrayage": embrayage,
        "exemplaire": embrayage.voiture_exemplaire,
    }
    return render(request, "embrayage/embrayage_detail.html", context)




@login_required
def modifier_embrayage_view(request, embrayage_id):

    tenant = request.user.societe

    embrayage = get_object_or_404(
        Embrayage.objects.select_related("voiture_exemplaire"),
        id=embrayage_id,
    )
    exemplaire = embrayage.voiture_exemplaire

    if not (
        (exemplaire.client and exemplaire.client.societe == tenant)
        or (exemplaire.client is None and exemplaire.societe == tenant)
    ):
        messages.error(request, _("Accès refusé"))
        return redirect("utilisateurs:dashboard")

    # =========================================================
    # VALEURS ENREGISTRÉES (lues en base, avant le formulaire)
    # =========================================================
    original = Embrayage.objects.get(pk=embrayage.pk)

    if original.kilometres_rollback:
        avant_chassis = original.kilometres_rollback
        avant_moteur = original.kilometres_moteur_rollback or 0
        avant_boite = original.kilometres_boite_rollback or 0
        avant_embrayage = original.kilometres_embrayage_rollback or 0
    else:
        avant_chassis = original.kilometres_chassis or 0
        avant_moteur = original.kilometres_moteur or 0
        avant_boite = original.kilometres_boite or 0
        avant_embrayage = original.kilometres_embrayage or 0

    ancien_km_remplacement = original.kilometres_remplacement_embrayage or avant_chassis
    ancien_embrayage_depose = original.kilometres_embrayage or 0

    # =========================================================
    # POST
    # =========================================================
    if request.method == "POST":

        form = EmbrayageForm(
            request.POST,
            instance=embrayage,
            user=request.user,
            exemplaire=exemplaire,
        )

        if form.is_valid():
            try:
                with transaction.atomic():

                    km = form.cleaned_data.get("kilometres_remplacement_embrayage")
                    km = int(km) if km is not None else ancien_km_remplacement

                    if km < avant_chassis:
                        form.add_error(
                            "kilometres_remplacement_embrayage",
                            _("Le kilométrage ne peut pas être inférieur à %(km)s km.") % {"km": avant_chassis},
                        )
                        raise ValidationError("km_inferieur")

                    # Un embrayage plus récent a été monté depuis ?
                    est_dernier_embrayage = (
                        (exemplaire.kilometres_remplacement_embrayage or 0) == ancien_km_remplacement
                    )

                    if km != ancien_km_remplacement and not est_dernier_embrayage:
                        form.add_error(
                            "kilometres_remplacement_embrayage",
                            _("Seul le dernier remplacement de l'embrayage peut voir son kilométrage modifié."),
                        )
                        raise ValidationError("pas_dernier")

                    variation = km - avant_chassis

                    # ==========================================
                    # EMBRAYAGE DÉPOSÉ : valeur du formulaire,
                    # jamais inférieure à la valeur enregistrée
                    # ==========================================
                    embrayage_form = form.cleaned_data.get("kilometres_embrayage")

                    if embrayage_form is None:
                        embrayage_form = avant_embrayage + variation

                    embrayage_depose = max(int(embrayage_form), ancien_embrayage_depose)

                    # ==========================================
                    # EMBRAYAGE
                    # ==========================================
                    embrayage = form.save(commit=False)
                    embrayage.voiture_exemplaire = exemplaire

                    embrayage.kilometres_chassis = avant_chassis
                    embrayage.kilometres_moteur = avant_moteur
                    embrayage.kilometres_boite = avant_boite
                    embrayage.kilometres_embrayage = embrayage_depose

                    embrayage.kilometres_remplacement_embrayage = km
                    embrayage.kilometrage_embrayage = km  # colonne NOT NULL
                    embrayage.kilometrage_variation = variation

                    # Les sauvegardes ne changent jamais en modification
                    embrayage.kilometres_rollback = original.kilometres_rollback
                    embrayage.kilometres_moteur_rollback = original.kilometres_moteur_rollback
                    embrayage.kilometres_boite_rollback = original.kilometres_boite_rollback
                    embrayage.kilometres_embrayage_rollback = original.kilometres_embrayage_rollback

                    embrayage.assign_technicien(request.user)
                    embrayage.tech_last_maintained_by = request.user

                    embrayage.save()
                    form.save_m2m()

                    # ==========================================
                    # ÉCRITURE FINALE (après save())
                    # ==========================================
                    Embrayage.objects.filter(pk=embrayage.pk).update(
                        kilometres_embrayage=embrayage_depose
                    )

                    if est_dernier_embrayage:

                        chassis_actuel = exemplaire.kilometres_chassis or 0

                        # Rien n'a bougé depuis ce remplacement ?
                        if chassis_actuel == ancien_km_remplacement:
                            nouveau_chassis = km
                            nouveau_moteur = avant_moteur + variation
                            nouvelle_boite = avant_boite + variation
                        else:
                            nouveau_chassis = chassis_actuel
                            nouveau_moteur = exemplaire.kilometres_moteur or 0
                            nouvelle_boite = exemplaire.kilometres_boite or 0

                        VoitureExemplaire.objects.filter(pk=exemplaire.pk).update(
                            kilometres_chassis=nouveau_chassis,
                            kilometres_remplacement_embrayage=km,
                            kilometres_embrayage=max(0, nouveau_chassis - km),
                            kilometres_moteur=nouveau_moteur,
                            kilometres_boite=nouvelle_boite,
                            date_derniere_intervention=timezone.localtime(timezone.now()).date(),
                        )

                    ACTION_MODIFICATION_REMPLACEMENT_EMBRAYAGE = gettext_noop(
                        "Modification du remplacement de l'embrayage"
                    )

                    UserLog.objects.create(
                        utilisateur=request.user,
                        action=f"{ACTION_MODIFICATION_REMPLACEMENT_EMBRAYAGE} - {exemplaire.immatriculation}",
                    )

                messages.success(request, _("Remplacement de l'embrayage modifié avec succès !"))

                return redirect(
                    f"{reverse('embrayage:embrayage_detail', kwargs={'embrayage_id': embrayage.id})}?saved=1"
                )

            except ValidationError:
                messages.error(request, _("Kilométrage invalide"))

            except Exception as e:
                messages.error(request, _("Erreur lors de la modification : %(error)s") % {"error": str(e)})

        else:
            messages.error(request, _("Le formulaire contient des erreurs."))

    # =========================================================
    # GET
    # =========================================================
    else:
        form = EmbrayageForm(
            instance=embrayage,
            user=request.user,
            exemplaire=exemplaire,
        )

    return render(request, "embrayage/modifier_embrayage.html", {
        "form": form,
        "embrayage": embrayage,
        "sections": _sections_embrayage(form),
        "exemplaire": exemplaire,
    })



@never_cache
@login_required
def delete_embrayage_view(request, embrayage_id):

    tenant = request.user.societe
    role = request.user.role

    roles_autorises = ["direction", "chef_mecanicien"]

    if role not in roles_autorises and not request.user.is_superuser:
        messages.error(request, _("Accès refusé"))
        return redirect("utilisateurs:dashboard")

    embrayage = get_object_or_404(
        Embrayage.objects.select_related("voiture_exemplaire", "maintenance"),
        id=embrayage_id,
    )

    exemplaire = embrayage.voiture_exemplaire
    maintenance = embrayage.maintenance

    if not (
        (exemplaire.client and exemplaire.client.societe == tenant)
        or (exemplaire.client is None and exemplaire.societe == tenant)
    ):
        messages.error(request, _("Accès refusé"))
        return redirect("utilisateurs:dashboard")

    # ==================================================
    # DELETE
    # ==================================================
    if request.method == "POST":

        try:
            with transaction.atomic():

                immatriculation = exemplaire.immatriculation
                e = embrayage

                # ------------------------------------------
                # Valeurs AVANT intervention
                # ------------------------------------------
                if e.kilometres_rollback:
                    km_chassis = e.kilometres_rollback
                    km_moteur = e.kilometres_moteur_rollback or 0
                    km_boite = e.kilometres_boite_rollback or 0
                    km_embrayage = e.kilometres_embrayage_rollback or 0
                else:
                    km_chassis = e.kilometres_chassis or 0
                    km_moteur = e.kilometres_moteur or 0
                    km_boite = e.kilometres_boite or 0
                    km_embrayage = e.kilometres_embrayage or 0

                km_remplacement = e.kilometres_remplacement_embrayage or 0
                ancien_point_embrayage = max(0, km_chassis - km_embrayage)

                # Cet embrayage est-il celui actuellement monté ?
                est_dernier_embrayage = (
                    (exemplaire.kilometres_remplacement_embrayage or 0) == km_remplacement
                )

                # Le châssis a-t-il bougé depuis (autre intervention) ?
                chassis_actuel = exemplaire.kilometres_chassis or 0
                rien_depuis = chassis_actuel == km_remplacement

                if est_dernier_embrayage and rien_depuis:
                    # Retour exact à l'état d'avant le remplacement
                    VoitureExemplaire.objects.filter(pk=exemplaire.pk).update(
                        kilometres_chassis=km_chassis,
                        kilometres_moteur=km_moteur,
                        kilometres_boite=km_boite,
                        kilometres_embrayage=km_embrayage,
                        kilometres_remplacement_embrayage=ancien_point_embrayage,
                    )

                elif est_dernier_embrayage:
                    # D'autres interventions depuis : on garde le châssis,
                    # on annule seulement le changement d'embrayage
                    VoitureExemplaire.objects.filter(pk=exemplaire.pk).update(
                        kilometres_remplacement_embrayage=ancien_point_embrayage,
                        kilometres_embrayage=max(0, chassis_actuel - ancien_point_embrayage),
                    )

                # Sinon : un embrayage plus récent est monté → on ne touche à rien

                embrayage.delete()

                if maintenance:
                    maintenance.delete()

                ACTION_SUPPRESSION_EMBRAYAGE = gettext_noop(
                    "Suppression du remplacement de l'embrayage"
                )

                UserLog.objects.create(
                    utilisateur=request.user,
                    action=f"{ACTION_SUPPRESSION_EMBRAYAGE} - {immatriculation}",
                )

            messages.success(request, _("Remplacement de l'embrayage supprimé avec succès."))

            return redirect(
                f"{reverse('embrayage:embrayage_list', kwargs={'exemplaire_id': exemplaire.id})}?deleted=1"
            )

        except Exception as err:
            messages.error(
                request,
                _("Erreur lors de la suppression : %(erreur)s") % {"erreur": str(err)}
            )

    return render(request, "embrayage/delete_embrayage.html", {
        "embrayage": embrayage,
        "exemplaire": exemplaire,
    })



def _sections_embrayage(form):

    def champs(mot):
        return [form[f.name] for f in form if mot in f.name]

    return [
        {"title": _("Kilométrage"), "icon": "icons/compteur.png", "fields": champs("kilo")},
        {"title": _("Disque d'embrayage"), "icon": "icons/disque-dembrayage.png", "fields": champs("disque_embrayage")},
        {"title": _("Plateau d'embrayage"), "icon": "icons/plateau-emb.png", "fields": champs("mecanisme_embrayage")},
        {"title": _("Butée d'embrayage"), "icon": "icons/butee-emb.png", "fields": champs("butee_embrayage")},
        {"title": _("Fourchette"), "icon": "icons/fourchette-emb.png", "fields": champs("fourchette_embrayage")},
        {"title": _("Guide de la butée d'embrayage"), "icon": "icons/guide-emb.png", "fields": champs("guide_butee")},
        {"title": _("Volant Moteur"), "icon": "icons/volant-mot.png", "fields": champs("volant_moteur")},
        {"title": _("Joint SPI vilebrequin"), "icon": "icons/joint-spi.png", "fields": champs("joint_spi_vilebrequin")},
        {"title": _("Joint SPI boite"), "icon": "icons/joint-spi.png", "fields": champs("joint_spi_boite")},
        {"title": _("Liquide de frein"), "icon": "icons/liquide_frein.png", "fields": champs("liquide_frein")},
        {"title": _("Etiquette"), "icon": "icons/tag.png", "fields": champs("tag")},
        {"title": _("Pays"), "icon": "icons/pays.png", "fields": champs("pays")},
        {"title": _("Remarques"), "icon": "icons/notes.png", "fields": champs("remarques")},
        {"title": _("Serrage des roues"), "icon": "icons/roue.png", "fields": champs("serrage")},
        {"title": _("Technicien"), "icon": "icons/mecanicien.png", "fields": champs("tech")},
        {"title": _("Taux horaire"), "icon": "icons/taux.png", "fields": champs("taux")},
    ]






@login_required
def embrayage_detail_pdf_view(request, pk):
    embrayage = get_object_or_404(
        Embrayage.objects.select_related(
            "maintenance",
            "maintenance__voiture_exemplaire",
            "maintenance__tech_technicien",
            "maintenance__tech_societe",
            "voiture_exemplaire",
            "tech_technicien",
            "tech_societe",
            "main_oeuvre",
        ),
        pk=pk,
    )

    # -------------------------
    # RAPPORT
    # -------------------------
    rapport = embrayage.generer_rapport_remplacement()

    # -------------------------
    # MAINTENANCE
    # -------------------------
    maintenance = getattr(
        embrayage,
        "maintenance",
        None,
    )

    vehicule = None
    technicien = None
    date_intervention = None

    if maintenance:
        vehicule = getattr(
            maintenance,
            "voiture_exemplaire",
            None,
        )

        technicien = getattr(
            maintenance,
            "tech_technicien",
            None,
        )

        date_intervention = getattr(
            maintenance,
            "date_intervention",
            None,
        )

    # -------------------------
    # FALLBACK SUR EMBRAYAGE
    # -------------------------
    if vehicule is None:
        vehicule = getattr(
            embrayage,
            "voiture_exemplaire",
            None,
        )

    if technicien is None:
        technicien = getattr(
            embrayage,
            "tech_technicien",
            None,
        )

    if date_intervention is None:
        date_intervention = getattr(
            embrayage,
            "date",
            None,
        )

    # -------------------------
    # IMMATRICULATION
    # -------------------------
    if vehicule:
        immatriculation = getattr(
            vehicule,
            "immatriculation",
            "sans_immatriculation",
        )
    else:
        immatriculation = getattr(
            embrayage,
            "immatriculation",
            "sans_immatriculation",
        )

    # -------------------------
    # TECHNICIEN
    # -------------------------
    nom_technicien = "technicien_inconnu"

    if technicien:
        prenom = getattr(
            technicien,
            "prenom",
            "",
        ) or ""

        nom = getattr(
            technicien,
            "nom",
            "",
        ) or ""

        nom_technicien = (
            f"{prenom} {nom}".strip()
            or getattr(
                technicien,
                "username",
                None,
            )
            or str(technicien)
        )

    # -------------------------
    # NOM DE FICHIER
    # -------------------------
    nom_technicien_fichier = (
        str(nom_technicien)
        .strip()
        .replace(" ", "_")
        .replace("/", "-")
        .replace("\\", "-")
        .replace(",", "")
    )

    immatriculation_fichier = (
        str(immatriculation)
        .strip()
        .replace(" ", "_")
        .replace("/", "-")
        .replace("\\", "-")
        .replace(",", "")
    )

    # -------------------------
    # TEMPLATE HTML
    # -------------------------
    html_string = render_to_string(
        "embrayage/embrayage_detail_pdf.html",
        {
            "embrayage": embrayage,
            "rapport": rapport,
            "maintenance": maintenance,
            "technicien": technicien,
            "date_intervention": date_intervention,
            "vehicule": vehicule,
            "immatriculation": immatriculation,
            "date_export": datetime.now(),
            "societe": getattr(
                request.user,
                "societe",
                None,
            ),
        },
        request=request,
    )

    # -------------------------
    # GÉNÉRATION PDF
    # -------------------------
    pdf = HTML(
        string=html_string,
        base_url=request.build_absolute_uri("/"),
    ).write_pdf()

    # =========================================================
    # IMMATRICULATION
    # =========================================================

    immatriculation = (
        embrayage.voiture_exemplaire.immatriculation
        if embrayage.voiture_exemplaire
        else "sans_immatriculation"
    )

    # =========================================================
    # TECHNICIEN
    # =========================================================

    technicien = (
            embrayage.tech_nom_technicien
            or "technicien_inconnu"
    )

    # Nettoyage pour le nom du fichier
    technicien = str(technicien).replace(" ", "_")
    immatriculation = str(immatriculation).replace(" ", "_")

    # =========================================================
    # DATE
    # =========================================================

    date_pdf = (
        embrayage.date.strftime("%Y-%m-%d")
        if embrayage.date
        else timezone.now().strftime("%Y-%m-%d")
    )

    # =========================================================
    # TITRE / NOM DU PDF
    # =========================================================

    nom_fichier = (
        f"{_('Embrayage')}_{technicien}_{immatriculation}_{date_pdf}.pdf"
    )

    response = HttpResponse(
        pdf,
        content_type="application/pdf",
    )

    response["Content-Disposition"] = (
        f'inline; filename="{nom_fichier}"'
    )

    return response