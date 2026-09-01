from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.db import transaction, models
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import ListView
from maintenance.models import Maintenance
from utilisateurs.models import UserLog
from voiture.voiture_exemplaire.models import VoitureExemplaire
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from maintenance.entretien.models import Entretien
from maintenance.entretien.forms import EntretienForm
from utilisateurs.apprentis.models import Apprenti
from utilisateurs.chef_mecanicien.models import ChefMecanicien
from utilisateurs.direction.models import Direction
from utilisateurs.magasinier.models import Magasinier
from utilisateurs.mecanicien.models import Mecanicien
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML



# -----------------------------
# Classe ListView pour entretien
# -----------------------------
@method_decorator([login_required, never_cache], name="dispatch")
class EntretienListView(ListView):
    model = Entretien
    template_name = "entretien/entretien_list.html"
    context_object_name = "entretiens"
    ordering = ["-id"]

    def get_queryset(self):
        queryset = Entretien.objects.select_related(
            "voiture_exemplaire",
            "maintenance",
            "tech_societe",
        )

        societe = getattr(self.request.user, "societe", None)

        if societe:
            queryset = queryset.filter(
                models.Q(tech_societe=societe) |
                models.Q(tech_societe__isnull=True)
            )

        return queryset.order_by(*self.ordering)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        exemplaire_id = self.kwargs.get("exemplaire_id")

        context["exemplaire"] = get_object_or_404(
            VoitureExemplaire,
            id=exemplaire_id
        )

        context["is_checkup_allowed"] = self.request.user.role in [
            "direction",
            "mecanicien",
            "chef_mecanicien",
            "magasinier",
        ]

        return context



#----------------------------
# creation entretien
#----------------------------

