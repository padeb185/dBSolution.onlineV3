# theme/views.py (ou core/views.py)
from django.shortcuts import redirect

def home_view(request):
    if request.user.is_authenticated:
        return redirect("utilisateurs:dashboard")
    return redirect("utilisateurs:login")

