from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginTOTPForm
from .models import Utilisateur

def login_totp_view(request):
    form = LoginTOTPForm(request.POST or None)
    message = ""

    if request.method == "POST" and form.is_valid():
        email = form.cleaned_data['email_google']
        password = form.cleaned_data['password']
        token = form.cleaned_data['totp_token']

        user = authenticate(request, email_google=email, password=password)
        if user is not None:
            if user.verify_totp(token):
                login(request, user)
                return redirect('home')  # page d'accueil après connexion
            else:
                message = "Code TOTP incorrect"
        else:
            message = "Email ou mot de passe incorrect"

    return render(request, 'login_totp.html', {'form': form, 'message': message})
