from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from ..models import UserProfile
from ..forms import UserProfileEditForm, InterestForm

class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    """
    View para atualizar o perfil do usuário logado.
    Permite editar as informações do perfil e os interesses, garantindo que 
    apenas o próprio usuário possa fazer alterações.
    """
    model = UserProfile
    form_class = UserProfileEditForm
    template_name = 'apps/account/edit_profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        """
        Obtém o objeto do perfil do usuário logado.
        Returns:
            UserProfile: Perfil do usuário autenticado.
        """
        return self.request.user.userprofile  

    def get_form(self, form_class=None):
        """
        Configura o formulário de edição do perfil para incluir o usuário logado.
        Args:
            form_class (Form, opcional): Classe do formulário.
        Returns:
            Form: Formulário preenchido com os dados do usuário.
        """
        form = super().get_form(form_class)
        form.__init__(user=self.request.user, **self.get_form_kwargs())  # Passa o usuário
        return form

    def get_context_data(self, **kwargs):
        """
        Adiciona o formulário de interesses ao contexto.
        Args:
            **kwargs: Argumentos de contexto adicionais.
        Returns:
            dict: Contexto atualizado com o formulário de interesses.
        """
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['interest_form'] = InterestForm(self.request.POST, instance=self.get_object())
        else:
            context['interest_form'] = InterestForm(instance=self.get_object())
        return context

    def form_valid(self, form):
        """
        Processa o formulário se for válido, salvando o perfil e os interesses.
        Args:
            form (Form): Formulário de edição do perfil.
        Returns:
            HttpResponseRedirect: Redirecionamento para a URL de sucesso.
        """
        context = self.get_context_data()
        interest_form = context['interest_form']

        if interest_form.is_valid():
            self.object = form.save()
            interest_form.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)
