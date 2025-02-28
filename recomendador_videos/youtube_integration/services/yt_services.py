from googleapiclient.discovery import build
import os


def get_youtube_api_keys():
    """
    Coleta automaticamente todas as chaves de API do YouTube a partir das variáveis de ambiente.
    Returns:
        list: Lista de chaves de API encontradas.
    """
    keys = []
    for key, value in os.environ.items():
        if key.startswith('YOUTUBE_API_KEY') and value:
            keys.append(value)
    return keys


def get_youtube_client():
    """
    Inicializa e retorna o cliente da API do YouTube, trocando de chave se necessário.
    Returns:
        googleapiclient.discovery.Resource: Cliente da API YouTube.
    """
    api_keys = get_youtube_api_keys()
    
    if not api_keys:
        raise ValueError("Nenhuma chave de API do YouTube encontrada nas variáveis de ambiente.")
    
    for key in api_keys:
        try:
            youtube = build('youtube', 'v3', developerKey=key)
            # Testa uma requisição simples para validar a chave
            youtube.videos().list(part='id', chart='mostPopular', maxResults=1).execute()
            print(f"Conectado com sucesso usando a chave: {key[:10]}...")
            return youtube
        except Exception as e:
            print(f"Erro com a chave {key[:10]}...: {e}")
            continue
    
    raise ValueError("Todas as chaves de API falharam. Verifique as configurações.")