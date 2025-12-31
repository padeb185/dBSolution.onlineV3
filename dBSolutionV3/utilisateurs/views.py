from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Utilisateur
from .forms import LoginForm
from django.contrib.auth import login, authenticate


def login_view(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        user = authenticate(
            email_google=form.cleaned_data['email'],
            password=form.cleaned_data['password']
        )
        if user:
            if not user.totp_secret:
                # si TOTP pas configuré
                user.generate_totp_secret()
                return redirect('totp_setup')  # redirige vers la page pour scanner le QR
            else:
                # si TOTP déjà configuré
                request.session['pre_totp_user_id'] = str(user.id)
                return redirect('totp_verify')
        else:
            messages.error(request, "Email ou mot de passe incorrect")
    return render(request, 'login.html', {'form': form})




def totp_verify_view(request):
    if request.method == 'POST':
        token = request.POST.get('token')
        user_id = request.session.get('pre_totp_user_id')
        user = Utilisateur.objects.get(id=user_id)
        if user.verify_totp(token):
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Code TOTP invalide")
    return render(request, 'totp/verify.html')


def dashboard_view(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    user = Utilisateur.objects.get(id=user_id)
    return render(request, "dashboard.html", {"user": user})



def totp_setup_view(request):
    user_id = request.user.id
    user = Utilisateur.objects.get(id=user_id)
    qr_code = user.generate_qr_code()
    return render(request, 'totp/setup.html', {'qr_code': qr_code})
