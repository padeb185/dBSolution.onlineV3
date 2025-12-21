from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from authentification.forms import LoginForm
from django.contrib.auth import authenticate, login as auth_login
from django.utils.translation import gettext as _



@login_required
def home(request):
    message = _("Bienvenue sur notre site")
    return render(request, "home.html", {"message": message})



def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('dashboard')  # redirige vers dashboard
            else:
                form.add_error(None, "Nom d'utilisateur ou mot de passe incorrect")
    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})



def dashboard(request):
    message = _("Bienvenue sur ton tableau de bord")
    return render(request, 'dashboard.html', {'message': message})
