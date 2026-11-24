from django.views.decorators.http import require_POST
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from .models import VoitureModele
from .forms import VoitureModeleForm
from django.utils.translation import gettext as _






class VoitureModeleListView(LoginRequiredMixin, ListView):
    model = VoitureModele
    template_name = "voiture_modele/voituremodele_list.html"  # ton template actuel
    context_object_name = "voiture_modeles"  # ⚡ correspond à ta boucle {% for voiture_modele in voiture_modeles %}


    def get_queryset(self):
        # ⚡ multi-tenant : on ne renvoie que les modèles de la société de l'utilisateur
        tenant = self.request.user.societe

        return (
            VoitureModele.objects
            .filter(societe=tenant)
            .select_related("voiture_marque")
            .order_by("voiture_marque__nom_marque", "nom_modele")
        )



@login_required
def voiture_modele_detail(request, voiture_modele_id):
    voiture_modele = get_object_or_404(VoitureModele, id=voiture_modele_id)


    return render(
        request,
        "voiture_modele/voiture_modele_detail.html",
        {
            "voiture_modele": voiture_modele,

        },
    )



def _initial_depuis_get(request):
    """
    Pré-remplissage depuis l'arborescence d'une marque :
      ?marque=<id>&nom_modele=…&generation=…&phase=…  (+ depuis=<id> : reprend portes, places, réservoir, batterie,
      et la production de la phase, d'une variante existante).
    """
    g = request.GET
    initial = {}
    if g.get("marque"):
        initial["voiture_marque"] = g["marque"]
    for champ in ("nom_modele", "generation", "phase"):
        if g.get(champ):
            initial[champ] = g[champ]
    if g.get("depuis"):
        ref = VoitureModele.objects.filter(pk=g["depuis"], societe=request.user.societe).first()
        if ref is not None:
            for champ in ("nombre_portes", "nbre_places", "taille_reservoir", "capacite_batterie"):
                initial.setdefault(champ, getattr(ref, champ))
            if g.get("phase") is not None and g.get("generation") is not None and g.get("variante") == "1":
                # nouvelle variante d'une phase : même début de production par défaut
                initial.setdefault("mois_debut", ref.mois_debut)
                initial.setdefault("annee_debut", ref.annee_debut)
    return initial


@login_required
def ajouter_modele(request):

    if request.method == "POST":
        form = VoitureModeleForm(request.POST, user=request.user)

        if form.is_valid():
            voiture_modele = form.save(commit=True)

                # sécuriser l'accès à la marque
            nom_marque = (
                voiture_modele.voiture_marque.nom_marque
                if voiture_modele.voiture_marque
                else _("(Marque non définie)")

            )

            messages.success(
                request,
                _("Le modèle a été ajouté avec succès pour la marque %(marque)s.") % {
                    "marque": nom_marque
                }
            )
            # Ajout depuis l'arborescence d'une marque : retour à la marque, sur le modèle ajouté
            if request.POST.get("retour") == "marque":
                from django.urls import reverse
                from django.utils.text import slugify
                url = reverse("voiture_marque:modeles_par_marque", args=[voiture_modele.voiture_marque.pk])
                return redirect(f"{url}#modele-{slugify(voiture_modele.nom_modele) or voiture_modele.pk}")
            return redirect("voiture_modele:voituremodele_list")

    else:
        form = VoitureModeleForm(user=request.user, initial=_initial_depuis_get(request))

    return render(
        request,
        "voiture_modele/ajouter_modele.html",
        {"form": form, "title": _("Ajouter un modèle"), "submit_text": _("Créer le modèle")},
    )


@login_required
def modifier_voiture_modele(request, voiture_modele_id):
    tenant = request.user.societe

    # Récupérer le modèle voiture pour ce tenant
    voiture_modele = get_object_or_404(
        VoitureModele,
        id=voiture_modele_id,
        societe=tenant,
    )

    if request.method == "POST":
        form_voiture_modele = VoitureModeleForm(
            request.POST,
            instance=voiture_modele,
            user=request.user,
        )

        if form_voiture_modele.is_valid():
            form_voiture_modele.save()
            messages.success(request, _("Le modèle de voiture à été mise à jour avec succès."))
            return redirect(
                "voiture_modele:voiture_modele_detail",
                voiture_modele_id=voiture_modele.id,
            )

        messages.error(request, _("Le formulaire contient des erreurs."))

    else:
        form_voiture_modele = VoitureModeleForm(
            instance=voiture_modele,
            user=request.user,
        )

    return render(
        request,
        "voiture_modele/modifier_voiture_modele_view.html",
        {
            "form": form_voiture_modele,
            "voiture_modele": voiture_modele,
        },
    )





@login_required
@require_POST
def check_nom(request):
    nom = request.POST.get("nom")
    existe = VoitureModele.objects.filter(nom__iexact=nom).exists()
    return JsonResponse({"existe": existe})