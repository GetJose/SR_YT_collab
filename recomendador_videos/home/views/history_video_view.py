from django.shortcuts import render
from django.core.paginator import Paginator 
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from recomendador_videos.youtube_integration.models import Video
from ..models import VideoRating

@method_decorator(login_required, name='dispatch')
class VideoHistoryView(ListView):
    template_name = 'apps/home/video_history.html' 
    paginate_by = 9

    def get(self, request):
        user_ratings = VideoRating.objects.filter(user=request.user)
        if user_ratings.exists():
            video_ids = user_ratings.values_list('video_id', flat=True)
            videos = Video.objects.filter(id__in=video_ids)
            query = request.GET.get('query')
            if query:
                videos = videos.filter(title__icontains=query) 

            paginator = Paginator(videos, self.paginate_by)
            page = request.GET.get('page')
            videos_paginated = paginator.get_page(page)
            return render(request, self.template_name, {
                'videos_history': videos_paginated,
                'user_ratings': {rating.video.youtube_id: rating.rating for rating in user_ratings},
            })
        else:
           
            return render(request, self.template_name, {
                'videos_history': [], 
                'user_ratings': {},
            })
