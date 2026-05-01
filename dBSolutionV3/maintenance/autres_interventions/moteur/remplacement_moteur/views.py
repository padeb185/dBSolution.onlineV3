from django.utils import timezone
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from django.db import models, transaction
from django_tenants.utils import tenant_context
from voiture.voiture_exemplaire.models import VoitureExemplaire
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from maintenance.models import Maintenance
from .models import RemplacementMoteur
from .forms import RemplacementMoteurForm
from voiture.voiture_exemplaire.models import VoitureExemplaire
from django.utils.translation import gettext_lazy as _



from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.db.models import Q

from .models import RemplacementMoteur
from voiture.voiture_exemplaire.models import VoitureExemplaire


@method_decorator([login_required, never_cache], name="dispatch")
class RemplacementMoteurListView(ListView):
    model = RemplacementMoteur
    template_name = "remplacement_moteur/remplacement_moteur_list.html"
    context_object_name = "remplacements"

    def get_queryset(self):
        queryset = RemplacementMoteur.objects.select_related(
            "voiture_exemplaire",
            "tech_societe",
            "client",
        )

        societe = getattr(self.request.user, "societe", None)

        if societe:
            queryset = queryset.filter(tech_societe=societe)

        exemplaire_id = self.kwargs.get("exemplaire_id")

        if exemplaire_id:
            queryset = queryset.filter(voiture_exemplaire_id=exemplaire_id)

        return queryset.order_by("-date")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        exemplaire_id = self.kwargs.get("exemplaire_id")

        context["exemplaire"] = None

        if exemplaire_id:
            context["exemplaire"] = VoitureExemplaire.objects.filter(
                id=exemplaire_id
            ).first()

        return context



