import numpy as np
import re
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.manifold import TSNE
from recomendador_videos.youtube_integration.models import Video

def extract_hashtags(text):
    """Extrai hashtags do título e descrição"""
    return set(re.findall(r'#\w+', text)) if text else set()

def get_video_features(video):
    """Extrai os metadados do vídeo como features"""
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
    """Calcula a similaridade entre dois vídeos considerando múltiplos fatores"""
    features1 = get_video_features(video1)
    features2 = get_video_features(video2)

    # Título e Descrição 
    title_similarity = calculate_text_similarity(features1["title"], features2["title"])
    description_similarity = calculate_text_similarity(features1["description"], features2["description"])

    # Canal e Playlist
    channel_similarity = 1 if features1["channel"] == features2["channel"] else 0
    playlist_similarity = 1 if features1["playlist"] and features1["playlist"] == features2["playlist"] else 0

    hashtag_intersection = features1["hashtags"].intersection(features2["hashtags"])
    hashtag_union = features1["hashtags"].union(features2["hashtags"])
    hashtag_similarity = len(hashtag_intersection) / len(hashtag_union) if hashtag_union else 0

    duration_diff = abs(features1["duration"] - features2["duration"])
    duration_similarity = 1 - (duration_diff / max(features1["duration"], features2["duration"], 1))  

    year_similarity = 1 if features1["year"] and features2["year"] and features1["year"] == features2["year"] else 0

    # Pesos ajustados para melhor balanceamento
    weights = {
        "title": 5, "description": 3, "channel": 12, "playlist": 2,
        "hashtags": 1, "duration": 0.2, "year": 0.2
    }

    similarities = {
        "title": title_similarity, "description": description_similarity, "channel": channel_similarity,
        "playlist": playlist_similarity, "hashtags": hashtag_similarity,
        "duration": duration_similarity, "year": year_similarity
    }

    # Imprimir cada similaridade para análise
    # print(f"\nComparação entre: {video1.title} e {video2.title}")
    # for feature, value in similarities.items():
    #     print(f"{feature} similarity: {value:.4f}")

    final_score = sum(weights[f] * similarities[f] for f in similarities) / sum(weights.values())
    
    return final_score


def calculate_text_similarity(text1, text2):
    """Calcula a similaridade entre dois textos usando TF-IDF"""
    if not text1 or not text2:
        return 0  # Se um deles estiver vazio, a similaridade é zero

    corpus = [text1, text2]
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(corpus)

    similarity_matrix = cosine_similarity(tfidf_matrix)
    return similarity_matrix[0, 1]  # Retorna a similaridade entre os dois textos


def get_similar_videos(video_base, threshold=0.1):
    """Retorna vídeos semelhantes ao vídeo base"""
    videos = Video.objects.exclude(id=video_base.id)
    similarities = [(video, calculate_similarity(video_base, video)) for video in videos]

    # Filtrar apenas os vídeos que atendem ao limiar de similaridade
    filtered_videos = [{"video": video, "similarity": score} for video, score in similarities if score >= threshold]

    # Ordenar por similaridade decrescente
    return sorted(filtered_videos, key=lambda x: x["similarity"], reverse=True)


def get_tsne_cluster_data(selected_video_id=None):
    """Gera dados para visualização dos clusters de vídeos usando t-SNE."""
    videos = Video.objects.all()
    if not videos:
        return json.dumps([])

    video_titles = [video.title for video in videos]
    video_ids = [video.id for video in videos]
    
    # Gerar embeddings TF-IDF
    texts = [video.title + " " + (video.description or "") for video in videos]

    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(texts).toarray()

    # Redução de Dimensionalidade com t-SNE
    tsne = TSNE(n_components=2, perplexity=30, random_state=42)
    reduced_features = tsne.fit_transform(tfidf_matrix)

    # Ajustando a cor e tamanho dos pontos
    data = [{
        "id": video_ids[i],
        "title": video_titles[i],
        "x": float(reduced_features[i, 0]),
        "y": float(reduced_features[i, 1]),
        "color": "red" if selected_video_id and video_ids[i] == selected_video_id else "blue",
        "size": 12 if selected_video_id and video_ids[i] == selected_video_id else 6  # Aumenta o ponto selecionado
    } for i in range(len(videos))]
    
    return json.dumps(data)
