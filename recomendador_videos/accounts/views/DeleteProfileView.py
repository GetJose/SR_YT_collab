from django.views.generic import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.models import User

class DeleteProfileView(LoginRequiredMixin, DeleteView):
    """
    View para excluir o perfil do usuário logado.
    Requer que o usuário esteja autenticado. Ao confirmar a exclusão, o usuário será redirecionado para a página inicial.
    Atributos:
        model (User): Modelo de usuário que será excluído.
        template_name (str): Caminho do template de confirmação de exclusão.
        success_url (str): URL de redirecionamento após a exclusão.
    """
    model = User
    template_name = 'apps/account/delete_confirm.html' 
    success_url = reverse_lazy('home')

    def get_object(self):
        """
        Obtém o objeto do usuário logado para exclusão.
        Returns:
            User: Objeto do usuário autenticado.
        """
        return self.request.user
