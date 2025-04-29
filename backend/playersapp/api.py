# minhaapp/api.py
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.decorators import action
from playersapp.models import Funcionario
from playersapp.serializers import FuncionarioSerializer

class FuncionarioViewSet(viewsets.ModelViewSet):
    queryset = Funcionario.objects.all()
    serializer_class = FuncionarioSerializer

    @action(detail=False, methods=['get'])
    def scrum_masters(self, request):
        funcionarios = Funcionario.objects.filter(ex_scrum_master=True)
        serializer = self.get_serializer(funcionarios, many=True)
        return Response(serializer.data)

class ScrumMastersAPIView(generics.ListAPIView):
    serializer_class = FuncionarioSerializer

    def get_queryset(self):
        return Funcionario.objects.filter(ex_scrum_master=True)