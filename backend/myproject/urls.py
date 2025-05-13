# myproject/urls.py
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views  # Importação necessária para LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', include('playersapp.urls')),  # Inclui as rotas do aplicativo playersapp
    path('register/', include('accounts.urls')),
    path('api/', include('playersapp.api_urls')),  # URLs da API
    path('api-auth/', include('rest_framework.urls')),  # Login para a API
    path("accounts/", include("django.contrib.auth.urls")),  # accounts
]