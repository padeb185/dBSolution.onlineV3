from django.utils import timezone
from datetime import timedelta
from django.shortcuts import render
from .models import AssurancePolice, Sinistre



def dashboard_assurances(request):
    today = timezone.now().date()
    in_30_days = today + timedelta(days=30)

    polices_actives = AssurancePolice.objects.filter(actif=True).count()
    polices_expirees = AssurancePolice.objects.filter(date_fin__lt=today).count()
    polices_bientot = AssurancePolice.objects.filter(date_fin__range=(today, in_30_days)).count()

    sinistres_ouverts = Sinistre.objects.filter(cloture=False).count()

    cout_total = AssurancePolice.cout_total_annuel()

    context = {
        'polices_actives': polices_actives,
        'polices_expirees': polices_expirees,
        'polices_bientot': polices_bientot,
        'sinistres_ouverts': sinistres_ouverts,
        'cout_total': cout_total,
    }

    return render(request, 'assurance_police/dashboard.html', context)

