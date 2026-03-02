from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django_tenants.utils import tenant_context
from voiture.voiture_marque.models import VoitureMarque
from .models import VoitureModele
from .forms import VoitureModeleForm
from django.utils.translation import gettext as _



@login_required
def modeles_par_marque(request, marque_id):
    marque = get_object_or_404(VoitureMarque, id_marque=marque_id)
    modeles = VoitureModele.objects.filter(marque=marque).order_by('nom_modele')
    context = {
        'marque': marque,
        'modeles': modeles,
    }
    return render(request, 'voiture_modele/modeles_list_all.html', context)



class VoitureModeleListView(LoginRequiredMixin, ListView):
    model = VoitureModele
    template_name = "voiture_modele/voituremodele_list.html"  # ton template actuel
    context_object_name = "voiture_modeles"  # ⚡ correspond à ta boucle {% for voiture_modele in voiture_modeles %}


    def get_queryset(self):
        # ⚡ multi-tenant : on ne renvoie que les modèles de la société de l'utilisateur
        tenant = self.request.user.societe
        with tenant_context(tenant):
            return (
                VoitureModele.objects
                .filter(societe=tenant)
                .select_related("voiture_marque")
                .order_by("voiture_marque__nom_marque", "nom_modele")
            )



@login_required
def voiture_modele_detail(request, voiture_modele_id):
    tenant = request.user.societe

    with tenant_context(tenant):
        voiture_modele = get_object_or_404(VoitureModele, id=voiture_modele_id)


    return render(
        request,
        "voiture_modele/voiture_modele_detail.html",
        {
            "voiture_modele": voiture_modele,

        },
    )



@login_required
def ajouter_modele(request):
    tenant = request.user.societe

    with tenant_context(tenant):
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
                return redirect("voiture_modele:voituremodele_list")

        else:
            form = VoitureModeleForm(user=request.user)

        return render(
            request,
            "voiture_modele/ajouter_modele.html",
            {"form": form, "title": _("Ajouter un modèle"), "submit_text": _("Créer le modèle")},
        )



@login_required
def modifier_voiture_modele(request, voiture_modele_id):
    tenant = request.user.societe

    with tenant_context(tenant):
        # Récupérer le modèle voiture
        voiture_modele = get_object_or_404(VoitureModele, id=voiture_modele_id)

        if request.method == "POST":
            form_voiture_modele = VoitureModeleForm(request.POST, instance=voiture_modele)

            if form_voiture_modele.is_valid():
                form_voiture_modele.save()  # pas besoin de commit=False si pas de traitement spécial
                messages.success(request, "VoitureModele mise à jour avec succès.")
                return redirect("voiture_modele:modifier_voiture_modele", voiture_modele_id=voiture_modele.id)
            else:
                messages.error(request, "Le formulaire contient des erreurs.")
        else:
            form_voiture_modele = VoitureModeleForm(instance=voiture_modele)

    return render(
        request,
        "voiture_modele/modifier_voiture_modele_view.html",
        {
            "form": form_voiture_modele,
            "voiture_modele": voiture_modele,
        }
    )




def check_nom(request):
    nom = request.POST.get("nom")
    existe = VoitureModele.objects.filter(nom__iexact=nom).exists()
    return JsonResponse({"existe": existe})