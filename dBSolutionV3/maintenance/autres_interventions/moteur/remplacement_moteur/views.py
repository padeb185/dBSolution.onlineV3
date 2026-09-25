from decimal import Decimal
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.db import models, transaction
from maindoeuvre.models import MainDoeuvre
from utilisateurs.models import UserLog
from django.contrib import messages
from maintenance.models import Maintenance
from .forms import RemplacementMoteurForm
from django.utils.translation import gettext_lazy as _, gettext_noop
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.db.models import Q, F
from .models import RemplacementMoteur
from voiture.voiture_exemplaire.models import VoitureExemplaire
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.translation import gettext as _
from weasyprint import HTML, pdf






@method_decorator([login_required, never_cache], name="dispatch")
class RemplacementMoteurListView(ListView):
    model = RemplacementMoteur
    template_name = "remplacement_moteur/remplacement_moteur_list.html"
    context_object_name = "remplacements"



    def get_queryset(self):
        queryset = RemplacementMoteur.objects.select_related(
            "voiture_exemplaire", "maintenance", "tech_societe"
        )

        societe = getattr(self.request.user, "societe", None)
        if societe:
            queryset = queryset.filter(
                models.Q(tech_societe=societe) | models.Q(tech_societe__isnull=True)
            )

        return queryset.order_by("-id")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        exemplaire_id = self.kwargs.get("exemplaire_id")
        if exemplaire_id:
            context["exemplaire"] = VoitureExemplaire.objects.get(id=exemplaire_id)

        roles_autorises = [
            "mecanicien",
            "apprenti",
            "magasinier",
            "chef_mecanicien",
            "direction",
        ]

        context["is_checkup_allowed"] = self.request.user.role in roles_autorises

        return context





