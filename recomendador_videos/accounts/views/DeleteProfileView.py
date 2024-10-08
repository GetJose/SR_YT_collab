from django.views.generic import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.models import User

class DeleteProfileView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'apps/account/delete_confirm.html'  # Confirmação de deleção
    success_url = reverse_lazy('home')

    def get_object(self):
        return self.request.user
