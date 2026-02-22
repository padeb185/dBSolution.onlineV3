from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import ListView
from recharge.models import Electricite




@method_decorator([login_required, never_cache], name="dispatch")
class ElectriciteListView(ListView):
    model = Electricite
    template_name = "recharge/recharge_list.html"
    context_object_name = "recharges"   # ⚠️ important : pluriel
    paginate_by = 20
    ordering = ["-date"]

    def get_queryset(self):
        return (
            Electricite.objects
            .select_related(
                "utilisateur",
                "voiture_exemplaire",
                "voiture_exemplaire__voiture_modele",
                "voiture_exemplaire__voiture_modele__voiture_marque",
            )
            .order_by("-date")
        )

