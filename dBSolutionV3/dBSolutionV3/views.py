from django.shortcuts import render
from django.utils.translation import gettext as _

def home(request):
    message = _("Bienvenue sur notre site")
    return render(request, "home.html", {"message": message})


def dashboard(request):
    message = _("Bienvenue sur ton tableau de bord")
    return render(request, 'dashboard.html', {'message': message})
