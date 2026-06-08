from django.shortcuts import redirect, render
from django.contrib import messages
from django.db import transaction, models
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import ListView
from maintenance.models import Maintenance
from maintenance.jeux_pieces.models import ControleJeuxPieces
from maintenance.jeux_pieces.forms import ControleJeuxPiecesForm
from utilisateurs.models import UserLog
from voiture.voiture_exemplaire.models import VoitureExemplaire
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponse
from django_tenants.utils import tenant_context
from django.utils import timezone
from weasyprint import HTML



# -----------------------------
# Classe ListView pour checkup
# -----------------------------
@method_decorator([login_required, never_cache], name='dispatch')
class JeuListView(ListView):
    model = ControleJeuxPieces
    template_name = "jeux_pieces/jeux_pieces_list.html"
    context_object_name = "jeux_pieces"
    ordering = ["-id"]

    def get_queryset(self):
        queryset = ControleJeuxPieces.objects.select_related(
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







@never_cache
@login_required
def controle_jeux_pieces_view(request, exemplaire_id):

    tenant = request.user.societe
    role = request.user.role

    maintenance = None  # 👈 important pour éviter UnboundLocalError

    with tenant_context(tenant):

        # 🔎 Récupération exemplaire
        exemplaire = get_object_or_404(
            VoitureExemplaire.objects.filter(
                Q(client__societe=tenant) |
                Q(client__isnull=True, societe=tenant)
            ),
            id=exemplaire_id
        )

        # 🔐 rôles autorisés
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
        if request.method == "POST":

            form = ControleJeuxPiecesForm(
                request.POST,
                user=request.user,
                exemplaire=exemplaire
            )

            if form.is_valid():

                try:
                    with transaction.atomic():

                        km = form.cleaned_data.get("kilometrage_jeu")

                        if km is not None:
                            km = int(km)

                            ancien_km = exemplaire.kilometres_chassis

                            if km < ancien_km:
                                form.add_error(
                                    "kilometrage_jeu",
                                    _("Le kilométrage ne peut pas diminuer.")
                                )
                                raise ValueError("Kilométrage invalide")

                            # 🚗 update voiture (source unique)
                            exemplaire.kilometres_chassis = km
                            exemplaire.date_derniere_intervention = timezone.now().date()

                            exemplaire.update_kilometres()
                            exemplaire.save()

                            # 🔗 checkup UNIQUE
                            controle = form.save(commit=False)
                            controle.assign_technicien(request.user)

                            controle.kilometres_chassis = exemplaire.kilometres_chassis
                            controle.kilometrage_jeu = km

                        # 🔴 maintenance unique
                        maintenance = Maintenance.objects.create(
                            societe=request.user.societe,
                            voiture_exemplaire=exemplaire,
                            immatriculation=exemplaire.immatriculation,
                            date_intervention=timezone.now().date(),
                            kilometres_chassis=exemplaire.kilometres_chassis,
                            kilometres_dernier_entretien=exemplaire.kilometres_dernier_entretien,
                            type_maintenance=Maintenance.TypeMaintenance.JEUX_PIECES,
                            tag=Maintenance.Tag.JAUNE,
                        )

                        # 🔧 affectation rôle
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
                        controle.assign_technicien(request.user)

                        # 🔗 lien final
                        controle.maintenance = maintenance
                        controle.save()

                        UserLog.objects.create(
                            utilisateur=request.user,
                            action=_("Jeux - %(immatriculation)s") % {
                                "immatriculation": exemplaire.immatriculation
                            }
                        )


                    messages.success(request, _("Contrôle des jeux enregistré avec succès."))

                except Exception as e:
                    messages.error(request, _(f"Erreur lors de l'enregistrement : {str(e)}"))
            else:
                print("FORM INVALID:", form.errors)
                messages.error(request, _("Le formulaire contient des erreurs."))

        else:
            controle = ControleJeuxPieces(
                voiture_exemplaire=exemplaire,
                kilometres_chassis=exemplaire.kilometres_chassis
            )

            controle.assign_technicien(request.user)

            form = ControleJeuxPiecesForm(
                instance=controle,
                user=request.user,
                exemplaire=exemplaire
            )

        return render(request, "jeux_pieces/controle_jeux.html", {
            "exemplaire": exemplaire,
            "immatriculation": exemplaire.immatriculation,
            "maintenance": maintenance,
            "form": form,
            "now": timezone.now(),
        })




# ------------
# Vue détail checkup
# -----------------------------
@login_required
def jeux_pieces_detail_view(request, jeu_id):
    jeu = get_object_or_404(
        ControleJeuxPieces.objects.select_related("voiture_exemplaire"),
        id=jeu_id
    )

    context = {
        "jeu": jeu,
        "exemplaire": jeu.voiture_exemplaire,
    }
    return render(request, "jeux_pieces/jeux_pieces_detail.html", context)


@login_required
def modifier_jeux_pieces_view(request, jeu_id):
    tenant = request.user.societe

    with tenant_context(tenant):
        # Récupération du checkup avec son exemplaire
        jeu = get_object_or_404(
            ControleJeuxPieces.objects.select_related("voiture_exemplaire"),
            id=jeu_id
        )
        exemplaire = jeu.voiture_exemplaire
        # -------------------------
        # POST
        # -------------------------
        if request.method == "POST":
            form = ControleJeuxPiecesForm(
                request.POST,
                instance=jeu,
                user=request.user,
                exemplaire=jeu.voiture_exemplaire
            )
            if form.is_valid():
                form.save()

                UserLog.objects.create(
                    utilisateur=request.user,
                    action=_("Modification jeux - %(immatriculation)s") % {
                        "immatriculation": exemplaire.immatriculation
                    }
                )

                messages.success(request, _("Contrôle des jeux modifié avec succès !"))

            else:
                messages.error(request, _("Le formulaire contient des erreurs."))
                print(form.errors)

        # -------------------------
        # GET
        # -------------------------
        else:
            form = ControleJeuxPiecesForm(
                instance=jeu,
                user=request.user,
                exemplaire=jeu.voiture_exemplaire
            )

    return render(
        request,
        "jeux_pieces/modifier_jeux_pieces.html",
        {
            "form": form,
            "jeu": jeu,
            "exemplaire": jeu.voiture_exemplaire,
        }
    )





@login_required
def controle_jeux_pdf_view(request, controle_id):
    tenant = request.user.societe

    with tenant_context(tenant):
        controle = get_object_or_404(
            ControleJeuxPieces.objects.select_related(
                "voiture_exemplaire",
                "maintenance",
                "main_oeuvre",
                "tech_technicien",
                "tech_societe",
            ),
            id=controle_id
        )

        html_string = render_to_string(
            "jeux_pieces/controle_jeux_pdf.html",
            {
                "controle": controle,
                "objet": controle,
                "date_export": timezone.now(),
                "societe": tenant,
            },
            request=request
        )

        pdf_file = HTML(
            string=html_string,
            base_url=request.build_absolute_uri("/")
        ).write_pdf()

        response = HttpResponse(pdf_file, content_type="application/pdf")
        response["Content-Disposition"] = (
            f'inline; filename="controle_jeux_{controle.id}.pdf"'
        )
        return response