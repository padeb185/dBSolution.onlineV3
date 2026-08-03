from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.db import transaction, models
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import ListView
from maintenance.autres_interventions.moteur.rodage.forms import RodageForm
from maintenance.autres_interventions.moteur.rodage.models import Rodage
from maintenance.models import Maintenance
from utilisateurs.models import UserLog
from voiture.voiture_exemplaire.models import VoitureExemplaire
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
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
@method_decorator([login_required, never_cache], name='dispatch')
class RodageListView(ListView):
    model = Rodage
    template_name = "rodage/rodage_list.html"
    context_object_name = "rodages"
    ordering = ["-id"]

    def get_queryset(self):
        queryset = Rodage.objects.select_related(
            "voiture_exemplaire", "maintenance", "tech_societe"
        )

        # Filtrer par société : inclure les objets NULL ou ceux de la société de l'utilisateur
        societe = getattr(self.request.user, "societe", None)
        if societe:
            queryset = queryset.filter(
                models.Q(tech_societe=societe) | models.Q(tech_societe__isnull=True)
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
def rodage_check_view(request, exemplaire_id):

    tenant = request.user.societe
    role = request.user.role

    # 🔎 Récupération exemplaire
    exemplaire = get_object_or_404(
        VoitureExemplaire.objects.filter(
            Q(client__societe=tenant) |
            Q(client__isnull=True, societe=tenant)
        ),
        id=exemplaire_id
    )

    # 🔐 Vérification rôles
    roles_autorises = [
        "mecanicien",
        "apprenti",
        "magasinier",
        "chef_mecanicien",
        "direction"
    ]

    if role not in roles_autorises:
        messages.error(request, _("Accès refusé"))
        return redirect("utilisateurs:dashboard")

    # =========================
    # POST
    # =========================

    maintenance = None

    if request.method == "POST":

        form = RodageForm(
            request.POST,
            user=request.user,
            exemplaire=exemplaire
        )

        if form.is_valid():

            try:
                with transaction.atomic():
                    km = form.cleaned_data.get("kilometres_rodage")

                    if km is not None:
                        km = int(km)

                        ancien_km = exemplaire.kilometres_chassis or 0

                        if km < ancien_km:
                            form.add_error(
                                "kilometres_rodage",
                                _("Le kilométrage ne peut pas diminuer.")
                            )
                            raise ValueError("Kilométrage invalide")

                        # 🚗 source unique = voiture
                        exemplaire.kilometres_chassis = km
                        exemplaire.kilometres_dernier_entretien = km
                        exemplaire.date_derniere_intervention = timezone.now().date()

                        exemplaire.update_kilometres()

                        exemplaire.save(
                            update_fields=[
                                "kilometres_chassis",
                                "kilometres_dernier_entretien",
                                "date_derniere_intervention",
                            ]
                        )

                    # 🔗 entretien
                    rodage = form.save(commit=False)

                    rodage.assign_technicien(request.user)

                    rodage.kilometres_chassis = exemplaire.kilometres_chassis
                    rodage.kilometrage_rodage = km


                    # 🔴 Création maintenance UNIQUE
                    maintenance = Maintenance.objects.create(
                        societe=request.user.societe,
                        voiture_exemplaire=exemplaire,
                        immatriculation=exemplaire.immatriculation,
                        date_intervention=timezone.now().date(),
                        kilometres_chassis=exemplaire.kilometres_chassis,
                        kilometres_dernier_entretien=exemplaire.kilometres_dernier_entretien,
                        type_maintenance=Maintenance.TypeMaintenance.RODAGE,
                        tag=Maintenance.Tag.JAUNE,
                    )

                    # 🔧 Affectation rôle
                    if role == "mecanicien":
                        maintenance.mecanicien = Mecanicien.objects.get(id=request.user.id)

                    elif role == "chef_mecanicien":
                        maintenance.chef_mecanicien = ChefMecanicien.objects.get(id=request.user.id)

                    elif role == "apprenti":
                        maintenance.apprentis = Apprenti.objects.get(id=request.user.id)

                    elif role == "magasinier":
                        maintenance.magasinier = Magasinier.objects.get(id=request.user.id)

                    elif role == 'direction':
                        maintenance.direction = Direction.objects.get(id=request.user.id)

                    maintenance.save()

                rodage.maintenance = maintenance
                rodage.save()

                UserLog.objects.create(
                    utilisateur=request.user,
                    action=_("Rodage - %(immatriculation)s") % {
                        "immatriculation": exemplaire.immatriculation
                    }
                )

                messages.success(request, _("Rodage enregistré avec succès."))
                return redirect("rodage:rodage_list", exemplaire_id=exemplaire.id)

            except Exception as e:
                messages.error(request, _(f"Erreur lors de l'enregistrement : {str(e)}"))
        else:
            print("FORM INVALID:", form.errors)
            messages.error(request, _("Le formulaire contient des erreurs."))



    else:
        rodage = Rodage(
            societe=tenant,
            voiture_exemplaire=exemplaire,
            kilometres_chassis=exemplaire.kilometres_chassis

        )

        rodage.assign_technicien(request.user)

        form = RodageForm(
            instance=rodage,
            user=request.user,
            exemplaire=exemplaire

        )


    return render(request, 'rodage/rodage_check.html', {
        "exemplaire": exemplaire,
        "immatriculation": exemplaire.immatriculation,
        "maintenance": maintenance,
        "form": form,
        "now": timezone.now(),
    })



# ------------
# Vue détail entretien
# -----------------------------
@never_cache
@login_required
def rodage_detail_view(request, rodage_id):
    tenant = request.user.societe

    rodage = get_object_or_404(
        Rodage.objects.select_related("voiture_exemplaire"),
        id=rodage_id
    )

    context = {
        "rodage": rodage,
        "exemplaire": rodage.voiture_exemplaire,
    }
    return render(request, "rodage/rodage_detail.html", context)


#---------------------

# Modifier rodage

#---------------------

@login_required
def modifier_rodage_view(request, rodage_id):
    tenant = request.user.societe

    # Récupération de l'entretien avec son exemplaire
    rodage = get_object_or_404(
        Rodage.objects.select_related("voiture_exemplaire"),
        id=rodage_id
    )

    exemplaire = rodage.voiture_exemplaire

    # -------------------------
    # POST
    # -------------------------
    if request.method == "POST":
        form = RodageForm(
            request.POST,
            instance=rodage,
            user=request.user,
            exemplaire=rodage.voiture_exemplaire
        )
        if form.is_valid():
            form.save()

            UserLog.objects.create(
                utilisateur=request.user,
                action=_("Modification rodage - %(immatriculation)s") % {
                    "immatriculation": exemplaire.immatriculation
                }
            )

            messages.success(request, _("rodage modifié avec succès !"))
            return redirect("rodage:rodage_detail", rodage_id=rodage.id)
        else:
            messages.error(request, _("Le formulaire contient des erreurs."))
            print(form.errors)

    # -------------------------
    # GET
    # -------------------------
    else:
        form = RodageForm(
            instance=rodage,
            user=request.user,
            exemplaire=rodage.voiture_exemplaire
        )

    return render(
        request,
        "rodage/modifier_rodage.html",
        {
            "form": form,
            "rodage": rodage,
            "exemplaire": rodage.voiture_exemplaire,
        }
    )




@login_required
def rodage_pdf_view(request, rodage_id):
    tenant = request.user.societe

    rodage = get_object_or_404(
        Rodage.objects.select_related(
            "voiture_exemplaire",
            "tech_technicien",
            "tech_societe",
            "main_oeuvre",
            "piece",
        ),
        id=rodage_id
    )

    # Génération du rapport des pièces et produits
    rapport = rodage.generer_rapport_remplacement() or {
        "lignes": [],
        "total_general": 0,
    }


    html_string = render_to_string(
        "rodage/rodage_pdf.html",
        {
            "rodage": rodage,
            "rapport": rapport,
            "date_export": timezone.now(),
            "societe": tenant,
        }
    )

    pdf = HTML(
        string=html_string,
        base_url=request.build_absolute_uri("/")
    ).write_pdf()

    immatriculation = (
        rodage.voiture_exemplaire.immatriculation
        if rodage.voiture_exemplaire
        else "sans_immatriculation"
    )

    technicien = (
        rodage.tech_nom_technicien
        or "technicien_inconnu"
    )

    response = HttpResponse(
        pdf,
        content_type="application/pdf"
    )

    response["Content-Disposition"] = (
        f'inline; filename="rodage_'
        f'{immatriculation}_{technicien}.pdf"'
    )

    return response