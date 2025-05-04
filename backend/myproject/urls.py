# myproject/urls.py
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('playersapp.urls')),  # URLs tradicionais
    path('register/', include('accounts.urls')),
    path('api/', include('playersapp.api_urls')),  # URLs da API
    path('api-auth/', include('rest_framework.urls')),  # Login para a API
    path("accounts/", include("django.contrib.auth.urls")),  # accounts
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'), 
]