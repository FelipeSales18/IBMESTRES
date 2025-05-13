from django.shortcuts import render, redirect
from .admin import CustomUserCreationForm
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from playersapp.models import Funcionario

# Create your views here.
@csrf_exempt
def register(request):
    form = CustomUserCreationForm()
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            # Cria o usuário na tabela auth_user
            user = form.save(commit=False)
            role = form.cleaned_data['role']
            full_name = form.cleaned_data['full_name']
            user.first_name = full_name.split()[0]
            user.last_name = " ".join(full_name.split()[1:])
            user.save()

            # Cria o registro correspondente na tabela playersapp_funcionario
            if role == 'leader':
                user.is_staff = True
                user.save()
                Funcionario.objects.create(
                    user=user,
                    nome=full_name,
                    idade=0,  # Líderes podem não ter idade definida
                    hard_skils="",
                    soft_skils="",
                )
            elif role == 'collaborator':
                Funcionario.objects.create(
                    user=user,
                    nome=full_name,
                    idade=form.cleaned_data['idade'],
                    hard_skils=form.cleaned_data['hard_skils'],
                    soft_skils=form.cleaned_data['soft_skils'],
                    ex_developer=form.cleaned_data['ex_developer'],
                    ex_product_owner=form.cleaned_data['ex_product_owner'],
                    ex_scrum_master=form.cleaned_data['ex_scrum_master'],
                )

            messages.success(request, 'Cadastro realizado com sucesso! Faça login para começar.')
            return redirect('login')

    return render(request, "registration/register.html", {"form": form})

