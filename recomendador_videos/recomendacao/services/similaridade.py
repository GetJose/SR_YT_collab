import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from ..models import VideoInteraction
from ..utils.texto import obter_dados_video
from recomendador_videos.youtube_integration.models import Video
from sklearn.feature_extraction.text import TfidfVectorizer

def calcular_similaridade_usuarios(user, metodo="pearson"):
    """
    Calcula a similaridade entre usuários com base nas avaliações de vídeos.
    Args:
        user (User): Usuário para quem a similaridade será calculada.
        metodo (str): Método de similaridade a ser utilizado ('pearson' ou 'cosseno').
    Returns:
        dict: Dicionário com os IDs dos usuários e seus respectivos scores de similaridade.
    """
    all_ratings = VideoInteraction.objects.exclude(rating__isnull=True).values("user_id", "video_id", "rating")
    df_ratings = pd.DataFrame.from_records(all_ratings)

    if df_ratings.empty or user.id not in df_ratings["user_id"].unique():
        return {}
    
    ratings_matrix = df_ratings.pivot_table(index='user_id', columns='video_id', values='rating')

    if user.id not in ratings_matrix.index:
        return {}

    user_ratings = ratings_matrix.loc[user.id]

    if metodo == "pearson":
        correlations = ratings_matrix.corrwith(user_ratings, axis=1, method='pearson')
    else:  
        similarities = cosine_similarity(user_ratings.fillna(0).values.reshape(1, -1), ratings_matrix.fillna(0).values)
        correlations = pd.Series(similarities.flatten(), index=ratings_matrix.index)

    correlations = correlations.drop(index=user.id, errors="ignore")

    return correlations.dropna().sort_values(ascending=False).to_dict()

def calcular_similaridade_itens(video_alvo, lista_videos, top_n=6):
    """
    Encontra vídeos semelhantes ao vídeo alvo com base no conteúdo textual.
    Utiliza TF-IDF e similaridade do cosseno para medir a proximidade dos vídeos.
    Args:
        video_alvo (Video): O vídeo base para a comparação.
        lista_videos (list[Video]): Lista de vídeos a serem comparados.
        top_n (int): Número de vídeos mais semelhantes a serem retornados.
    Returns:
        list[Video]: Lista dos vídeos mais semelhantes ao vídeo alvo.
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