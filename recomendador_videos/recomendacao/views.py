import pandas as pd
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from recomendador_videos.recomendacao.services import calcular_correlacao_pearson
from recomendador_videos.home.models import VideoRating
from django.contrib.auth.models import User
from sklearn.metrics.pairwise import cosine_similarity

class UserCorrelationView(View):
    template_name = 'apps/recomendacao/user_correlation.html'

    def get(self, request):
        correlations = {}
        users = User.objects.all()
        for user in users:
            user_correlations = calcular_correlacao_pearson(user)
            correlations[user] = user_correlations
        return render(request, self.template_name, {'correlations': correlations})

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

def calcular_similaridade_cosseno(request):
    user = request.user
    all_ratings = VideoRating.objects.all()

    data = {
        'user_id': [rating.user_id for rating in all_ratings],
        'video_id': [rating.video_id for rating in all_ratings],
        'rating': [rating.rating for rating in all_ratings],
    }
    df_ratings = pd.DataFrame(data)

    ratings_matrix = df_ratings.pivot_table(index='user_id', columns='video_id', values='rating').fillna(0)

    if user.id not in ratings_matrix.index:
        return pd.Series(dtype='float64')

    user_ratings = ratings_matrix.loc[user.id].values.reshape(1, -1)

    similarities = cosine_similarity(user_ratings, ratings_matrix.values).flatten()

    similar_users = pd.Series(similarities, index=ratings_matrix.index).sort_values(ascending=False)
    similaridade = similar_users.drop(user.id)
    similaridade_com_nomes = similaridade.index.map(lambda user_id: User.objects.get(id=user_id).username)

    similaridade_dict = dict(zip(similaridade_com_nomes, similaridade.values))
    return render(request, 'apps/recomendacao/similaridade.html', {'similaridade': similaridade_dict})
