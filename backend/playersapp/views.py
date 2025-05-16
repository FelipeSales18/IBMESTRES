from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .forms import FuncionarioForm, AssociarEquipeForm, ProjetoForm, EquipeForm
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

class EquipeListView(LoginRequiredMixin, ListView):
    model = Equipe
    template_name = 'listar_equipes.html'
    context_object_name = 'equipes'

class EquipeCreateView(LoginRequiredMixin, CreateView):
    model = Equipe
    form_class = EquipeForm
    template_name = 'associar_equipe.html'
    success_url = reverse_lazy('listar_equipes')

class EquipeUpdateView(LoginRequiredMixin, UpdateView):
    model = Equipe
    form_class = EquipeForm
    template_name = 'associar_equipe.html'
    success_url = reverse_lazy('listar_equipes')

class EquipeDeleteView(LoginRequiredMixin, DeleteView):
    model = Equipe
    template_name = 'excluir_equipe.html'
    success_url = reverse_lazy('listar_equipes')

class EquipeDetailView(LoginRequiredMixin, DetailView):
    model = Equipe
    template_name = 'detalhes_equipe.html'
    context_object_name = 'equipe'

def detalhes_equipe(request, equipe_id):
    # Recupera a equipe pelo ID ou retorna 404 se não existir
    equipe = get_object_or_404(Equipe, id=equipe_id)
    
    # Renderiza a página com os detalhes da equipe
    return render(request, 'detalhes_equipe.html', {'equipe': equipe})

@login_required
def listar_projetos(request):
    funcionario = Funcionario.objects.filter(user=request.user).first()
    print("Funcionario:", funcionario)
    print("is_staff:", request.user.is_staff)
    if not funcionario or not request.user.is_staff:
        return HttpResponse("Você não é líder ou não está vinculado a um funcionário.")
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

def set_leader_permissions(user, full_name):
    role = user.groups.values_list('name', flat=True).first()  # Obtém o nome do primeiro grupo do usuário

    if role == 'leader':
        user.is_staff = True
        user.save()
        Funcionario.objects.create(
            user=user,
            nome=full_name,
            idade=0,
            hard_skils="",
            soft_skils="",
        )