@never_cache
@login_required
def remplacement_moteur_form_view(request, exemplaire_id):

    tenant = request.user.societe
    role = request.user.role

    exemplaire = get_object_or_404(
        VoitureExemplaire.objects.filter(
            Q(client__societe=tenant) | Q(client__isnull=True, societe=tenant)
        ),
        id=exemplaire_id
    )

    roles_autorises = ["mecanicien", "apprenti", "magasinier", "chef_mecanicien", "direction"]

    if role not in roles_autorises:
        messages.error(request, _("Accès refusé"))
        return redirect("utilisateurs:dashboard")

    remplacement_moteur = None

    # ==========================================================
    # POST
    # ==========================================================
    if request.method == "POST":

        form = RemplacementMoteurForm(request.POST, user=request.user, exemplaire=exemplaire)

        if form.is_valid():
            try:
                with transaction.atomic():

                    # ==================================================
                    # VALEURS AVANT INTERVENTION
                    # ==================================================
                    ancien_chassis = exemplaire.kilometres_chassis or 0
                    ancien_moteur = exemplaire.kilometres_moteur or 0
                    ancien_boite = exemplaire.kilometres_boite or 0
                    ancien_embrayage = exemplaire.kilometres_embrayage or 0

                    # ==================================================
                    # NOUVEAU KILOMÉTRAGE
                    # ==================================================
                    nouveau_km = form.cleaned_data.get("kilometres_remplacement")

                    if nouveau_km is None:
                        form.add_error("kilometres_remplacement", _("Le kilométrage du remplacement est obligatoire."))
                        raise ValidationError("km_obligatoire")

                    if nouveau_km < ancien_chassis:
                        form.add_error("kilometres_remplacement", _("Le kilométrage ne peut pas être inférieur au dernier kilométrage."))
                        raise ValidationError("km_inferieur")

                    variation = nouveau_km - ancien_chassis

                    # ==================================================
                    # EXEMPLAIRE
                    # ==================================================
                    exemplaire.kilometres_rollback = ancien_chassis
                    exemplaire.kilometres_moteur_rollback = ancien_moteur
                    exemplaire.kilometres_boite_rollback = ancien_boite
                    exemplaire.kilometres_embrayage_rollback = ancien_embrayage

                    exemplaire.date_derniere_intervention = timezone.localtime(timezone.now()).date()
                    exemplaire.kilometres_chassis = nouveau_km
                    exemplaire.kilometres_remplacement_moteur = nouveau_km  # moteur neuf → 0

                    exemplaire.update_kilometres()

                    exemplaire.save(update_fields=[
                        "kilometres_chassis",
                        "date_derniere_intervention",
                        "kilometres_rollback",
                        "kilometres_moteur_rollback",
                        "kilometres_boite_rollback",
                        "kilometres_embrayage_rollback",
                        "kilometres_remplacement_moteur",
                        "kilometres_moteur",
                        "kilometres_boite",
                        "kilometres_embrayage",
                        "variation_kilometres",
                    ])

                    # ==================================================
                    # MAINTENANCE
                    # ==================================================
                    maintenance = Maintenance.objects.create(
                        societe=request.user.societe,
                        voiture_exemplaire=exemplaire,
                        immatriculation=exemplaire.immatriculation,
                        date_intervention=timezone.now().date(),
                        kilometres_chassis=exemplaire.kilometres_chassis,
                        kilometres_dernier_entretien=exemplaire.kilometres_dernier_entretien,
                        type_maintenance=Maintenance.TypeMaintenance.REMPLACEMENT_MOTEUR,
                        tag=Maintenance.Tag.JAUNE,
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

                    # ==================================================
                    # REMPLACEMENT
                    # ==================================================
                    remplacement_moteur = form.save(commit=False)
                    remplacement_moteur.voiture_exemplaire = exemplaire
                    remplacement_moteur.maintenance = maintenance

                    # Kilométrages au moment de l'intervention
                    remplacement_moteur.kilometres_chassis = ancien_chassis
                    remplacement_moteur.kilometres_boite = ancien_boite
                    remplacement_moteur.kilometres_embrayage = ancien_embrayage
                    remplacement_moteur.kilometres_moteur = ancien_moteur + variation  # moteur déposé
                    remplacement_moteur.kilometres_remplacement = nouveau_km

                    # Sauvegardes pour la suppression (valeurs AVANT)
                    remplacement_moteur.kilometres_rollback = ancien_chassis
                    remplacement_moteur.kilometres_moteur_rollback = ancien_moteur
                    remplacement_moteur.kilometres_boite_rollback = ancien_boite
                    remplacement_moteur.kilometres_embrayage_rollback = ancien_embrayage

                    remplacement_moteur.assign_technicien(request.user)
                    remplacement_moteur.tech_last_maintained_by = request.user

                    # ==================================================
                    # MAIN-D'ŒUVRE
                    # ==================================================
                    heures = form.cleaned_data.get("temps_heures") or 0
                    minutes = form.cleaned_data.get("temps_minutes") or 0
                    total_minutes = heures * 60 + minutes
                    taux_horaire = form.cleaned_data.get("taux_horaire") or 0

                    if remplacement_moteur.main_oeuvre_id:
                        main_oeuvre = remplacement_moteur.main_oeuvre
                        main_oeuvre.temps_minutes = total_minutes
                        main_oeuvre.taux_horaire = taux_horaire
                        main_oeuvre.save(update_fields=["temps_minutes", "taux_horaire"])
                    else:
                        remplacement_moteur.main_oeuvre = MainDoeuvre.objects.create(
                            utilisateur=request.user,
                            temps_minutes=total_minutes,
                            taux_horaire=taux_horaire,
                        )

                    remplacement_moteur.save()
                    form.save_m2m()


                    # save() du modèle remet kilometres_moteur à 0 → on impose le moteur déposé
                    RemplacementMoteur.objects.filter(pk=remplacement_moteur.pk).update(
                        kilometres_moteur=ancien_moteur + variation
                    )

                    # ==================================================
                    # MOTEUR NEUF = 0 KM (écrit EN DERNIER)
                    # ==================================================
                    VoitureExemplaire.objects.filter(pk=exemplaire.pk).update(
                        kilometres_chassis=nouveau_km,
                        kilometres_remplacement_moteur=nouveau_km,
                        kilometres_moteur=0,
                    )

                    ACTION_REMPLACEMENT_MOTEUR = gettext_noop("Remplacement moteur")

                    UserLog.objects.create(
                        utilisateur=request.user,
                        action=f"{ACTION_REMPLACEMENT_MOTEUR} - {exemplaire.immatriculation}",
                    )

                messages.success(request, _("Remplacement du moteur enregistré avec succès"))

                return redirect(
                    f"{reverse('remplacement_moteur:remplacement_moteur_list', kwargs={'exemplaire_id': exemplaire.id})}?saved=1"
                )

            except ValidationError:
                messages.error(request, _("Veuillez corriger les erreurs du formulaire"))

            except Exception as e:
                messages.error(request, str(e))

        else:
            messages.error(request, _("Veuillez corriger les erreurs du formulaire"))

    # ==========================================================
    # GET
    # ==========================================================
    else:
        remplacement_moteur = RemplacementMoteur(
            voiture_exemplaire=exemplaire,
            kilometres_chassis=exemplaire.kilometres_chassis or 0,
            kilometres_moteur=exemplaire.kilometres_moteur or 0,
            kilometres_boite=exemplaire.kilometres_boite or 0,
            kilometres_embrayage=exemplaire.kilometres_embrayage or 0,
        )

        remplacement_moteur.assign_technicien(request.user)

        form = RemplacementMoteurForm(
            instance=remplacement_moteur,
            user=request.user,
            exemplaire=exemplaire,
        )

    return render(request, "remplacement_moteur/remplacement_moteur_form.html", {
        "remplacement_moteur": remplacement_moteur,
        "exemplaire": exemplaire,
        "form": form,
        "sections": _sections_moteur(form),
        "now": timezone.now(),
    })




@login_required
def remplacement_moteur_detail_view(request, remplacement_moteur_id):
    remplacement_moteur = get_object_or_404(
        RemplacementMoteur.objects.select_related("voiture_exemplaire"),
        id=remplacement_moteur_id
    )

    context = {
        "remplacement_moteur": remplacement_moteur,
        "exemplaire": remplacement_moteur.voiture_exemplaire,
    }
    return render(request, "remplacement_moteur/remplacement_moteur_detail.html", context)






@login_required
def modifier_remplacement_moteur_view(request, remplacement_moteur_id):

    tenant = request.user.societe

    remplacement_moteur = get_object_or_404(
        RemplacementMoteur.objects.select_related("voiture_exemplaire"),
        id=remplacement_moteur_id,
    )

    exemplaire = remplacement_moteur.voiture_exemplaire

    if exemplaire.client and exemplaire.client.societe != tenant:
        messages.error(request, _("Accès refusé"))
        return redirect("utilisateurs:dashboard")

    # ==========================================================
    # VALEURS ENREGISTRÉES (lues en base, avant le formulaire)
    # ==========================================================
    original = RemplacementMoteur.objects.get(pk=remplacement_moteur.pk)

    if original.kilometres_rollback:
        avant_chassis = original.kilometres_rollback
        avant_moteur = original.kilometres_moteur_rollback or 0
        avant_boite = original.kilometres_boite_rollback or 0
        avant_embrayage = original.kilometres_embrayage_rollback or 0
    else:
        # Ancien remplacement : les champs contiennent les valeurs d'avant
        avant_chassis = original.kilometres_chassis or 0
        avant_moteur = original.kilometres_moteur or 0
        avant_boite = original.kilometres_boite or 0
        avant_embrayage = original.kilometres_embrayage or 0

    ancien_km_remplacement = original.kilometres_remplacement or avant_chassis
    ancien_moteur_depose = original.kilometres_moteur or 0

    km_moteur_reference = avant_moteur  # utilisé par le template

    # ==========================================================
    # POST
    # ==========================================================
    if request.method == "POST":

        form = RemplacementMoteurForm(
            request.POST,
            instance=remplacement_moteur,
            user=request.user,
            exemplaire=exemplaire,
        )

        if form.is_valid():
            try:
                with transaction.atomic():

                    km = form.cleaned_data.get("kilometres_remplacement")
                    km = int(km) if km is not None else ancien_km_remplacement

                    if km < avant_chassis:
                        form.add_error(
                            "kilometres_remplacement",
                            _("Le kilométrage ne peut pas être inférieur à %(km)s km.") % {"km": avant_chassis},
                        )
                        raise ValidationError("km_inferieur")

                    # Un moteur plus récent a été monté depuis ?
                    est_dernier_moteur = (
                        (exemplaire.kilometres_remplacement_moteur or 0) == ancien_km_remplacement
                    )

                    if km != ancien_km_remplacement and not est_dernier_moteur:
                        form.add_error(
                            "kilometres_remplacement",
                            _("Seul le dernier remplacement du moteur peut voir son kilométrage modifié."),
                        )
                        raise ValidationError("pas_dernier")

                    variation = km - avant_chassis

                    # ==================================================
                    # MOTEUR DÉPOSÉ : valeur du formulaire,
                    # jamais inférieure à la valeur enregistrée
                    # ==================================================
                    moteur_form = form.cleaned_data.get("kilometres_moteur")

                    if moteur_form is None:
                        moteur_form = avant_moteur + variation

                    moteur_depose = max(int(moteur_form), ancien_moteur_depose)

                    # ==================================================
                    # REMPLACEMENT
                    # ==================================================
                    remplacement = form.save(commit=False)
                    remplacement.voiture_exemplaire = exemplaire

                    remplacement.kilometres_chassis = avant_chassis
                    remplacement.kilometres_boite = avant_boite
                    remplacement.kilometres_embrayage = avant_embrayage
                    remplacement.kilometres_moteur = moteur_depose
                    remplacement.kilometres_remplacement = km

                    # Les sauvegardes ne changent jamais en modification
                    remplacement.kilometres_rollback = original.kilometres_rollback
                    remplacement.kilometres_moteur_rollback = original.kilometres_moteur_rollback
                    remplacement.kilometres_boite_rollback = original.kilometres_boite_rollback
                    remplacement.kilometres_embrayage_rollback = original.kilometres_embrayage_rollback

                    remplacement.assign_technicien(request.user)
                    remplacement.tech_last_maintained_by = request.user

                    remplacement.save()
                    form.save_m2m()

                    RemplacementMoteur.objects.filter(pk=remplacement.pk).update(
                        kilometres_moteur=moteur_depose
                    )


                    # ==================================================
                    # EXEMPLAIRE (écrit EN DERNIER)
                    # ==================================================
                    if est_dernier_moteur:

                        chassis_actuel = exemplaire.kilometres_chassis or 0

                        # Rien n'a bougé depuis ce remplacement ?
                        if chassis_actuel == ancien_km_remplacement:
                            nouveau_chassis = km
                            nouvelle_boite = avant_boite + variation
                            nouvel_embrayage = avant_embrayage + variation
                        else:
                            nouveau_chassis = chassis_actuel
                            nouvelle_boite = exemplaire.kilometres_boite or 0
                            nouvel_embrayage = exemplaire.kilometres_embrayage or 0

                        VoitureExemplaire.objects.filter(pk=exemplaire.pk).update(
                            kilometres_chassis=nouveau_chassis,
                            kilometres_remplacement_moteur=km,
                            kilometres_moteur=max(0, nouveau_chassis - km),
                            kilometres_boite=nouvelle_boite,
                            kilometres_embrayage=nouvel_embrayage,
                            date_derniere_intervention=timezone.localtime(timezone.now()).date(),
                        )

                    ACTION_MODIFICATION_REMPLACEMENT_MOTEUR = gettext_noop(
                        "Modification du remplacement moteur"
                    )

                    UserLog.objects.create(
                        utilisateur=request.user,
                        action=f"{ACTION_MODIFICATION_REMPLACEMENT_MOTEUR} - {exemplaire.immatriculation}",
                    )

                messages.success(request, _("Remplacement du moteur modifié avec succès !"))

                return redirect(
                    f"{reverse('remplacement_moteur:remplacement_moteur_detail', kwargs={'remplacement_moteur_id': remplacement.id})}?saved=1"
                )

            except ValidationError:
                messages.error(request, _("Kilométrage invalide"))

        else:
            messages.error(request, _("Le formulaire contient des erreurs."))

    # ==========================================================
    # GET
    # ==========================================================
    else:
        form = RemplacementMoteurForm(
            instance=remplacement_moteur,
            user=request.user,
            exemplaire=exemplaire,
        )

    return render(request, "remplacement_moteur/modifier_remplacement_moteur.html", {
        "remplacement_moteur": remplacement_moteur,
        "form": form,
        "sections": _sections_moteur(form),
        "exemplaire": exemplaire,
        "km_moteur_reference": km_moteur_reference,
    })




@never_cache
@login_required
def delete_moteur_view(request, remplacement_moteur_id):

    tenant = request.user.societe
    role = request.user.role

    roles_autorises = ["direction", "chef_mecanicien"]

    if role not in roles_autorises and not request.user.is_superuser:
        messages.error(request, _("Accès refusé"))
        return redirect("utilisateurs:dashboard")

    remplacement_moteur = get_object_or_404(
        RemplacementMoteur.objects.select_related("voiture_exemplaire", "maintenance"),
        id=remplacement_moteur_id,
    )

    exemplaire = remplacement_moteur.voiture_exemplaire
    maintenance = remplacement_moteur.maintenance

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
                r = remplacement_moteur

                # ------------------------------------------
                # Valeurs AVANT intervention
                # ------------------------------------------
                if r.kilometres_rollback:
                    km_chassis = r.kilometres_rollback
                    km_moteur = r.kilometres_moteur_rollback or 0
                    km_boite = r.kilometres_boite_rollback or 0
                    km_embrayage = r.kilometres_embrayage_rollback or 0
                else:
                    km_chassis = r.kilometres_chassis or 0
                    km_moteur = r.kilometres_moteur or 0
                    km_boite = r.kilometres_boite or 0
                    km_embrayage = r.kilometres_embrayage or 0

                km_remplacement = r.kilometres_remplacement or 0
                ancien_point_moteur = max(0, km_chassis - km_moteur)

                # Ce remplacement est-il le moteur actuellement monté ?
                est_dernier_moteur = (
                    (exemplaire.kilometres_remplacement_moteur or 0) == km_remplacement
                )

                # Le châssis a-t-il bougé depuis (autre intervention) ?
                chassis_actuel = exemplaire.kilometres_chassis or 0
                rien_depuis = chassis_actuel == km_remplacement

                if est_dernier_moteur and rien_depuis:
                    # Retour exact à l'état d'avant le remplacement
                    VoitureExemplaire.objects.filter(pk=exemplaire.pk).update(
                        kilometres_chassis=km_chassis,
                        kilometres_moteur=km_moteur,
                        kilometres_boite=km_boite,
                        kilometres_embrayage=km_embrayage,
                        kilometres_remplacement_moteur=ancien_point_moteur,
                    )

                elif est_dernier_moteur:
                    # D'autres interventions depuis : on garde le châssis,
                    # on annule seulement le changement de moteur
                    VoitureExemplaire.objects.filter(pk=exemplaire.pk).update(
                        kilometres_remplacement_moteur=ancien_point_moteur,
                        kilometres_moteur=max(0, chassis_actuel - ancien_point_moteur),
                    )

                # Sinon : un moteur plus récent est monté → on ne touche à rien

                remplacement_moteur.delete()

                if maintenance:
                    maintenance.delete()

                ACTION_SUPPRESSION_MOTEUR = gettext_noop("Suppression du remplacement moteur")

                UserLog.objects.create(
                    utilisateur=request.user,
                    action=f"{ACTION_SUPPRESSION_MOTEUR} - {immatriculation}",
                )

            messages.success(request, _("Remplacement moteur supprimé avec succès."))

            return redirect(
                f"{reverse('remplacement_moteur:remplacement_moteur_list', kwargs={'exemplaire_id': exemplaire.id})}?deleted=1"
            )

        except Exception as e:
            messages.error(
                request,
                _("Erreur lors de la suppression : %(erreur)s") % {"erreur": str(e)}
            )

    return render(request, "remplacement_moteur/delete_remplacement_moteur.html", {
        "remplacement_moteur": remplacement_moteur,
        "exemplaire": exemplaire,
    })





def _sections_moteur(form):

    def champs(mot):
        return [form[f.name] for f in form if mot in f.name]

    return [
        {"title": _("Kilométrage"), "icon": "icons/compteur.png", "fields": champs("kilometres")},
        {"title": _("Remplacement du moteur"), "icon": "icons/engine.png", "fields": champs("moteurs")},
        {"title": _("Huile moteur"), "icon": "icons/huile-moteur.png", "fields": champs("niveau")},
        {"title": _("Liquide de refroidissement"), "icon": "icons/anti-gel.png", "fields": champs("refroidissement")},
        {"title": _("Remise à Zéro des kilomètres moteurs"), "icon": "icons/km.png", "fields": champs("remplacement_effectue")},
        {"title": _("Etiquette"), "icon": "icons/tag.png", "fields": champs("tag")},
        {"title": _("Pays"), "icon": "icons/pays.png", "fields": champs("pays")},
        {"title": _("Remarques"), "icon": "icons/notes.png", "fields": champs("remarques")},
        {"title": _("Serrage des roues"), "icon": "icons/roue.png", "fields": champs("serrage")},
        {"title": _("Technicien"), "icon": "icons/mecanicien.png", "fields": champs("tech")},
        {"title": _("Taux horaire"), "icon": "icons/taux.png", "fields": champs("taux")},
    ]




@login_required
def remplacement_moteur_pdf_view(request, remplacement_moteur_id):
    tenant = request.user.societe


    remplacement = get_object_or_404(
        RemplacementMoteur.objects.select_related(
            "voiture_exemplaire",
            "voiture_exemplaire__voiture_marque",
            "voiture_exemplaire__voiture_modele",
            "maintenance",
            "tech_technicien",
            "tech_societe",
            "main_oeuvre",
            "main_oeuvre__utilisateur",
        ),
        pk=remplacement_moteur_id,
    )

    # Rapport des pièces et produits
    rapport = remplacement.generer_rapport_remplacement()

    lignes_rapport = rapport.get("lignes", [])
    total_pieces_produits = rapport.get(
        "total_general",
        Decimal("0.00"),
    )

    # Main-d'œuvre
    cout_main_oeuvre = remplacement.cout_main_oeuvre
    total_general = remplacement.total_general_avec_main_oeuvre

    html_string = render_to_string(
        "remplacement_moteur/remplacement_moteur_pdf.html",
        {
            "remplacement": remplacement,
            "rapport": rapport,
            "lignes_rapport": lignes_rapport,

            # Compatibilité avec les templates utilisant pieces_utilisees
            "pieces_utilisees": lignes_rapport,

            "total_pieces": total_pieces_produits,
            "total_pieces_produits": total_pieces_produits,
            "cout_main_oeuvre": cout_main_oeuvre,
            "total_general": total_general,

            "maintenance": remplacement.maintenance,
            "vehicule": remplacement.voiture_exemplaire,
            "societe": tenant,
            "date_export": timezone.now(),
        },
        request=request,
    )

    pdf = HTML(
        string=html_string,
        base_url=request.build_absolute_uri("/"),
    ).write_pdf()

    vehicule = remplacement.voiture_exemplaire

    # =========================================================
    # IMMATRICULATION
    # =========================================================

    immatriculation = (
        remplacement.voiture_exemplaire.immatriculation
        if remplacement.voiture_exemplaire
        else "sans_immatriculation"
    )

    # =========================================================
    # TECHNICIEN
    # =========================================================

    technicien = (
            remplacement.tech_nom_technicien
            or "technicien_inconnu"
    )

    # Nettoyage pour le nom du fichier
    technicien = str(technicien).replace(" ", "_")
    immatriculation = str(immatriculation).replace(" ", "_")

    # =========================================================
    # DATE
    # =========================================================

    date_pdf = (
        remplacement.date.strftime("%Y-%m-%d")
        if remplacement.date
        else timezone.now().strftime("%Y-%m-%d")
    )

    # =========================================================
    # TITRE / NOM DU PDF
    # =========================================================

    nom_fichier = (
        f"{_('Remplacement moteur')}_{technicien}_{immatriculation}_{date_pdf}.pdf"
    )

    response = HttpResponse(
        pdf,
        content_type="application/pdf",
    )

    response["Content-Disposition"] = (
        f'inline; filename="{nom_fichier}"'
    )

    return response
