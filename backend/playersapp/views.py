from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import FuncionarioForm
from .models import Funcionario

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


