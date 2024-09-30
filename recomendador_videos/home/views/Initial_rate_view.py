from django.http import JsonResponse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from recomendador_videos.home.services import avaliacao_inicial

@method_decorator(login_required, name='dispatch')
class InitialRateVideoView(View):
    def post(self, request):  
        video_id = request.POST.get('video_id')
        user = request.user
        if video_id:
            resultado = avaliacao_inicial(user, video_id)

            if resultado:
                return JsonResponse({'message': 'Avaliação inicial salva com sucesso.'}, status=200)
            else:
                return JsonResponse({'message': 'Avaliação já existente.'}, status=400)
        return JsonResponse({'message': 'Dados inválidos.'}, status=400)