@never_cache
@login_required
def entretien_check_view(request, exemplaire_id):

    tenant = request.user.societe
    role = request.user.role

    # =========================
    # VÉHICULE
    # =========================
    exemplaire = get_object_or_404(
        VoitureExemplaire.objects.filter(
            Q(client__societe=tenant) |
            Q(client__isnull=True, societe=tenant)
        ),
        id=exemplaire_id
    )

    # =========================
    # RÔLES
    # =========================
    roles_autorises = [
        "mecanicien",
        "apprenti",
        "magasinier",
        "chef_mecanicien",
        "direction",
    ]

    if role not in roles_autorises:
        messages.error(request, _("Accès refusé"))
        return redirect("utilisateurs:dashboard")

    maintenance = None

    # =========================
    # POST
    # =========================
    if request.method == "POST":

        form = EntretienForm(
            request.POST,
            user=request.user,
            exemplaire=exemplaire,
        )

        if form.is_valid():

            km = form.cleaned_data.get("kilometrage_entretien")

            ancien_kilometrage = (
                exemplaire.kilometres_chassis or 0
            )

            # =========================
            # VALIDATION KM
            # =========================
            if km is not None:

                km = int(km)

                if km < ancien_kilometrage:

                    form.add_error(
                        "kilometrage_entretien",
                        _("Le kilométrage ne peut pas diminuer.")
                    )

                    messages.error(
                        request,
                        _("Le kilométrage ne peut pas diminuer.")
                    )

                    return render(
                        request,
                        "entretien/entretien_check.html",
                        {
                            "exemplaire": exemplaire,
                            "immatriculation": exemplaire.immatriculation,
                            "maintenance": maintenance,
                            "form": form,
                            "now": timezone.now(),
                        }
                    )

            try:

                with transaction.atomic():

                    # =========================
                    # VARIATION
                    # =========================
                    kilometrage_variation = 0

                    if km is not None:
                        kilometrage_variation = (
                            km - ancien_kilometrage
                        )

                    # =========================
                    # ENTRETIEN
                    # =========================
                    entretien = form.save(commit=False)

                    entretien.societe = tenant
                    entretien.voiture_exemplaire = exemplaire

                    entretien.kilometres_chassis = (
                        ancien_kilometrage
                    )

                    entretien.kilometrage_entretien = km

                    entretien.kilometrage_variation = (
                        kilometrage_variation
                    )

                    entretien.assign_technicien(request.user)

                    # =========================
                    # VÉHICULE
                    # =========================
                    if km is not None:

                        exemplaire.kilometres_chassis = km

                        exemplaire.date_derniere_intervention = (
                            timezone.now().date()
                        )

                        exemplaire.update_kilometres()

                        exemplaire.save()

                    # =========================
                    # MAINTENANCE
                    # =========================
                    maintenance = Maintenance(
                        societe=tenant,
                        voiture_exemplaire=exemplaire,
                        immatriculation=exemplaire.immatriculation,
                        date_intervention=timezone.now().date(),

                        kilometres_chassis=(
                            exemplaire.kilometres_chassis
                        ),

                        kilometres_dernier_entretien=(
                            exemplaire.kilometres_dernier_entretien
                        ),

                        type_maintenance=(
                            Maintenance.TypeMaintenance.ENTRETIEN
                        ),

                        tag=Maintenance.Tag.JAUNE,
                    )

                    # =========================
                    # AFFECTATION UTILISATEUR
                    # =========================
                    #
                    # IMPORTANT :
                    # ne pas utiliser systématiquement
                    # Mecanicien.objects.get(id=request.user.id)
                    #
                    # Si tes modèles ont un lien `utilisateur`,
                    # utilise plutôt celui-ci.
                    #

                    # =========================
                    # AFFECTATION DU RÔLE
                    # =========================

                    if role == "mecanicien":
                        maintenance.mecanicien = Mecanicien.objects.filter(
                            pk=request.user.pk
                        ).first()

                    elif role == "chef_mecanicien":
                        maintenance.chef_mecanicien = ChefMecanicien.objects.filter(
                            pk=request.user.pk
                        ).first()

                    elif role == "apprenti":
                        maintenance.apprentis = Apprenti.objects.filter(
                            pk=request.user.pk
                        ).first()

                    elif role == "magasinier":
                        maintenance.magasinier = Magasinier.objects.filter(
                            pk=request.user.pk
                        ).first()

                    elif role == "direction":
                        maintenance.direction = Direction.objects.filter(
                            pk=request.user.pk
                        ).first()

                    maintenance.save()

                    # =========================
                    # LIEN ENTRETIEN / MAINTENANCE
                    # =========================
                    entretien.maintenance = maintenance

                    # Sauvegarde entretien
                    entretien.save()

                    # =========================
                    # MANY TO MANY
                    # =========================
                    form.instance = entretien
                    form.save_m2m()

                    # =========================
                    # LOG
                    # =========================
                    UserLog.objects.create(
                        utilisateur=request.user,
                        action=_(
                            "Entretien") + f" - {exemplaire.immatriculation}"
                    )

                # =========================
                # SUCCÈS
                # =========================
                messages.success(
                    request,
                    _("Entretien enregistré avec succès.")
                )

                return redirect(
                    "entretien:entretien_list",
                    exemplaire_id=exemplaire.id
                )

            except Exception as e:

                # TEMPORAIRE POUR DEBUG
                import traceback
                traceback.print_exc()

                messages.error(
                    request,
                    _("Erreur lors de l'enregistrement : %(erreur)s") % {
                        "erreur": str(e)
                    }
                )

        else:
            messages.error(
                request,
                _("Le formulaire contient des erreurs.")
            )

    # =========================
    # GET
    # =========================
    else:

        entretien = Entretien(
            societe=tenant,
            voiture_exemplaire=exemplaire,
            kilometres_chassis=exemplaire.kilometres_chassis,
            kilometrage_variation=0,
        )

        entretien.assign_technicien(request.user)

        form = EntretienForm(
            instance=entretien,
            user=request.user,
            exemplaire=exemplaire,
        )

    # =========================
    # TEMPLATE
    # =========================
    return render(
        request,
        "entretien/entretien_check.html",
        {
            "exemplaire": exemplaire,
            "immatriculation": exemplaire.immatriculation,
            "maintenance": maintenance,
            "form": form,
            "now": timezone.now(),
        }
    )


