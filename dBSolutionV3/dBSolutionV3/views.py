from django.shortcuts import render, redirect
from django.utils.translation import gettext as _
from authentification.forms import LoginForm



def home(request):
    message = _("Bienvenue sur notre site")
    return render(request, "home.html", {"message": message})

def login(request):
    form = LoginForm()
    if len(request.POST):
        if form.is_valid():
            return redirect('dashboard')
        else:
            return render(request, "login.html", {"form": form})
    else :
        form = LoginForm(request.POST)
        return render(request, "login.html", {"form": form})


def dashboard(request):
    message = _("Bienvenue sur ton tableau de bord")
    return render(request, 'dashboard.html', {'message': message})
