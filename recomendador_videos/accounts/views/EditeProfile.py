from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from ..models import UserProfile
from ..forms import UserProfileEditForm, InterestForm

class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    form_class = UserProfileEditForm
    template_name = 'apps/account/edit_profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user.userprofile  # Obtém o perfil do usuário logado

    def get_form(self, form_class=None):
        """Garante que o usuário logado seja passado para o formulário"""
        form = super().get_form(form_class)
        form.__init__(user=self.request.user, **self.get_form_kwargs())  # Passa o usuário
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['interest_form'] = InterestForm(self.request.POST, instance=self.get_object())
        else:
            context['interest_form'] = InterestForm(instance=self.get_object())
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        interest_form = context['interest_form']

        if interest_form.is_valid():
            self.object = form.save()
            interest_form.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)
