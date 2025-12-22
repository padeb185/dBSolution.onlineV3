from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from dBSolutionV3 import views
from django.contrib.auth import views as auth_views
from authentification.views import login_totp

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    # URLs non-traduisibles, si besoin
    # Exemple: admin ou autres
    # path('admin/', admin.site.urls),
]

urlpatterns += i18n_patterns(
    path('', views.home, name='home'),
    path("login/totp/", login_totp, name="login_totp"),
    path('dashboard/', views.dashboard, name='dashboard'),  # /fr/dashboard/
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),  # /fr/login/
)
