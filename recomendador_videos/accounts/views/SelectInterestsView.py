from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from ..models import UserProfile, Interest
from ..forms import InterestForm

class SelectInterestsView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    form_class = InterestForm
    template_name = 'apps/account/select_interests.html'
    success_url = reverse_lazy('home')

    def get_object(self):
        return self.request.user.userprofile 

    def form_valid(self, form):
        # Adiciona nova área de interesse se fornecida
        new_interest = form.cleaned_data.get('new_interest')
        if new_interest:
            # Cria uma nova instância de Interest se ela não existir
            interest, created = Interest.objects.get_or_create(name=new_interest)
            # Adiciona a nova área de interesse ao perfil do usuário
            form.instance.interests.add(interest)

        # Salva as áreas de interesse selecionadas
        return super().form_valid(form)
