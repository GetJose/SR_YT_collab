from django.db.models import Prefetch
from ..models import VideoInteraction

def carregar_videos_assistidos(usuario):
    """
    Retorna os vídeos que o usuário assistiu, otimizando a consulta ao banco.
    """
    return VideoInteraction.objects.filter(user=usuario).select_related("video")


def carregar_videos_assistidos(usuario):
    """
    Retorna os ultimos 5 vídeos que o usuário curtiu
    """
    return VideoInteraction.objects.filter(user=usuario, rating=1).order_by('-updated_at')[:5]