from django.shortcuts import render, redirect
from .admin import CustomUserCreationForm
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt
def register(request):
    form = CustomUserCreationForm()
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_valid = False
            user.save()
            messages.success(request, 'Cadastro realizado com sucesso! Faça login para começar.')
            return redirect('login')  # Redireciona para a página de login

        else:
            print('Detalhes de registro inválidos')

    return render(request, "registration/register.html", {"form": form})

