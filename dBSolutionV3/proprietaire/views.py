from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import ListView
from django_tenants.utils import schema_context
from proprietaire.models import Proprietaire, ProprietaireVoiture




@never_cache
@login_required
def proprietaire_dashboard_view(request):
    user = request.user
    societe = getattr(user, "societe", None)

    # Valeurs par défaut
    total_proprietaire = 0
    total_voiture_cop = 0
    proprietaire = []
    proprietaire_voiture = []

    if societe:
        schema_name = societe.schema_name

        with schema_context(schema_name):

            proprietaire = Proprietaire.objects.filter(societe=societe)
            proprietaire_voiture = ProprietaireVoiture.objects.filter(societe=societe)

            total_proprietaire = proprietaire.count()
            total_voiture_cop = proprietaire_voiture.count()

    context = {
        "user": user,
        "societe": societe,
        "total_proprietaire": total_proprietaire,
        "total_voiture_cop": total_voiture_cop,
        "proprietaire": proprietaire,
        "proprietaire_voiture": proprietaire_voiture,

    }

    return render(request, "proprietaire/proprietaire_dashboard.html", context)




@method_decorator([login_required, never_cache], name='dispatch')
class ProprietaireListView(ListView):
    model = Proprietaire
    template_name = "proprietaire/proprietaire_list.html"
    context_object_name = "proprietaires"
    paginate_by = 20
    ordering = ["nom_proprietaire"]

    def get_queryset(self):
        user = self.request.user

        if not hasattr(user, "societe") or user.societe is None:
            return Proprietaire.objects.none()

        return Proprietaire.objects.filter(societe=user.societe)






@method_decorator([login_required, never_cache], name='dispatch')
class ProprietaireVoitureListView(ListView):
    model = Proprietaire
    template_name = "proprietaire/proprietaire_voiture_list.html"
    context_object_name = "proprietaire_voitures"
    paginate_by = 20
    ordering = ["nom_proprietaire_voiture"]

    def get_queryset(self):
        user = self.request.user

        if not hasattr(user, "societe") or user.societe is None:
            return Proprietaire.objects.none()

        return Proprietaire.objects.filter(societe=user.societe)


