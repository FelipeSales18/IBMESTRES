from django.contrib.auth.models import User
from django.db import models

class Funcionario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    nome = models.CharField(max_length=100)
    idade = models.IntegerField()
    hard_skils = models.CharField(max_length=300)
    soft_skils = models.CharField(max_length=300)
    ex_developer = models.BooleanField(default=False)
    ex_product_owner = models.BooleanField(default=False)
    ex_scrum_master = models.BooleanField(default=False)
    foto = models.ImageField(upload_to='fotos_perfil/', null=True, blank=True)  # Novo campo

    def __str__(self):
        return self.nome

class Equipe(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True)
    lider = models.ForeignKey('Funcionario', on_delete=models.SET_NULL, null=True, blank=True, related_name='equipes_lideradas')
    colaboradores = models.ManyToManyField('Funcionario', related_name='equipes')

    def __str__(self):
        return self.nome

class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Nome único da equipe
    members = models.ManyToManyField(User, related_name='teams')  # Membros da equipe

    def __str__(self):
        return self.name

class Projeto(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField(blank=True, null=True)
    lider = models.ForeignKey(Funcionario, on_delete=models.CASCADE, related_name='projetos')
    data_criacao = models.DateTimeField(auto_now_add=True)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name='projects')

    def __str__(self):
        return self.nome

