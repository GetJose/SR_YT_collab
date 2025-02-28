import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer

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
