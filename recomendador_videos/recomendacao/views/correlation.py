from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
import pandas as pd
from django.contrib.auth.models import User
from recomendador_videos.youtube_integration.models import Video
from ..models import VideoInteraction
from ..services.similaridade import calcular_similaridade_usuarios

class UserCorrelationView(LoginRequiredMixin, UserPassesTestMixin, View):
    """
    View para exibir e calcular a correlação entre usuários com base em suas interações com vídeos.
    Requer login e que o usuário seja administrador.
    """
    template_name = 'apps/recomendacao/user_correlation.html'
    login_url = 'login'  
    redirect_field_name = 'next'  

    def test_func(self):
        """
        Verifica se o usuário é administrador.
        """
        return self.request.user.is_staff

    def get(self, request):
        """
        Obtém e exibe as correlações e estatísticas de interação entre usuários.
        """
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

        # Calcula a similaridade e ajusta para dicionário
        similaridade_cosseno = calcular_similaridade_usuarios(request.user, metodo="cosseno")
        similaridade_pearson = calcular_similaridade_usuarios(request.user)

        # Mapeia os nomes dos usuários com base nos IDs
        similaridade_cosseno_dict = {User.objects.get(id=user_id).username: score for user_id, score in similaridade_cosseno.items()}
        similaridade_pearson_dict = {User.objects.get(id=user_id).username: score for user_id, score in similaridade_pearson.items()}

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
        """
        Gera e exporta um arquivo CSV com as correlações de todos os usuários.
        """
        users = User.objects.all()
        data = []
        
        for user in users:
            user_correlations = calcular_similaridade_usuarios(user)
            for similar_user_id, score in user_correlations.items():
                similar_user = User.objects.get(id=similar_user_id)
                data.append([user.username, similar_user.username, score])
        
        df = pd.DataFrame(data, columns=['Usuário', 'Usuário Semelhante', 'Correlação'])
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="user_correlations.csv"'
        df.to_csv(path_or_buf=response, index=False)
        
        return response
