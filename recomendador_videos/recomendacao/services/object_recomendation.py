import numpy as np
import re
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.manifold import TSNE
from recomendador_videos.youtube_integration.models import Video

def extract_hashtags(text):
    """
    Extrai hashtags de um texto.
    Args:
        text (str): Texto de entrada (título ou descrição).
    Returns:
        set: Conjunto de hashtags encontradas.
    """
    return set(re.findall(r'#\w+', text)) if text else set()

def get_video_features(video):
    """
    Extrai os metadados de um vídeo para usar como features.
    Args:
        video (Video): Objeto do vídeo.
    Returns:
        dict: Dicionário com as features do vídeo (título, descrição, canal, etc.).
    """
    hashtags = extract_hashtags(video.title + " " + (video.description or ""))
    return {
        "title": video.title.lower() if video.title else "",
        "description": video.description.lower() if video.description else "",
        "channel": video.channel_title.lower() if video.channel_title else "",
        "playlist": video.playlist_id.lower() if video.playlist_id else "",
        "duration": video.duration,
        "year": video.published_at.year if video.published_at else None,
        "hashtags": hashtags
    }

def calculate_similarity(video1, video2):
    """
    Calcula a similaridade entre dois vídeos com base em múltiplas features.
    A similaridade final é ponderada de acordo com a importância de cada feature.
    Args:
        video1 (Video): Primeiro vídeo.
        video2 (Video): Segundo vídeo.
    Returns:
        float: Pontuação final de similaridade entre 0 e 1.
    """
    features1 = get_video_features(video1)
    features2 = get_video_features(video2)

    # Similaridade de título e descrição
    title_similarity = calculate_text_similarity(features1["title"], features2["title"])
    description_similarity = calculate_text_similarity(features1["description"], features2["description"])

    # Similaridade de canal e playlist
    channel_similarity = 1 if features1["channel"] == features2["channel"] else 0
    playlist_similarity = 1 if features1["playlist"] and features1["playlist"] == features2["playlist"] else 0

    # Similaridade de hashtags
    hashtag_intersection = features1["hashtags"].intersection(features2["hashtags"])
    hashtag_union = features1["hashtags"].union(features2["hashtags"])
    hashtag_similarity = len(hashtag_intersection) / len(hashtag_union) if hashtag_union else 0

    # Similaridade de duração
    duration_diff = abs(features1["duration"] - features2["duration"])
    duration_similarity = 1 - (duration_diff / max(features1["duration"], features2["duration"], 1))  

    # Similaridade de ano de publicação
    year_similarity = 1 if features1["year"] and features2["year"] and features1["year"] == features2["year"] else 0

    # Pesos para balancear cada feature
    weights = {
        "title": 5, "description": 3, "channel": 12, "playlist": 2,
        "hashtags": 1, "duration": 0.2, "year": 0.2
    }

    similarities = {
        "title": title_similarity, "description": description_similarity, "channel": channel_similarity,
        "playlist": playlist_similarity, "hashtags": hashtag_similarity,
        "duration": duration_similarity, "year": year_similarity
    }

    # Calcula a média ponderada das similaridades
    final_score = sum(weights[f] * similarities[f] for f in similarities) / sum(weights.values())
    return final_score

def calculate_text_similarity(text1, text2):
    """
    Calcula a similaridade entre dois textos usando TF-IDF e cosseno.
    Args:
        text1 (str): Primeiro texto.
        text2 (str): Segundo texto.
    Returns:
        float: Pontuação de similaridade entre 0 e 1.
    """
    if not text1 or not text2:
        return 0

    corpus = [text1, text2]
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(corpus)

    similarity_matrix = cosine_similarity(tfidf_matrix)
    return similarity_matrix[0, 1]

def get_similar_videos(video_base, threshold=0.1):
    """
    Retorna vídeos semelhantes ao vídeo base com base na similaridade calculada.
    Args:
        video_base (Video): Vídeo de referência.
        threshold (float): Limiar mínimo de similaridade para considerar um vídeo relevante.
    Returns:
        list[dict]: Lista de vídeos semelhantes com a pontuação de similaridade.
    """
    videos = Video.objects.exclude(id=video_base.id)
    similarities = [(video, calculate_similarity(video_base, video)) for video in videos]

    # Filtrar vídeos com similaridade acima do limiar
    filtered_videos = [{"video": video, "similarity": score} for video, score in similarities if score >= threshold]

    # Ordenar por similaridade decrescente
    return sorted(filtered_videos, key=lambda x: x["similarity"], reverse=True)

def get_tsne_cluster_data(selected_video_id=None):
    """
    Gera os dados para visualização dos clusters de vídeos usando t-SNE.
    Cada vídeo é reduzido a dois componentes principais para visualização.
    Args:
        selected_video_id (int, opcional): ID do vídeo selecionado (para destacar na visualização).
    Returns:
        str: Dados de cluster em formato JSON para visualização.
    """
    videos = Video.objects.all()
    if not videos:
        return json.dumps([])

    video_titles = [video.title for video in videos]
    video_ids = [video.id for video in videos]
    
    # Gerar embeddings TF-IDF
    texts = [video.title + " " + (video.description or "") for video in videos]

    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(texts).toarray()

    # Redução de dimensionalidade com t-SNE
    tsne = TSNE(n_components=2, perplexity=30, random_state=42)
    reduced_features = tsne.fit_transform(tfidf_matrix)

    # Organiza os dados para visualização
    data = [{
        "id": video_ids[i],
        "title": video_titles[i],
        "x": float(reduced_features[i, 0]),
        "y": float(reduced_features[i, 1]),
        "color": "red" if selected_video_id and video_ids[i] == selected_video_id else "blue",
        "size": 12 if selected_video_id and video_ids[i] == selected_video_id else 6
    } for i in range(len(videos))]
    
    return json.dumps(data)
