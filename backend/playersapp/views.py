from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import FuncionarioForm

def home(request):
    return HttpResponse("Bem-vindo ao meu site!")

def funcionario_sucesso(request):
    return render(request, 'funcionario_sucesso.html')


def cadastrar_funcionario(request):
    if request.method == 'POST':
        form = FuncionarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('funcionario_sucesso')  # você pode redirecionar para uma página de sucesso
    else:
        form = FuncionarioForm()
    
    return render(request, 'cadastrar_funcionario.html', {'form': form})
