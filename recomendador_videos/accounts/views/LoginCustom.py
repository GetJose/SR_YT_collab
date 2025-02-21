from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.contrib.auth import authenticate
from django.shortcuts import redirect

class CustomLoginView(LoginView):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')  # Nome da URL da home
        return super().dispatch(request, *args, **kwargs)

    def form_invalid(self, form):
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')

        user = authenticate(self.request, username=username, password=password)

        if user and not user.is_active:
            messages.error(self.request, "Conta ainda inativa. Verifique seu e-mail para ativá-la.")
        else:
            messages.error(self.request, "Nome de usuário ou senha incorretos.")  # Mensagem padrão

        return super().form_invalid(form)
