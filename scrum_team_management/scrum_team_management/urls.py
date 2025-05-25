from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('projects/', include('projects.urls')),
    path('teams/', include('teams.urls')),
    path('users/', include('users.urls')),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('', lambda request: redirect('login')),  # or any default view
]