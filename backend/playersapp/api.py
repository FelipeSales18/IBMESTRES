# minhaapp/api.py
from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
import random
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

    @action(detail=False, methods=['post'])
    def gerar_equipes(self, request):
        numero_equipes = request.data.get('numero_equipes')
        pessoas_por_equipe = request.data.get('pessoas_por_equipe')

        # Validação dos parâmetros
        if not numero_equipes or not pessoas_por_equipe:
            raise ValidationError("Os campos 'numero_equipes' e 'pessoas_por_equipe' são obrigatórios.")
        
        try:
            numero_equipes = int(numero_equipes)
            pessoas_por_equipe = int(pessoas_por_equipe)
        except ValueError:
            raise ValidationError("Os campos 'numero_equipes' e 'pessoas_por_equipe' devem ser números inteiros.")

        if numero_equipes <= 0 or pessoas_por_equipe <= 0:
            raise ValidationError("Os valores de 'numero_equipes' e 'pessoas_por_equipe' devem ser maiores que zero.")

        # Obter todos os funcionários
        funcionarios = list(Funcionario.objects.all())
        random.shuffle(funcionarios)  # Embaralhar a lista de funcionários

        # Gerar as equipes
        equipes = []
        for i in range(numero_equipes):
            equipe = funcionarios[:pessoas_por_equipe]
            funcionarios = funcionarios[pessoas_por_equipe:]
            equipes.append(equipe)

            if not funcionarios:  # Se não houver mais funcionários, parar
                break

        # Serializar as equipes
        equipes_serializadas = [
            FuncionarioSerializer(equipe, many=True).data for equipe in equipes
        ]

        return Response({'equipes': equipes_serializadas}, status=status.HTTP_200_OK)

class ScrumMastersAPIView(generics.ListAPIView):
    serializer_class = FuncionarioSerializer

    def get_queryset(self):
        return Funcionario.objects.filter(ex_scrum_master=True)


