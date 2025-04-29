# myapp/api_urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from playersapp.api import FuncionarioViewSet, ScrumMastersAPIView

router = DefaultRouter()
router.register(r'funcionarios', FuncionarioViewSet, basename='funcionario')

urlpatterns = [
    path('', include(router.urls)),
    path('funcionarios/scrummasters/',  ScrumMastersAPIView.as_view(), name='funcionarios-scrummasters' ),
]