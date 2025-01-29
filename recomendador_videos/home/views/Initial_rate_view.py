from django.http import JsonResponse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from recomendador_videos.home.services import avaliar_video

@method_decorator(login_required, name='dispatch')
class InitialRateVideoView(View):
    def post(self, request):
        video_id = request.POST.get('video_id')
        user = request.user

        if video_id:
            _, message = avaliar_video(video_id, user, rating_value=0)  # Salva como avaliação inicial
            return JsonResponse({'message': message}, status=200)

        return JsonResponse({'message': 'Dados inválidos.'}, status=400)
