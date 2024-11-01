import random
import pandas as pd
from django.contrib.auth.models import User
from recomendador_videos.home.models import VideoRating
from recomendador_videos.recomendacao.models import UserSimilarity
from recomendador_videos.youtube_integration.models import Video
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')

def remover_stopwords(text):
   stop_words = set(stopwords.words('portuguese'))
   return ' '.join([word for word in text.split() if word.lower() not in stop_words])

def obter_dados_video(video):
   titulo = remover_stopwords(video.title or "")
   descricao = remover_stopwords(video.description or "")
   return f"{titulo} {descricao} {video.category}"

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
       return pd.Series()

   user_ratings = ratings_matrix.loc[user.id]
   correlations = ratings_matrix.corrwith(user_ratings, axis=1, method='pearson').dropna().sort_values(ascending=False)

   for similar_user_id, similarity_score in correlations.items():
       if similar_user_id != user.id:
           UserSimilarity.objects.update_or_create(
               user=user,
               similar_user_id=similar_user_id,
               defaults={'score': similarity_score}
           )
   return correlations

def calcular_similaridade_cosseno(user):
   all_ratings = VideoRating.objects.all()
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

#ABORDAGEM DE RECOMENDAÇÃO HIBRIDA EM CASCATA ONDE UMA RECOMENDAÇÃO É USADA COMO BASE PRA OUTRA
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

def calcular_similaridade_itens(user, recommended_videos):
    videos_assistidos = VideoRating.objects.filter(user=user).values_list('video', flat=True)
    videos_restantes = Video.objects.exclude(id__in=videos_assistidos)

    video_data_user = [obter_dados_video(Video.objects.get(id=vid)) for vid in videos_assistidos]
    video_data_recommended = [obter_dados_video(video) for video in recommended_videos]

    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix_user = tfidf_vectorizer.fit_transform(video_data_user)
    tfidf_matrix_recommended = tfidf_vectorizer.transform(video_data_recommended)

    similaridade = cosine_similarity(tfidf_matrix_user, tfidf_matrix_recommended)

    return sorted(zip(recommended_videos, similaridade.mean(axis=0)), key=lambda x: x[1], reverse=True)

def recomendar_videos_hibrido(user):
    colaborativa_recommended = recomendar_videos(user)

    similaridade_filtrada = calcular_similaridade_itens(user, colaborativa_recommended)

    return [video for video, _ in similaridade_filtrada[:12]]

#ABORDADEM DE FUSÃO DE DUAS LISTAS 
def recomendar_videos_user_based(user):
    user_correlations = calcular_correlacao_pearson(user)
    similar_users = sorted(user_correlations.items(), key=lambda x: x[1], reverse=True)

    recommended_videos = set()
    for similar_user, score in similar_users:
        if score > 0:
            similar_user_ratings = VideoRating.objects.filter(user=similar_user, rating=1)
            for rating in similar_user_ratings:
                if not VideoRating.objects.filter(user=user, video=rating.video).exists():
                    recommended_videos.add(rating.video)
    if len(recommended_videos) > 12:
        recommended_videos = random.sample(list(recommended_videos), 12)
    return recommended_videos

def encontrar_videos_similares(video_alvo, top_n=10):
   todos_videos = Video.objects.exclude(id=video_alvo.id)
   dados_videos = [obter_dados_video(video) for video in todos_videos]
   dados_videos.insert(0, obter_dados_video(video_alvo))

   tfidf_vectorizer = TfidfVectorizer()
   tfidf_matrix = tfidf_vectorizer.fit_transform(dados_videos)
   similaridade = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()

   return [video for video, _ in sorted(zip(todos_videos, similaridade), key=lambda x: x[1], reverse=True)[:top_n]]

def recomendar_videos_itens_based(user):
   videos_recentes = [rating.video for rating in VideoRating.objects.filter(user=user, rating=1).order_by('-updated_at')[:5]]
   recomendados = set()

   for video in videos_recentes:
       recomendados.update([
           video_similar for video_similar in encontrar_videos_similares(video, top_n=10)
           if not VideoRating.objects.filter(user=user, video=video_similar).exists()
       ])

   return list(recomendados)

def combinar_recomendacoes(user_recommendations, item_recommendations):
   user_recommendations = list(user_recommendations)
   item_recommendations = list(item_recommendations)

   ranking_videos = {}

   for idx, video in enumerate(user_recommendations):
       ranking_videos[video] = (len(user_recommendations) - idx) * 0.3

   for idx, video in enumerate(item_recommendations):
       if video in ranking_videos:
           ranking_videos[video] += (len(item_recommendations) - idx) * 0.7
       else:
           ranking_videos[video] = (len(item_recommendations) - idx) * 0.7

   recomendacoes_hibridas = sorted(ranking_videos.items(), key=lambda x: x[1], reverse=True)
   return [video for video, score in recomendacoes_hibridas]

def filtrar_e_ranquear_videos(videos, duracao_media=None):
   categorias_permitidas = ['Education', 'Science & Technology', 'Unknown']
   videos_filtrados = [video for video in videos if video.category in categorias_permitidas]

   def calcular_ranking(video):
       likes = int(video.like_count or 0)
       dislikes = int(video.dislike_count or 0)
       total_views = int(video.view_count or 0)
       duracao = int(video.duration or 0)

       percentual_likes = likes / (likes + dislikes) if likes + dislikes > 0 else 0
       peso_duracao = 1 - abs(duracao - duracao_media) / duracao_media if duracao_media else 0

       return percentual_likes + (total_views * 0.5) + (peso_duracao * 0.5)

   return sorted(videos_filtrados, key=calcular_ranking, reverse=True)

# Função híbrida de recomendação com junção
def recomendar_videos_fusao(user):
   #user_recommendations = recomendar_videos(user)
   user_recommendations = []
   item_recommendations = recomendar_videos_itens_based(user)


   recomendacoes_comb = combinar_recomendacoes(user_recommendations, item_recommendations)
   duracao_media = sum(v.duration or 0 for v in user_recommendations) / len(user_recommendations) if user_recommendations else 0
  
  # return filtrar_e_ranquear_videos(recomendacoes_comb, duracao_media=duracao_media)[:12]
   return recomendacoes_comb[:12]