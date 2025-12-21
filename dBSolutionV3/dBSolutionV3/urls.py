
"""from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.shortcuts import redirect
from django.http import HttpResponse

def home_view(request):
    return HttpResponse("Bienvenue sur la page home")  # juste pour reverse('home')


from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect"""


from django.contrib import admin
from django.urls import path

urlpatterns = [
    path("admin/", admin.site.urls),
]


"""URLs globales (hors i18n)
urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('', lambda request: redirect('/admin/')),  # racine -> admin global
    path('admin/', admin.site.urls),               # admin hors i18n
    path('__reload__/', include('django_browser_reload.urls')),
]

# URLs traduisibles
urlpatterns += i18n_patterns(
    path('', home_view, name='home'),
    # path('dashboard/', views.dashboard, name='dashboard'),  # à activer si besoin
    path('accounts/', include('django.contrib.auth.urls')),
)
"""