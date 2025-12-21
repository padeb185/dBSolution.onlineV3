from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.shortcuts import redirect
from dBSolutionV3.views import home, dashboard, login

# urls.py
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
]

"""
urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('', lambda request: redirect('/admin/')),  # racine -> admin global
    path('admin/', admin.site.urls),               # admin hors i18n
    path('__reload__/', include('django_browser_reload.urls')),
]
"""
# URLs traduisibles
urlpatterns += i18n_patterns(
    path('', login),
    path('login', login),
    path('', home, name='home'),

    path('dashboard/', dashboard, name='dashboard'),  # à activer si besoin
    path('accounts/', include('django.contrib.auth.urls')),
)
