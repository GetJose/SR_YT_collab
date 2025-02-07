from django.shortcuts import render
from django.views import View
from recomendador_videos.youtube_integration.models import Video
from ..services.object_recomendation import get_similar_videos, get_tsne_cluster_data

class ObjectRecommendationView(View):
    template_name = 'apps/recomendacao/object_recommendation.html'

    def get(self, request):
        videos = Video.objects.all()
        cluster_data = get_tsne_cluster_data()
        return render(request, self.template_name, {'videos': videos, "cluster_data": cluster_data})

    def post(self, request):
        video_id = int(request.POST.get('video_id'))
        video_base = Video.objects.get(id=video_id)
        similar_videos = get_similar_videos(video_base)
        cluster_data = get_tsne_cluster_data(selected_video_id=video_id)

        return render(request, self.template_name, {
            'videos': Video.objects.all(),
            "video_base": video_base,
            "similar_videos": similar_videos,
            "cluster_data": cluster_data
        })