@never_cache
@login_required
def remplacement_moteur_form_view(request, exemplaire_id):
    tenant = request.user.societe

    with tenant_context(tenant):
        # Récupération de l'exemplaire
        exemplaire = get_object_or_404(
            VoitureExemplaire.objects.filter(
                Q(client__societe=tenant) | Q(client__isnull=True, societe=tenant)
            ),
            id=exemplaire_id
        )

        # Vérification des rôles
        roles_autorises = ["mécanicien", "apprenti", "magasinier", "chef mécanicien"]
        if request.user.role not in roles_autorises:
            messages.error(
                request,
                _("Seuls les mécaniciens, apprentis, magasiniers et chefs mécaniciens peuvent accéder à cette page.")
            )
            return redirect("maintenance_liste_all")

        # Récupération ou création de la maintenance
        maintenance = Maintenance.objects.filter(
            voiture_exemplaire=exemplaire,
            type_maintenance="courroie"
        ).order_by("-date_intervention").first()

        if not maintenance:
            maintenance = Maintenance.objects.create(
                societe=tenant,
                voiture_exemplaire=exemplaire,
                mecanicien=request.user,
                immatriculation=exemplaire.immatriculation,
                date_intervention=timezone.now().date(),
                kilometres_chassis=exemplaire.kilometres_chassis,
                kilometres_dernier_entretien=exemplaire.kilometres_dernier_entretien,
                type_maintenance="admission",
                tag=Maintenance.Tag.JAUNE,
            )

        # Créer ou récupérer l'objet admission
        remplacement_moteur = RemplacementMoteur(
            voiture_exemplaire=exemplaire,
            maintenance=maintenance,
            kilometres_chassis=exemplaire.kilometres_chassis
        )
        remplacement_moteur.assign_technicien(request.user)


        # --- Formulaire ---
        if request.method == "POST":
            form = RemplacementMoteurForm(
                request.POST or None,
                instance=remplacement_moteur,
                user=request.user,
                exemplaire=exemplaire
            )

            if form.is_valid():
                try:
                    with transaction.atomic():
                        remplacement_moteur = form.save(commit=False)

                        # Gestion du kilométrage
                        km_checkup = form.cleaned_data.get("kilometres_chassis")
                        if km_checkup is not None and km_checkup >= exemplaire.kilometres_chassis:
                            remplacement_moteur.kilometres_chassis = km_checkup
                            exemplaire.kilometres_chassis = km_checkup
                            exemplaire.save()
                        elif km_checkup is not None and km_checkup < exemplaire.kilometres_chassis:
                            form.add_error(
                                "kilometres_chassis",
                                _("Le kilométrage ne peut pas être inférieur au kilométrage actuel.")
                            )
                            raise ValueError("Kilométrage invalide")

                        remplacement_moteur.save()
                    messages.success(request, _("Remplacement du moteur enregistré avec succès."))

                except Exception as e:
                    messages.error(request, _(f"Erreur lors de l'enregistrement : {str(e)}"))

            else:
                messages.error(request, _("Le formulaire contient des erreurs."))
                print(form.errors)

        else:
            form = RemplacementMoteurForm(
                request.POST or None,
                instance=remplacement_moteur,
                user=request.user,
                exemplaire=exemplaire
            )


        # --- Génération des champs par section ---
        sections = [
            {
                "title": _("Voiture"),
                "icon": "icons/voiture-de-course.png",
                "fields": [form[f.name] for f in form if "voiture" in f.name],
            },
            {
                "title": _("Utilisation"),
                "icon": "icons/.png",
                "fields": [form[f.name] for f in form if "type_util" in f.name],
            },
            {
                "title": _("Kilométrage"),
                "icon": "icons/compteur.png",
                "fields": [form[f.name] for f in form if "kilo" in f.name],
            },
            {
                "title": _("Remplacement du moteur"),
                "icon": "icons/engine.png",
                "fields": [form[f.name] for f in form if "moteur" in f.name],
            },


            {
                "title": _("Liquide de refroidissement"),
                "icon": "icons/radiateur.png",
                "fields": [form[f.name] for f in form if "refroidissement" in f.name],
            },

            {
                "title": _("Etiquette"),
                "icon": "icons/tag.png",
                "fields": [form[f.name] for f in form if "tag" in f.name],
            },
            {
                "title": _("Pays"),
                "icon": "icons/pays.png",
                "fields": [form[f.name] for f in form if "pays" in f.name],
            },
            {
                "title": _("Remarques"),
                "icon": "icons/notes.png",
                "fields": [form[f.name] for f in form if "remarques" in f.name],
            },
            {
                "title": _("Technicien"),
                "icon": "icons/mecanicien.png",
                "fields": [form[f.name] for f in form if "tech" in f.name],
            },

        ]

        return render(request, "remplacement_moteur/remplacement_moteur_form.html", {
            "remplacement_moteur": remplacement_moteur,
            "exemplaire": exemplaire,
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

    with tenant_context(tenant):

        remplacement_moteur = get_object_or_404(
            RemplacementMoteur.objects.select_related("voiture_exemplaire"),
            id=remplacement_moteur_id
        )

        # -------------------------
        # POST
        # -------------------------
        if request.method == "POST":
            form = RemplacementMoteurForm(
                request.POST,
                instance=remplacement_moteur,
                user=request.user,
                exemplaire=remplacement_moteur.voiture_exemplaire
            )

            if form.is_valid():
                form.save()
                messages.success(request, _("Remplacement du moteur modifié avec succès !"))
                return redirect(
                    "remplacement_moteur:modifier_remplacement_moteur",
                    remplacement_moteur_id=remplacement_moteur.id
                )
            else:
                messages.error(request, _("Le formulaire contient des erreurs."))
                print(form.errors)

        # -------------------------
        # GET
        # -------------------------
        else:
            form = RemplacementMoteurForm(
                instance=remplacement_moteur,
                user=request.user,
                exemplaire=remplacement_moteur.voiture_exemplaire
            )

        # -------------------------
        # SECTIONS
        # -------------------------
        sections = [
            {
                "title": _("Voiture"),
                "icon": "icons/voiture-de-course.png",
                "fields": [form[f.name] for f in form if "voiture" in f.name],
            },
            {
                "title": _("Utilisation"),
                "icon": "icons/utilisation.png",
                "fields": [form[f.name] for f in form if "type_util" in f.name],
            },
            {
                "title": _("Kilométrage"),
                "icon": "icons/compteur.png",
                "fields": [form[f.name] for f in form if "kilo" in f.name],
            },
            {
                "title": _("Remplacement du moteur"),
                "icon": "icons/engine.png",
                "fields": [form[f.name] for f in form if "moteur" in f.name],
            },
            {
                "title": _("Liquide de refroidissement"),
                "icon": "icons/radiateur.png",
                "fields": [form[f.name] for f in form if "refroidissement" in f.name],
            },
            {
                "title": _("Etiquette"),
                "icon": "icons/tag.png",
                "fields": [form[f.name] for f in form if "tag" in f.name],
            },
            {
                "title": _("Pays"),
                "icon": "icons/pays.png",
                "fields": [form[f.name] for f in form if "pays" in f.name],
            },
            {
                "title": _("Remarques"),
                "icon": "icons/notes.png",
                "fields": [form[f.name] for f in form if "remarques" in f.name],
            },
            {
                "title": _("Technicien"),
                "icon": "icons/mecanicien.png",
                "fields": [form[f.name] for f in form if "tech" in f.name],
            },
        ]

        return render(request, "remplacement_moteur/modifier_remplacement_moteur.html", {
            "remplacement_moteur": remplacement_moteur,
            "form": form,
            "sections": sections,
            "exemplaire": remplacement_moteur.voiture_exemplaire,
        })