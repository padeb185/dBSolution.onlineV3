from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from dBSolutionV3 import views
from django.contrib.auth import views as auth_views
from authentification.views import login_totp, totp_setup

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
]

urlpatterns += i18n_patterns(
    # Admin
    path("admin/", admin.site.urls),

    # Pages de login / TOTP
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('login/totp/', login_totp, name='login_totp'),
    path('login/totp/setup/', totp_setup, name='totp_setup'),

    # Dashboard / home
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # Inclure toutes les autres URLs de l’app authentification
    path('', include('authentification.urls')),
)