# ------------
# Vue détail entretien
# -----------------------------
@never_cache
@login_required
def entretien_detail_view(request, entretien_id):
    tenant = request.user.societe

    entretien = get_object_or_404(
        Entretien.objects.select_related("voiture_exemplaire"),
        id=entretien_id
    )

    context = {
        "entretien": entretien,
        "exemplaire": entretien.voiture_exemplaire,
    }
    return render(request, "entretien/entretien_detail.html", context)


#---------------------

# Modifier entretien

#---------------------
@never_cache
@login_required
def modifier_entretien_view(request, entretien_id):

    tenant = request.user.societe

    # =========================
    # RÉCUPÉRATION ENTRETIEN
    # =========================
    entretien = get_object_or_404(
        Entretien.objects.select_related(
            "voiture_exemplaire",
            "maintenance",
            "tech_societe",
            "tech_technicien",
        ),
        id=entretien_id,
    )

    # =========================
    # VÉHICULE
    # =========================
    exemplaire = get_object_or_404(
        VoitureExemplaire.objects.filter(
            Q(client__societe=tenant) |
            Q(client__isnull=True, societe=tenant)
        ),
        id=entretien.voiture_exemplaire_id
    )

    # =========================
    # KILOMÉTRAGE DE RÉFÉRENCE
    # =========================
    # Kilométrage historique avant cet entretien
    km_reference = entretien.kilometres_chassis or 0

    # =========================
    # POST
    # =========================
    if request.method == "POST":

        form = EntretienForm(
            request.POST,
            instance=entretien,
            user=request.user,
            exemplaire=exemplaire,
        )

        if form.is_valid():

            km_entretien = form.cleaned_data.get(
                "kilometrage_entretien"
            )

            if km_entretien is not None:
                km_entretien = int(km_entretien)

            # =========================
            # VALIDATION KILOMÉTRAGE
            # =========================
            if (
                km_entretien is not None
                and km_entretien < km_reference
            ):

                form.add_error(
                    "kilometrage_entretien",
                    _(
                        "Le kilométrage de l'entretien "
                        "ne peut pas être inférieur à "
                        "%(km)s km."
                    ) % {
                        "km": km_reference
                    }
                )

                messages.error(
                    request,
                    _("Le kilométrage ne peut pas diminuer.")
                )

            else:

                try:

                    with transaction.atomic():

                        # =========================
                        # ENTRETIEN
                        # =========================
                        entretien_modifie = form.save(
                            commit=False
                        )

                        # Conserver les relations
                        entretien_modifie.voiture_exemplaire = (
                            exemplaire
                        )

                        # On peut corriger la société
                        # pour les anciens entretiens
                        entretien_modifie.societe = tenant

                        # =========================
                        # KILOMÉTRAGE HISTORIQUE
                        # =========================
                        entretien_modifie.kilometres_chassis = (
                            km_reference
                        )

                        entretien_modifie.kilometrage_entretien = (
                            km_entretien
                        )

                        # =========================
                        # VARIATION
                        # =========================
                        if km_entretien is not None:

                            entretien_modifie.kilometrage_variation = (
                                km_entretien - km_reference
                            )

                        else:

                            entretien_modifie.kilometrage_variation = 0

                        # =========================
                        # TECHNICIEN
                        # =========================
                        entretien_modifie.assign_technicien(
                            request.user
                        )

                        # =========================
                        # SAUVEGARDE ENTRETIEN
                        # =========================
                        entretien_modifie.save()

                        form.save_m2m()

                        # =========================
                        # MISE À JOUR DU VÉHICULE
                        # =========================
                        kilometrage_actuel = (
                            exemplaire.kilometres_chassis or 0
                        )

                        # Ne jamais diminuer le kilométrage
                        # actuel du véhicule.
                        if (
                            km_entretien is not None
                            and km_entretien > kilometrage_actuel
                        ):

                            exemplaire.kilometres_chassis = (
                                km_entretien
                            )

                            exemplaire.date_derniere_intervention = (
                                timezone.now().date()
                            )

                            exemplaire.update_kilometres()

                            exemplaire.save()

                        # =========================
                        # MAINTENANCE ASSOCIÉE
                        # =========================
                        maintenance = entretien_modifie.maintenance

                        if maintenance:

                            maintenance_km = (
                                maintenance.kilometres_chassis or 0
                            )

                            if (
                                km_entretien is not None
                                and km_entretien > maintenance_km
                            ):

                                maintenance.kilometres_chassis = (
                                    km_entretien
                                )

                                maintenance.save(
                                    update_fields=[
                                        "kilometres_chassis"
                                    ]
                                )

                        # =========================
                        # LOG
                        # =========================
                        UserLog.objects.create(
                            utilisateur=request.user,
                            action=_(
                                "Modification de l'entretien") + f" - {exemplaire.immatriculation}"
                        )

                    # =========================
                    # SUCCÈS
                    # =========================
                    messages.success(
                        request,
                        _("Entretien modifié avec succès !")
                    )

                    return redirect(
                        "entretien:entretien_detail",
                        entretien_id=entretien_modifie.id
                    )

                except Exception as e:

                    import traceback
                    traceback.print_exc()

                    messages.error(
                        request,
                        _(
                            "Erreur lors de la modification : "
                            "%(erreur)s"
                        ) % {
                            "erreur": str(e)
                        }
                    )

        else:

            messages.error(
                request,
                _("Le formulaire contient des erreurs.")
            )

    # =========================
    # GET
    # =========================
    else:

        form = EntretienForm(
            instance=entretien,
            user=request.user,
            exemplaire=exemplaire,
        )

    # =========================
    # TEMPLATE
    # =========================
    return render(
        request,
        "entretien/modifier_entretien.html",
        {
            "form": form,
            "entretien": entretien,
            "exemplaire": exemplaire,
            "km_reference": km_reference,
        }
    )




