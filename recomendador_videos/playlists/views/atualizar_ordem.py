import json
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from ..models import PlaylistVideo

class AtualizarOrdemVideosView(LoginRequiredMixin, View):
    """
    View para atualizar a ordem dos vídeos em uma playlist.
    Permite que o usuário logado reordene os vídeos arrastando ou movendo os itens.  
    A atualização é feita via requisição POST com a nova ordem enviada em JSON.
    """
    def post(self, request):
        """
        Processa a requisição para atualizar a ordem dos vídeos.
        Recebe a nova ordem como uma lista de IDs e atualiza os vídeos da playlist.  
        Cada vídeo recebe um novo valor para o campo `ordem`.
        Args:
            request (HttpRequest): A requisição HTTP contendo a nova ordem dos vídeos.
        Returns:
            JsonResponse: Resposta JSON com o status da operação.
        """
        try:
            data = json.loads(request.body)
            ordem_videos = data.get('ordem', [])

            for index, pv_id in enumerate(ordem_videos):
                pv = get_object_or_404(PlaylistVideo, id=pv_id, playlist__usuario=request.user)
                pv.ordem = index
                pv.save()

            return JsonResponse({"status": "success", "message": "Ordem atualizada com sucesso!"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
