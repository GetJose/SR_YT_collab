from django.shortcuts import render
from django.views import View
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from googleapiclient.errors import HttpError
from httplib2 import ServerNotFoundError
from .services.search_service import busca_YT, filtrar_e_ranquear_videos, buscar_videos_local
from recomendador_videos. recomendacao.services.avaliar import  obter_avaliacoes_do_usuario 

class VideoSearchView(LoginRequiredMixin, View):
    """
    View para buscar vídeos no YouTube com base em uma palavra-chave.
    A busca é feita usando a API do YouTube, e os vídeos retornados são filtrados e ranqueados
    conforme as preferências do perfil do usuário. Os resultados são paginados para melhor navegação.
    Atributos:
        template_name (str): Caminho do template para exibir os resultados da busca.
        videos_per_page (int): Número de vídeos exibidos por página.
    Métodos:
        get: Processa a busca e exibe os resultados paginados, aplicando os filtros do perfil do usuário.
    """
    template_name = 'apps/youtube/video_search.html'
    videos_per_page = 12
    login_url = '/login/'
    redirect_field_name = 'next' 

    def get(self, request):
        """
        Processa a requisição GET para buscar vídeos, filtrar, ranquear e paginar os resultados.
        Args:
            request (HttpRequest): Requisição HTTP contendo a palavra-chave e o número da página.
        Returns:
            HttpResponse: Página renderizada com os vídeos encontrados, avaliações do usuário e informações de paginação.
        """
        try:
            user_profile = request.user.userprofile  
        except AttributeError:
            messages.error(request, "Perfil do usuário não encontrado. Complete o cadastro para buscar vídeos.")
            return render(request, self.template_name, {'videos': [], 'user_ratings': {}})

        query = request.GET.get('query')  
        page_number = request.GET.get('page', 1)
        videos = []

        if query:
            try:
                videos = busca_YT(query, max_results=50)
            except ServerNotFoundError:
                messages.error(request, "Não foi possível conectar ao YouTube. Verifique sua conexão com a internet ou tente novamente mais tarde.")
                videos = list(buscar_videos_local(query))
            except HttpError as e:
                if e.resp.status == 403:
                    messages.warning(request, "O limite de requisições para o YouTube foi atingido. Exibindo vídeos locais.")
                    videos = list(buscar_videos_local(query))
                else:
                    messages.error(request, "Ocorreu um erro ao buscar vídeos. Tente novamente mais tarde.")
                    videos = []

        videos_ranqueados = filtrar_e_ranquear_videos(videos, user_profile)
        user_ratings = obter_avaliacoes_do_usuario(request.user, videos_ranqueados)
        
        paginator = Paginator(videos_ranqueados, self.videos_per_page)
        page_obj = paginator.get_page(page_number)

        return render(request, self.template_name, {
            'videos': page_obj,
            'user_ratings': user_ratings,
            'query': query,
            'paginator': paginator,
            'page_obj': page_obj,
        })
