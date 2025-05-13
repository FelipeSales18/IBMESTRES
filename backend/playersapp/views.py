from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import FuncionarioForm, AssociarEquipeForm, ProjetoForm
from .models import Funcionario, Equipe, Projeto

def home(request):
    return render(request, 'base.html')

def funcionario_sucesso(request):
    return render(request, 'funcionario_sucesso.html')

def cadastrar_funcionario(request):
    if request.method == 'POST':
        form = FuncionarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('funcionario_sucesso')
    else:
        form = FuncionarioForm()
    
    return render(request, 'cadastrar_funcionario.html', {'form': form})

def listar_funcionarios(request):
    funcionarios = Funcionario.objects.all()  # Busca todos os funcionários no banco de dados
    return render(request, 'listar_funcionarios.html', {'funcionarios': funcionarios})

def associar_equipe(request):
    if request.method == 'POST':
        form = AssociarEquipeForm(request.POST)
        if form.is_valid():
            funcionario = form.cleaned_data['funcionario']
            equipe = form.cleaned_data['equipe']
            funcionario.equipes.add(equipe)  # Associa a equipe ao colaborador
            return redirect('listar_associacoes')  # Redireciona para a lista de associações
    else:
        form = AssociarEquipeForm()

    return render(request, 'associar_equipe.html', {'form': form})

def listar_associacoes(request):
    funcionarios = Funcionario.objects.all()
    return render(request, 'listar_associacoes.html', {'funcionarios': funcionarios})

def listar_equipes(request):
    equipes = Equipe.objects.all()
    return render(request, 'listar_equipes.html', {'equipes': equipes})

def detalhes_equipe(request, equipe_id):
    # Recupera a equipe pelo ID ou retorna 404 se não existir
    equipe = get_object_or_404(Equipe, id=equipe_id)
    
    # Renderiza a página com os detalhes da equipe
    return render(request, 'detalhes_equipe.html', {'equipe': equipe})

@login_required
def listar_projetos(request):
    # Verifica se o usuário é um líder
    funcionario = Funcionario.objects.filter(user=request.user).first()
    if not funcionario or not request.user.is_staff:
        return redirect('home')  # Redireciona para a página inicial se não for líder

    projetos = Projeto.objects.filter(lider=funcionario)
    return render(request, 'listar_projetos.html', {'projetos': projetos})

@login_required
def criar_projeto(request):
    funcionario = Funcionario.objects.filter(user=request.user).first()
    if not funcionario or not request.user.is_staff:
        return redirect('home')  # Redireciona para a página inicial se não for líder

    if request.method == 'POST':
        form = ProjetoForm(request.POST)
        if form.is_valid():
            projeto = form.save(commit=False)
            projeto.lider = funcionario
            projeto.save()
            return redirect('listar_projetos')
    else:
        form = ProjetoForm()

    return render(request, 'criar_projeto.html', {'form': form})


