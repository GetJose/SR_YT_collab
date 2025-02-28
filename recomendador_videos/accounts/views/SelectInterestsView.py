from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from ..models import UserProfile, Interest
from ..forms import InterestForm

class SelectInterestsView(LoginRequiredMixin, UpdateView):
    """
    View para selecionar e atualizar os interesses do usuário logado.
    Atributos:
        model (UserProfile): Modelo de perfil do usuário.
        form_class (InterestForm): Formulário para edição dos interesses.
        template_name (str): Caminho do template para seleção de interesses.
        success_url (str): URL para redirecionamento após salvar os interesses.
    """
    model = UserProfile
    form_class = InterestForm
    template_name = 'apps/account/select_interests.html'
    success_url = reverse_lazy('home')

    def get_object(self):
        """
        Obtém o objeto do perfil do usuário logado.
        Returns:
            UserProfile: Perfil do usuário autenticado.
        """
        return self.request.user.userprofile

    def form_valid(self, form):
        """
        Processa o formulário de interesses, adicionando novos se necessário.
        Verifica se o usuário inseriu novos interesses, cria e adiciona ao perfil.
        Args:
            form (InterestForm): Formulário validado com os interesses do usuário.
        Returns:
            HttpResponseRedirect: Redireciona para a URL de sucesso após salvar os interesses.
        """
        new_interest_text = form.cleaned_data.get('new_interests')
        if new_interest_text:
            interest, created = Interest.objects.get_or_create(name=new_interest_text)
            form.instance.interests.add(interest)

        return super().form_valid(form)
