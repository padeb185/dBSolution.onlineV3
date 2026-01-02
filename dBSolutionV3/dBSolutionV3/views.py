# theme/views.py (ou core/views.py)
from django.shortcuts import render, redirect

def home_view(request):
    if request.user.is_authenticated:
        return redirect("utilisateurs:dashboard")
    # Si l'utilisateur n'est pas connecté, afficher la page home
    return render(request, "home.html")
