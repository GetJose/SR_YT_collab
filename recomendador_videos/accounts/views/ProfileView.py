from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from ..forms import UserProfileFilterForm
from ..models import UserProfile

class ProfileView(LoginRequiredMixin, DetailView):
    """
    View para exibir e atualizar o perfil do usuário logado.
    Permite visualizar os detalhes do perfil e editar as preferências diretamente.
    """
    model = UserProfile
    template_name = 'apps/account/profile.html'

    def get(self, request, *args, **kwargs):
        """
        Renderiza a página de perfil com os dados atuais do usuário.
        Também carrega as linguagens preferidas, ajustando a lista inicial do formulário.
        Args:
            request (HttpRequest): A requisição HTTP recebida.
            *args: Argumentos posicionais adicionais.
            **kwargs: Argumentos nomeados adicionais.
        Returns:
            HttpResponse: Página de perfil renderizada com o formulário preenchido.
        """
        user_profile = request.user.userprofile
        form = UserProfileFilterForm(instance=user_profile)

        linguagens_preferidas = user_profile.linguagens_preferidas
        if linguagens_preferidas:
            linguagens_list = linguagens_preferidas.split(',')
            form.initial['linguagens_preferidas'] = linguagens_list 
        
        return render(request, 'apps/account/profile.html', {'form': form, 'user': request.user})

    def post(self, request, *args, **kwargs):
        """
        Processa a submissão do formulário para atualizar os filtros do perfil.
        Se o formulário for válido, salva as alterações e redireciona para a página do perfil.
        Caso contrário, recarrega a página com os erros do formulário.
        Args:
            request (HttpRequest): A requisição HTTP contendo os dados do formulário.
            *args: Argumentos posicionais adicionais.
            **kwargs: Argumentos nomeados adicionais.
        Returns:
            HttpResponseRedirect: Redireciona para a página do perfil após salvar.
            HttpResponse: Página de perfil renderizada com os erros, se houver.
        """
        user_profile = request.user.userprofile
        form = UserProfileFilterForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
        return render(request, 'apps/account/profile.html', {'form': form, 'user': request.user})
