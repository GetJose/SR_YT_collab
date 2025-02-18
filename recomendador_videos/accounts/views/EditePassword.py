from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect

class CustomPasswordChangeView(PasswordChangeView):
    template_name = "apps/account/change_password.html"
    success_url = reverse_lazy("profile")  # Redireciona para o perfil após alteração bem-sucedida

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Senha alterada com sucesso!")  # Mensagem de sucesso
        return response
