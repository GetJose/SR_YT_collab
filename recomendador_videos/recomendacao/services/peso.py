from collections import Counter
from recomendador_videos.recomendacao.models import VideoInteraction

def calcular_pesos_recomendacao(user):
    """
    Calcula os pesos das recomendações user-based e item-based com base no histórico de interações do usuário.
    O peso de cada método é definido pela frequência com que ele aparece no histórico:
    - Se o usuário interagiu mais com vídeos recomendados por user-based, o peso será maior para essa abordagem.
    - Se interagiu mais com item-based, o peso será ajustado para priorizar esse método.
    Args:
        user (User): Usuário para quem os pesos serão calculados.
    Returns:
        tuple(float, float): Um par de valores representando os pesos de user-based e item-based, respectivamente.
    """
    interacoes = VideoInteraction.objects.filter(user=user).values_list('method', flat=True)
    
    # Filtra apenas os métodos relevantes
    contagem_metodos = Counter(m for m in interacoes if m in ["user_based", "item_based"])
    total = sum(contagem_metodos.values())
    
    if total == 0:
        return 0.5, 0.5  # Caso não haja dados, assume pesos iguais
    
    peso_user = contagem_metodos.get("user_based", 0) / total
    peso_item = contagem_metodos.get("item_based", 0) / total
    
    return peso_user, peso_item
