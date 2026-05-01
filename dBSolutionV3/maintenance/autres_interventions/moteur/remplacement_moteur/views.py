from django.views.generic import ListView
from django.db import models
from voiture.voiture_exemplaire.models import VoitureExemplaire
from django.views.generic import CreateView
from django.urls import reverse
from django.contrib import messages
from django.utils.timezone import now
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from .models import RemplacementMoteur
from .forms import RemplacementMoteurForm
from voiture.voiture_exemplaire.models import VoitureExemplaire





@method_decorator([login_required, never_cache], name='dispatch')
class RemplacementMoteurListView(ListView):
    model = RemplacementMoteur
    template_name = "remplacement_moteur/remplacement_moteur_list.html"
    context_object_name = "remplacements"

    def get_queryset(self):
        queryset = RemplacementMoteur.objects.select_related(
            "voiture_exemplaire",
            "voiture_marque",
            "voiture_modele",
            "tech_societe",
            "client",
        )

        # 🔒 Filtrage par société
        societe = getattr(self.request.user, "societe", None)
        if societe:
            queryset = queryset.filter(
                models.Q(tech_societe=societe) |
                models.Q(tech_societe__isnull=True)
            )

        # 🎯 Filtrage par exemplaire (IMPORTANT)
        exemplaire_id = self.kwargs.get("exemplaire_id")
        if exemplaire_id:
            queryset = queryset.filter(voiture_exemplaire_id=exemplaire_id)

        return queryset.order_by("-date")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        exemplaire_id = self.kwargs.get("exemplaire_id")

        if exemplaire_id:
            try:
                context["exemplaire"] = VoitureExemplaire.objects.get(id=exemplaire_id)
            except VoitureExemplaire.DoesNotExist:
                context["exemplaire"] = None

        return context






@method_decorator([login_required, never_cache], name='dispatch')
class RemplacementMoteurCreateView(CreateView):
    model = RemplacementMoteur
    form_class = RemplacementMoteurForm
    template_name = "remplacement_moteur/remplacement_moteur_form.html"

    def get_exemplaire(self):
        return VoitureExemplaire.objects.get(id=self.kwargs["exemplaire_id"])

    def get_initial(self):
        initial = super().get_initial()
        exemplaire = self.get_exemplaire()

        initial.update({
            "voiture_exemplaire": exemplaire,
            "voiture_marque": exemplaire.voiture_marque,
            "voiture_modele": exemplaire.voiture_modele,
            "immatriculation": exemplaire.immatriculation,
            "kilometres_chassis": exemplaire.kilometrage,
        })
        return initial

    def form_valid(self, form):
        exemplaire = self.get_exemplaire()

        obj = form.save(commit=False)
        obj.voiture_exemplaire = exemplaire
        obj.societe = getattr(self.request.user, "societe", None)
        obj.last_maintained_by = self.request.user

        obj.save()

        messages.success(self.request, "Remplacement moteur enregistré avec succès.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("remplacement_moteur:remplacement_moteur_list", kwargs={
            "exemplaire_id": self.kwargs["exemplaire_id"]
        })

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        exemplaire = self.get_exemplaire()

        context["exemplaire"] = exemplaire
        context["now"] = now()

        form = context["form"]

        context["sections"] = [
            {
                "title": "Informations véhicule",
                "icon": "icons/voiture.png",
                "fields": [
                    form["voiture_marque"],
                    form["voiture_modele"],
                    form["immatriculation"],
                ],
            },
            {
                "title": "Kilométrage",
                "icon": "icons/kilometrage.png",
                "fields": [
                    form["kilometres_chassis"],
                    form["kilometres_dernier_entretien"],
                    form["kilometres_moteur"],
                ],
            },
            {
                "title": "Remplacement moteur",
                "icon": "icons/moteur.png",
                "fields": [
                    form["remplacement_effectue"],
                    form["numero_moteur"],
                    form["prix_moteur"],
                ],
            },
            {
                "title": "Niveaux",
                "icon": "icons/liquide.png",
                "fields": [
                    form["moteur_niveau_huile_etat"],
                    form["moteur_niveau_huile_quantite"],
                    form["moteur_niveau_huile_qualite"],
                    form["refroidissement_etat"],
                    form["refroidissement_quantite"],
                    form["refroidissement_qualite"],
                ],
            },
            {
                "title": "Technicien",
                "icon": "icons/technicien.png",
                "fields": [
                    form["tech_nom_technicien"],
                    form["tech_role_technicien"],
                    form["tech_societe"],
                ],
            },
        ]

        return context