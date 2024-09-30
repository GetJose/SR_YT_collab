import pandas as pd
from recomendador_videos.home.models import VideoRating
from django.contrib.auth.models import User
from recomendador_videos.recomendacao.models import UserSimilarity

def calcular_correlacao_pearson(user):
    all_ratings = VideoRating.objects.all()
    data = {
        'user_id': [rating.user_id for rating in all_ratings],
        'video_id': [rating.video_id for rating in all_ratings],
        'rating': [rating.rating for rating in all_ratings],
    }
    
    df_ratings = pd.DataFrame(data)
    ratings_matrix = df_ratings.pivot_table(index='user_id', columns='video_id', values='rating')

    if user.id not in ratings_matrix.index:
        print(f"Usuário com ID {user.id} não possui avaliações suficientes.")
        return pd.Series()  

    user_ratings = ratings_matrix.loc[user.id]

    correlations = ratings_matrix.corrwith(user_ratings, axis=1, method='pearson')
    correlations = correlations.dropna().sort_values(ascending=False)

    # Preencher a tabela UserSimilarity
    for similar_user_id, similarity_score in correlations.items():
        if similar_user_id != user.id:  # Evitar inserir similaridade do próprio usuário
            UserSimilarity.objects.update_or_create(
                user=user,
                similar_user_id=similar_user_id,
                defaults={'score': similarity_score}  # Corrigido para usar 'score'
            )

    return correlations


def recomendar_videos(user):
    user_correlations = calcular_correlacao_pearson(user)
    similar_users = sorted(user_correlations.items(), key=lambda x: x[1], reverse=True)

    recommended_videos = set()
    for similar_user, score in similar_users:
        if score > 0:
            similar_user_ratings = VideoRating.objects.filter(user=similar_user, rating=1)
            for rating in similar_user_ratings:
                if not VideoRating.objects.filter(user=user, video=rating.video).exists():
                    recommended_videos.add(rating.video)
    return recommended_videos
