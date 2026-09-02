from decimal import Decimal
from django.shortcuts import redirect, render
from django.contrib import messages
from django.db import transaction, models
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import ListView
from maintenance.models import Maintenance
from maintenance.jeux_pieces.models import ControleJeuxPieces
from maintenance.jeux_pieces.forms import ControleJeuxPiecesForm
from utilisateurs.models import UserLog
from voiture.voiture_exemplaire.models import VoitureExemplaire
from django.db.models import Q
from django.utils.translation import gettext_lazy as _, gettext_noop
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponse
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

                    controle = form.save(commit=False)

                    controle.assign_technicien(request.user)
                    controle.voiture_exemplaire = exemplaire
                    controle.immatriculation = exemplaire.immatriculation
                    controle.societe = tenant
                    controle.kilometres_chassis = exemplaire.kilometres_chassis

                    km = form.cleaned_data.get("kilometrage_jeu")

                    # ✅ On conserve le kilométrage précédent
                    ancien_kilometrage = exemplaire.kilometres_chassis or 0

                    # ✅ Variation calculée dynamiquement
                    kilometrage_variation = 0

                    if km is not None:

                        # Validation
                        if km < ancien_kilometrage:
                            raise ValueError(
                                _("Le kilométrage du Checkup-Freins ne peut pas être inférieur "
                                  "au kilométrage actuel du véhicule.")
                            )

                        # Calcul AVANT mise à jour du véhicule
                        kilometrage_variation = km - ancien_kilometrage

                        # Mise à jour du kilométrage véhicule
                        exemplaire.kilometres_chassis = km
                        exemplaire.save(
                            update_fields=["kilometres_chassis"]
                        )

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
                    controle = form.save(commit=False)

                    controle.voiture_exemplaire = exemplaire
                    controle.maintenance = maintenance

                    # ✅ kilométrage saisi lors du controle
                    controle.kilometrage_jeu = km

                    # ✅ ancien kilométrage avant le controle
                    controle.kilometres_chassis = ancien_kilometrage

                    # ✅ différence entre les deux
                    controle.kilometrage_variation = kilometrage_variation

                    # 👨‍🔧 technicien
                    controle.assign_technicien(request.user)

                    # 👨‍🔧 dernier technicien maintenance
                    controle.tech_last_maintained_by = request.user

                    controle.save()


                    ACTION_CONTROLE_JEUX = gettext_noop(
                        "Contrôle des jeux"
                    )

                    UserLog.objects.create(
                        utilisateur=request.user,
                        action=f"{ACTION_CONTROLE_JEUX} - {exemplaire.immatriculation}"
                    )


                messages.success(request, _("Contrôle des jeux enregistré avec succès."))
                return redirect("jeux_pieces:jeux_pieces_list", exemplaire_id=exemplaire.id)

            except Exception as e:
                messages.error(request, _(f"Erreur lors de l'enregistrement : {str(e)}"))
        else:
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



            ACTION_MODIFICATION_CONTROLE_JEUX = gettext_noop(
                "Modification du contrôle des jeux"
            )

            UserLog.objects.create(
                utilisateur=request.user,
                action=f"{ACTION_MODIFICATION_CONTROLE_JEUX} - {exemplaire.immatriculation}"
            )
            messages.success(request, _("Contrôle des jeux modifié avec succès !"))
            return redirect("jeux_pieces:jeux_pieces_detail", jeu_id=jeu_id)

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
            "exemplaire": exemplaire,
        }
    )




@login_required
def controle_jeux_pdf_view(request, controle_id):
    tenant = request.user.societe

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

    # Génération du rapport des pièces
    rapport = controle.generer_rapport_remplacement()

    html_string = render_to_string(
        "jeux_pieces/controle_jeux_pdf.html",
        {
            "controle": controle,
            "objet": controle,
            "rapport": rapport,
            "pieces_utilisees": rapport.get("lignes", []),
            "total_pieces": rapport.get(
                "total_general",
                Decimal("0.00"),
            ),
            "date_export": timezone.now(),
            "societe": tenant,
        },
        request=request
    )

    pdf = HTML(
        string=html_string,
        base_url=request.build_absolute_uri("/")
    ).write_pdf()

    # =========================================================
    # IMMATRICULATION
    # =========================================================

    immatriculation = (
        controle.voiture_exemplaire.immatriculation
        if controle.voiture_exemplaire
        else "sans_immatriculation"
    )

    # =========================================================
    # TECHNICIEN
    # =========================================================

    technicien = (
            controle.tech_nom_technicien
            or "technicien_inconnu"
    )

    # Nettoyage pour le nom du fichier
    technicien = str(technicien).replace(" ", "_")
    immatriculation = str(immatriculation).replace(" ", "_")

    # =========================================================
    # DATE
    # =========================================================

    date_pdf = (
        controle.date.strftime("%Y-%m-%d")
        if controle.date
        else timezone.now().strftime("%Y-%m-%d")
    )

    # =========================================================
    # TITRE / NOM DU PDF
    # =========================================================

    nom_fichier = (
        f"{_('Jeux')}_{technicien}_{immatriculation}_{date_pdf}.pdf"
    )

    response = HttpResponse(
        pdf,
        content_type="application/pdf",
    )

    response["Content-Disposition"] = (
        f'inline; filename="{nom_fichier}"'
    )

    return response
