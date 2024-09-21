import pandas as pd
from recomendador_videos.home.models import VideoRating
from django.contrib.auth.models import User

def calcular_correlacao_pearson(user):
    """Calcula a correlação de Pearson entre o usuário e outros usuários usando Pandas"""
    
    # Recupera todas as avaliações de vídeos no banco de dados
    all_ratings = VideoRating.objects.all()
    
    # Constrói um DataFrame com as avaliações
    data = {
        'user_id': [rating.user_id for rating in all_ratings],
        'video_id': [rating.video_id for rating in all_ratings],
        'rating': [rating.rating for rating in all_ratings],
    }
    df_ratings = pd.DataFrame(data)
    
    # Converte a tabela para o formato de matriz de usuários x vídeos, preenchendo com NaN onde não há avaliação
    ratings_matrix = df_ratings.pivot_table(index='user_id', columns='video_id', values='rating')

    # Verifica se o usuário tem avaliações
    if user.id not in ratings_matrix.index:
        # Se o usuário não tem avaliações, retorna uma recomendação padrão ou uma lista vazia
        return pd.Series(dtype='float64')  # Ou outra estratégia de fallback
    
    # Recupera as avaliações do usuário alvo
    user_ratings = ratings_matrix.loc[user.id]

    # Calcula a correlação de Pearson entre o usuário e todos os outros usuários
    correlations = ratings_matrix.corrwith(user_ratings, axis=1, method='pearson')

    # Ordena pela maior correlação e remove NaN
    correlations = correlations.dropna().sort_values(ascending=False)

    return correlations


def recomendar_videos(user):
    """Recomenda vídeos com base nas avaliações de usuários semelhantes"""
    # Calcula a correlação de Pearson
    user_correlations = calcular_correlacao_pearson(user)

    # Ordena os usuários mais semelhantes
    similar_users = sorted(user_correlations.items(), key=lambda x: x[1], reverse=True)

    recommended_videos = set()

    # Para cada usuário semelhante, recomendando vídeos que o usuário logado ainda não assistiu
    for similar_user, score in similar_users:
        if score > 0:  # Apenas usuários com correlação positiva
            similar_user_ratings = VideoRating.objects.filter(user=similar_user, rating=1)
            for rating in similar_user_ratings:
                if not VideoRating.objects.filter(user=user, video=rating.video).exists():
                    recommended_videos.add(rating.video)

    return recommended_videos