@login_required
def entretien_pdf_view(request, entretien_id):
    tenant = request.user.societe

    entretien = get_object_or_404(
        Entretien.objects.select_related(
            "voiture_exemplaire",
            "tech_technicien",
            "tech_societe",
            "main_oeuvre",
            "piece",
        ),
        id=entretien_id
    )

    rapport = entretien.generer_rapport_remplacement()

    html_string = render_to_string(
        "entretien/entretien_detail_pdf.html",
        {
            "entretien": entretien,
            "objet": entretien,
            "rapport": rapport,
            "pieces_utilisees": rapport.get("lignes", []),
            "total_pieces": rapport.get("total_general", 0),
            "date_export": timezone.now(),
            "societe": tenant,
        },
        request=request,
    )

    pdf = HTML(
        string=html_string,
        base_url=request.build_absolute_uri("/")
    ).write_pdf()

    # =========================================================
    # IMMATRICULATION
    # =========================================================

    immatriculation = (
        entretien.voiture_exemplaire.immatriculation
        if entretien.voiture_exemplaire
        else "sans_immatriculation"
    )

    # =========================================================
    # TECHNICIEN
    # =========================================================

    technicien = (
        entretien.tech_nom_technicien
        or "technicien_inconnu"
    )

    # Nettoyage pour le nom du fichier
    technicien = str(technicien).replace(" ", "_")
    immatriculation = str(immatriculation).replace(" ", "_")

    # =========================================================
    # DATE
    # =========================================================

    date_pdf = (
        entretien.date.strftime("%Y-%m-%d")
        if entretien.date
        else timezone.now().strftime("%Y-%m-%d")
    )

    # =========================================================
    # TITRE / NOM DU PDF
    # =========================================================

    nom_fichier = (
        f"Entretien_{technicien}_{immatriculation}_{date_pdf}.pdf"
    )

    response = HttpResponse(
        pdf,
        content_type="application/pdf",
    )

    response["Content-Disposition"] = (
        f'inline; filename="{nom_fichier}"'
    )

    return response