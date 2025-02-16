import json
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from ..models import PlaylistVideo

class AtualizarOrdemVideosView(LoginRequiredMixin, View):
    def post(self, request):
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
