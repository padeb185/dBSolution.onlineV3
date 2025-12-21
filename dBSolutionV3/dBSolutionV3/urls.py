from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from dBSolutionV3.views import home, dashboard, login
from django.contrib.auth import views as auth_views

# Routes principales
urlpatterns = [
    # Login accessible pour tous (utilisateurs normaux)
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),

    # Admin Django (optionnel, si tu veux garder l'accès)
    path('admin/', admin.site.urls),

    # Auth routes standard (logout, password reset, etc.)
    path('accounts/', include('django.contrib.auth.urls')),
]

# URLs traduisibles
urlpatterns += i18n_patterns(
    path('', login, name='login_home'),       # racine → login personnalisé
    path('dashboard/', dashboard, name='dashboard'),  # dashboard si besoin
    path('home/', home, name='home'),         # home view si besoin
)
