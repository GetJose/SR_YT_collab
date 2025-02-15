import json
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
import pandas as pd
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from recomendador_videos.youtube_integration.models import Video
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import VideoInteraction
from django.db.models import F, Max

from .services_ import (
    recomendar_videos_user_based,
    recomendar_videos_itens_based,
    recomendar_videos_hibrido,
    calcular_similaridade_cosseno,
    calcular_correlacao_pearson,
    recomendar_videos_fusao
)

@method_decorator(login_required, name='dispatch')
class ItemRecommendationView(View):
    template_name = 'apps/recomendacao/item_recommendation.html'

    def get(self, request):
        videos_recomendados = recomendar_videos_itens_based(request.user)
        
        return render(request, self.template_name, {
            'videos': videos_recomendados,
        })

@method_decorator(login_required, name='dispatch')
class UserRecommendationView(View):
    template_name = 'apps/recomendacao/user_recommendation.html'

    def get(self, request):
        videos_recomendados = recomendar_videos_user_based(request.user)
        
        return render(request, self.template_name, {
            'videos': videos_recomendados,
        })

@method_decorator(login_required, name='dispatch')
class HybridRecommendationView(View):
    template_name = 'apps/recomendacao/hybrid_recommendation.html'

    def get(self, request):
        metodo = request.GET.get('metodo', 'cosseno')
        similaridade = (
            calcular_similaridade_cosseno if metodo == 'cosseno' else calcular_correlacao_pearson
        )
        videos_recomendados = recomendar_videos_hibrido(request.user, similaridade)
        
        return render(request, self.template_name, {
            'videos': videos_recomendados,
            'metodo': metodo,
        })


@method_decorator(user_passes_test(lambda u: u.is_staff), name='dispatch')
class UserCorrelationView(View):
    template_name = 'apps/recomendacao/user_correlation.html'

    def get(self, request):
        user = request.user
      
        selected_user_id_1 = request.GET.get('selected_user_1')
        selected_user_id_2 = request.GET.get('selected_user_2')

        total_videos_assistidos_user_1 = total_videos_assistidos_user_2 = 0
        common_videos = common_positive_ratings = None
        selected_user_1 = selected_user_2 = None

        if selected_user_id_1 and selected_user_id_2:
            try:
                selected_user_1 = User.objects.get(id=selected_user_id_1)
                selected_user_2 = User.objects.get(id=selected_user_id_2)

                ratings_user_1 = VideoInteraction.objects.filter(user=selected_user_1).values('video_id')
                ratings_user_2 = VideoInteraction.objects.filter(user=selected_user_2).values('video_id')

                total_videos_assistidos_user_1 = ratings_user_1.count()
                total_videos_assistidos_user_2 = ratings_user_2.count()

                common_videos = set(ratings_user_1.values_list('video_id', flat=True)) & set(ratings_user_2.values_list('video_id', flat=True))

                positive_ratings_user_1 = set(ratings_user_1.filter(rating=1).values_list('video_id', flat=True))
                positive_ratings_user_2 = set(ratings_user_2.filter(rating=1).values_list('video_id', flat=True))
                common_positive_ratings = positive_ratings_user_1 & positive_ratings_user_2
            except User.DoesNotExist:
                pass  

        similaridade_cosseno = calcular_similaridade_cosseno(user)
        similaridade_pearson = calcular_correlacao_pearson(user)

        similaridade_com_nomes_cosseno = similaridade_cosseno.index.map(lambda user_id: User.objects.get(id=user_id).username)
        similaridade_cosseno_dict = dict(zip(similaridade_com_nomes_cosseno, similaridade_cosseno.values))

        similaridade_com_nomes_pearson = similaridade_pearson.index.map(lambda user_id: User.objects.get(id=user_id).username)
        similaridade_pearson_dict = dict(zip(similaridade_com_nomes_pearson, similaridade_pearson.values))

        return render(request, self.template_name, {
            'similaridade_cosseno': similaridade_cosseno_dict,
            'similaridade_pearson': similaridade_pearson_dict,
            'total_videos_assistidos_user_1': total_videos_assistidos_user_1,
            'total_videos_assistidos_user_2': total_videos_assistidos_user_2,
            'common_videos': common_videos,
            'common_positive_ratings': common_positive_ratings,
            'users': User.objects.all(), 
            'selected_user_1': selected_user_1,  
            'selected_user_2': selected_user_2,
        })

    def post(self, request):
        users = User.objects.all()
        data = []
        
        for user in users:
            user_correlations = calcular_correlacao_pearson(user)
            for similar_user_id, score in user_correlations.items():
                similar_user = User.objects.get(id=similar_user_id)
                data.append([user.username, similar_user.username, score])
        
        df = pd.DataFrame(data, columns=['Usuário', 'Usuário Semelhante', 'Correlação'])
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="user_correlations.csv"'
        df.to_csv(path_or_buf=response, index=False)
        
        return response

    
@method_decorator(login_required, name='dispatch')
class VideoRecommendation(View):
    template_name = 'apps/recomendacao/recomendacao_hibrida.html'

    def get(self, request):
        user = request.user
        recomendacoes_hibridas = recomendar_videos_fusao(user)

        videos_curtidos = VideoInteraction.objects.filter(user=user, rating=1).values_list('video_id', flat=True)

        return render(request, self.template_name, {
            'videos': recomendacoes_hibridas,  # Cada vídeo tem o atributo 'method'
            'rated_videos': videos_curtidos,
        })

    
class VideoMarked(View):
    @csrf_exempt
    def register_interaction(request):
        if request.method == 'POST':
            data = json.loads(request.body)
            video_id = data.get('video_id')
            rating = data.get('rating')
            method = data.get('method')

            if video_id and rating and method:
                video = Video.objects.get(youtube_id=video_id)
                interaction = VideoInteraction.objects.create(
                    user=request.user,
                    video=video,
                    rating=int(rating),
                    method=method
                )
                return JsonResponse({'status': 'success', 'message': 'Interação registrada com sucesso.'})

        return JsonResponse({'status': 'error', 'message': 'Dados inválidos.'}, status=400)
