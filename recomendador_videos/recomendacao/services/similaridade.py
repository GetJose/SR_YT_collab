import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from ..models import VideoInteraction
from ..utils.texto import obter_dados_video
from recomendador_videos.youtube_integration.models import Video
from sklearn.feature_extraction.text import TfidfVectorizer


def calcular_correlacao_pearson(user):
   all_ratings = VideoInteraction.objects.all()
   data = {
       'user_id': [rating.user_id for rating in all_ratings],
       'video_id': [rating.video_id for rating in all_ratings],
       'rating': [rating.rating for rating in all_ratings],
   }
   df_ratings = pd.DataFrame(data)
   ratings_matrix = df_ratings.pivot_table(index='user_id', columns='video_id', values='rating')

   if user.id not in ratings_matrix.index:
       return pd.Series()

   user_ratings = ratings_matrix.loc[user.id]
   correlations = ratings_matrix.corrwith(user_ratings, axis=1, method='pearson').dropna().sort_values(ascending=False)

   return correlations

def calcular_similaridade_cosseno(user):
   all_ratings = VideoInteraction.objects.all()
   data = {
       'user_id': [rating.user_id for rating in all_ratings],
       'video_id': [rating.video_id for rating in all_ratings],
       'rating': [rating.rating for rating in all_ratings],
   }
   df_ratings = pd.DataFrame(data)
   ratings_matrix = df_ratings.pivot_table(index='user_id', columns='video_id', values='rating').fillna(0)

   if user.id not in ratings_matrix.index:
       return pd.Series()

   user_ratings = ratings_matrix.loc[user.id].values.reshape(1, -1)
   similarities = cosine_similarity(user_ratings, ratings_matrix.values).flatten()
   return pd.Series(similarities, index=ratings_matrix.index).drop(user.id).sort_values(ascending=False)

def calcular_similaridade_usuarios(user, metodo="pearson"):
    """
    Calcula a similaridade entre usuários com base nas avaliações de vídeos.
    """
    all_ratings = VideoInteraction.objects.all().values("user_id", "video_id", "rating")
    df_ratings = pd.DataFrame.from_records(all_ratings)
    ratings_matrix = df_ratings.pivot_table(index='user_id', columns='video_id', values='rating')
    
    if user.id not in ratings_matrix.index:
        return {}

    user_ratings = ratings_matrix.loc[user.id]
    
    if metodo == "pearson":
        correlations = ratings_matrix.corrwith(user_ratings, axis=1, method='pearson')
    else:  # Similaridade do cosseno
        similarities = cosine_similarity(user_ratings.values.reshape(1, -1), ratings_matrix.fillna(0).values)
        correlations = pd.Series(similarities.flatten(), index=ratings_matrix.index)
    
    return correlations.dropna().sort_values(ascending=False).to_dict()

def calcular_similaridade_itens(video_alvo, lista_videos, top_n=6):
    """
    Encontra vídeos semelhantes ao video_alvo dentro da lista_videos.
    """
    if not lista_videos:
        return []
    lista_videos = [video for video in lista_videos if video.id != video_alvo.id]

    dados_videos = [obter_dados_video(video) for video in lista_videos]
    dados_video_alvo = obter_dados_video(video_alvo)
    
    if not dados_video_alvo or all(not texto for texto in dados_videos):
        return [] 

    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform([dados_video_alvo] + dados_videos)
    
    similaridade = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
    videos_ordenados = sorted(zip(lista_videos, similaridade), key=lambda x: x[1], reverse=True)
    
    return [video for video, _ in videos_ordenados[:top_n]]