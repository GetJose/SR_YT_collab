from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect

class CustomPasswordChangeView(PasswordChangeView):
    """
    View personalizada para alterar a senha do usuário logado.

    Após a alteração bem-sucedida, exibe uma mensagem de sucesso e redireciona para a página de perfil.

    Atributos:
        template_name (str): Caminho do template de alteração de senha.
        success_url (str): URL de redirecionamento após a alteração da senha.

    Métodos:
        form_valid: Manipula o formulário válido, salva a nova senha e exibe uma mensagem de sucesso.
    """
    template_name = "apps/account/change_password.html"
    success_url = reverse_lazy("profile")  

    def form_valid(self, form):
        """
        Manipula o formulário de alteração de senha válido.

        Exibe uma mensagem de sucesso e redireciona o usuário para a URL de sucesso definida.

        Args:
            form (PasswordChangeForm): Formulário de alteração de senha validado.

        Returns:
            HttpResponseRedirect: Redirecionamento para a URL de sucesso.
        """
        response = super().form_valid(form)
        messages.success(self.request, "Senha alterada com sucesso!")  
        return response
