from django.shortcuts import render
from django.utils.translation import gettext as _

def home(request):
    message = _("Welcome to the platform")
    return render(request, "home.html", {"message": message})


def dashboard(request):
    message = _("Welcome to the dashboard")
    return render(request, 'dashboard.html', {'message': message})
