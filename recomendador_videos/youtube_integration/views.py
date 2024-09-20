from django.shortcuts import render
from django.views import View
from .services import busca_YT

# Função de busca, mantendo a integração com a model


# A view que utiliza a nova função de busca com integração à model Video
class VideoSearchView(View):
    template_name = 'apps/youtube/video_search.html'

    def get(self, request):
        query = request.GET.get('query')  # Obtém o termo de busca do usuário
        videos = []

        if query:
            # Chama a função busca_YT para realizar a busca e integrar com a model Video
            videos = busca_YT(query)

        return render(request, self.template_name, {'videos': videos, 'query': query})
