from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.contrib.auth import views as auth_views
from authentification.views import login_totp, totp_setup
from dBSolutionV3.views import dashboard, home

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),  # pour changer la langue
]

urlpatterns += i18n_patterns(
    # Admin
    path('admin/', admin.site.urls),

    # Page d'accueil
    path('', home, name='home'),

    # Login standard et TOTP
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('login/totp/', login_totp, name='login_totp'),
    path('login/totp/setup/', totp_setup, name='totp_setup'),

    # Dashboard
    path('dashboard/', dashboard, name='dashboard'),

    # Autres URLs de l'app authentification
    path('auth/', include('authentification.urls')),
)
