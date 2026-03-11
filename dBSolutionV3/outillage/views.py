from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import ListView
from outillage.models import Outillage


@method_decorator([login_required, never_cache], name='dispatch')
class OutillageListView(ListView):
    model = Outillage
    template_name = "outillage/outillage_list.html"
    context_object_name = "outillage"
    paginate_by = 20
    ordering = ["nom"]

    def get_queryset(self):
        societe = self.request.user.societe
        return Outillage.objects.filter(societe=societe)
