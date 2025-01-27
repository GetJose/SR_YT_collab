from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from ..forms import UserProfileFilterForm
from ..models import UserProfile

class ProfileView(LoginRequiredMixin, DetailView):
    model = UserProfile
    template_name = 'apps/account/profile.html'

    def get(self, request, *args, **kwargs):
        user_profile = request.user.userprofile
        form = UserProfileFilterForm(instance=user_profile)
        
        # Carregar as linguagens preferidas
        linguagens_preferidas = user_profile.linguagens_preferidas
        if linguagens_preferidas:
            linguagens_list = linguagens_preferidas.split(',')
            form.initial['linguagens_preferidas'] = linguagens_list  # Atualizar o `initial` do campo no formulário
        
        return render(request, 'apps/account/profile.html', {'form': form, 'user': request.user})


    def post(self, request, *args, **kwargs):
        user_profile = request.user.userprofile
        form = UserProfileFilterForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redireciona para a página do perfil após salvar
        return render(request, 'apps/account/profile.html', {'form': form, 'user': request.user})
