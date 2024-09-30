from django.http import JsonResponse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from recomendador_videos.home.services import avaliar_video
from django.http import JsonResponse

@method_decorator(login_required, name='dispatch')
class RateVideoView(View):
    def post(self, request, video_id):
        rating_value = int(request.POST.get('rating'))  # 1 para curtir, -1 para não curtir
        video_rating, message = avaliar_video(video_id, request.user, rating_value)

        if video_rating is None:
            return JsonResponse({'message': message}, status=404)

        return JsonResponse({'message': message})