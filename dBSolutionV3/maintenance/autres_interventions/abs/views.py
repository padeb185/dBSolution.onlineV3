from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.db import transaction, models
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import ListView
from django_tenants.utils import tenant_context
from maintenance.models import Maintenance
from voiture.voiture_exemplaire.models import VoitureExemplaire
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView
from decimal import Decimal
from .forms import AbsForm
from .models import Abs


@method_decorator([login_required, never_cache], name='dispatch')
class AbsListView(ListView):
    model = Abs
    template_name = "abs/abs_list.html"
    context_object_name = "abss"
    paginate_by = 100
    ordering = ["-id"]

    def get_queryset(self):
        queryset = Abs.objects.select_related(
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
        return context



@never_cache
@login_required
def abs_form_view(request, exemplaire_id):
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
            type_maintenance="abs"
        ).order_by("-date_intervention").first()

        if not maintenance:
            maintenance = Maintenance.objects.create(
                societe=tenant,
                voiture_exemplaire=exemplaire,
                mecanicien=request.user,
                immatriculation=exemplaire.immatriculation,
                date_intervention=timezone.localtime(timezone.now()).date(),
                kilometres_chassis=exemplaire.kilometres_chassis,
                kilometres_dernier_entretien=exemplaire.kilometres_dernier_entretien,
                type_maintenance="abs",
                tag=Maintenance.Tag.JAUNE,
            )

        # Créer ou récupérer l'objet admission
        abs = Abs(
            voiture_exemplaire=exemplaire,
            maintenance=maintenance,
            kilometres_chassis=exemplaire.kilometres_chassis
        )
        abs.assign_technicien(request.user)


        # --- Formulaire ---
        if request.method == "POST":
            form = AbsForm(
                request.POST,
                instance=abs,
                user=request.user,
                exemplaire=exemplaire
            )

            if form.is_valid():
                try:
                    with transaction.atomic():
                        abs = form.save(commit=False)

                        # Gestion du kilométrage
                        km_checkup = form.cleaned_data.get("kilometres_chassis")
                        if km_checkup is not None and km_checkup >= exemplaire.kilometres_chassis:
                            abs.kilometres_chassis = km_checkup
                            exemplaire.kilometres_chassis = km_checkup
                            exemplaire.save()
                        elif km_checkup is not None and km_checkup < exemplaire.kilometres_chassis:
                            form.add_error(
                                "kilometres_chassis",
                                _("Le kilométrage ne peut pas être inférieur au kilométrage actuel.")
                            )
                            raise ValueError("Kilométrage invalide")

                        abs.save()
                    messages.success(request, _("Contrôle du système ABS enregistré avec succès."))

                except Exception as e:
                    messages.error(request, _(f"Erreur lors de l'enregistrement : {str(e)}"))

            else:
                messages.error(request, _("Le formulaire contient des erreurs."))
                print(form.errors)

        else:
            form = AbsForm(
                instance=abs,
                user=request.user,
                exemplaire=exemplaire
            )

        # --- Génération des champs par section ---
        sections = [
            {
                "title": _("Kilométrage"),
                "icon": "icons/compteur.png",
                "fields": [form[f.name] for f in form if "kilo" in f.name],
            },
            {
                "title": _("Pompe du système ABS"),
                "icon": "icons/abs.png",
                "fields": [form[f.name] for f in form if "pompe" in f.name],
            },
            {
                "title": _("Calculateur ABS"),
                "icon": "icons/calculateur.png",
                "fields": [form[f.name] for f in form if "calculateur" in f.name],
            },
            {
                "title": _("Capteur ABS"),
                "icon": "icons/capteurs.png",
                "fields": [form[f.name] for f in form if "capteur" in f.name],
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

        return render(request, 'abs/abs_form.html', {
            "exemplaire": exemplaire,
            "immatriculation": exemplaire.immatriculation,
            "maintenance": maintenance,
            "form": form,
            "sections": sections,
            "now": timezone.now(),
        })


# ------------
# Vue détail boite
# -----------------------------
@login_required
def abs_detail_view(request, abs_id):
    abs = get_object_or_404(
        Abs.objects.select_related("voiture_exemplaire"),
        id=abs_id
    )

    context = {
        "abs": abs,
        "exemplaire": abs.voiture_exemplaire,
    }
    return render(request, "abs/abs_detail.html", context)



@login_required
def modifier_abs_view(request, abs_id):
    tenant = request.user.societe

    with tenant_context(tenant):

        abs = get_object_or_404(
            Abs.objects.select_related("voiture_exemplaire"),
            id=abs_id
        )

        # -------------------------
        # POST
        # -------------------------
        if request.method == "POST":
            form = AbsForm(
                request.POST,
                instance=abs,
                user=request.user,
                exemplaire=abs.voiture_exemplaire
            )

            if form.is_valid():
                form.save()
                messages.success(request, _("Contrôle du système ABS modifié avec succès !"))
                return redirect("abs:modifier_abs", abs_id=abs.id)
            else:
                messages.error(request, _("Le formulaire contient des erreurs."))
                print(form.errors)

        # -------------------------
        # GET
        # -------------------------
        else:
            form = AbsForm(
                instance=abs,
                user=request.user,
                exemplaire=abs.voiture_exemplaire
            )

        # -------------------------
        # Sections pour le template
        # -------------------------
        sections = [
            {
                "title": _("Kilométrage"),
                "icon": "icons/compteur.png",
                "fields": [form[f.name] for f in form if "kilo" in f.name],
            },
            {
                "title": _("Pompe du système ABS"),
                "icon": "icons/abs.png",
                "fields": [form[f.name] for f in form if "pompe" in f.name],
            },
            {
                "title": _("Calculateur ABS"),
                "icon": "icons/calculateur.png",
                "fields": [form[f.name] for f in form if "calculateur" in f.name],
            },
            {
                "title": _("Capteur ABS"),
                "icon": "icons/capteurs.png",
                "fields": [form[f.name] for f in form if "capteur" in f.name],
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

    return render(
        request,
        "abs/modifier_abs.html",
        {
            "form": form,
            "abs": abs,
            "sections": sections,
            "exemplaire": abs.voiture_exemplaire,
        }
    )


@login_required
def rapport_abs_view(request, pk):
    obj = get_object_or_404(Abs, pk=pk)

    rapport = obj.generer_rapport_remplacement()

    return render(request, "abs/rapport_abs.html", {
        "rapport": rapport,
        "obj": obj
    })





class AbsRapportDetailView(DetailView):
    model = Abs
    template_name = "abs/rapport_pdf_abs.html"
    context_object_name = "obj"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        obj = self.object

        rapport = obj.generer_rapport_remplacement()

        if not rapport:
            rapport = {"lignes": [], "total_general": Decimal("0")}

        # 🔥 AJOUT DU TAUX TVA DANS CHAQUE LIGNE
        taux_tva = obj.TVA_PIECES.get(obj.pays, 0)

        for ligne in rapport["lignes"]:
            ligne["taux_tva"] = taux_tva

        context["rapport"] = rapport

        return context