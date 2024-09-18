from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login

class RegisterView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'apps/auth/register.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Faz login automático após o registro
            return redirect('home')  # Redireciona para a página inicial
        return render(request, 'apps/auth/register.html', {'form': form})