import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

nltk.download('stopwords')
nltk.download('punkt')

def remover_stopwords(texto: str) -> str:
    """
    Remove as stopwords de um texto para limpar o conteúdo e facilitar a análise.
    """
    stop_words = set(stopwords.words('portuguese'))
    return ' '.join([palavra for palavra in texto.split() if palavra.lower() not in stop_words])

def obter_dados_video(video):
    """
    Obtém uma string consolidada com as informações relevantes do vídeo (título, descrição e categoria).
    As stopwords são removidas para otimizar a análise de similaridade.
    """
    titulo = remover_stopwords(video.title or "")
    descricao = remover_stopwords(video.description or "")
    return f"{titulo} {descricao} {video.category}"

def obter_palavra_importante(titulo: str) -> str:
    """
    Extrai a palavra mais importante de um título com base no peso TF-IDF.
    """
    if not titulo:
        return ""
    
    palavras = word_tokenize(titulo)
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([' '.join(palavras)])
    palavras_importantes = vectorizer.get_feature_names_out()
    pesos = tfidf_matrix.toarray()[0]

    max_indice = pesos.argmax()
    return palavras_importantes[max_indice]


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