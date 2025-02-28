from django.http import JsonResponse
from django.contrib.auth.models import User
from django.db.models import Q

def buscar_usuarios(request):
    """
    Busca usuários pelo nome de usuário ou e-mail, excluindo o próprio usuário logado.
    Algumas funçoes precisam dos nomes de forma dinaminca na página por isso a view que retorna os usuarios, funcionando como uma api.
    Args:
        request (HttpRequest): A requisição HTTP contendo o parâmetro de pesquisa 'q' na query string.
    Returns:
        JsonResponse: Uma lista JSON contendo os IDs e usernames dos usuários encontrados.
    """
    termo = request.GET.get("q", "")
    if termo:
        usuarios = User.objects.filter(
            Q(username__icontains=termo) | Q(email__icontains=termo)
        ).exclude(id=request.user.id)[:10]
    else:
        usuarios = User.objects.all().exclude(id=request.user.id)[:10]
    
    usuarios_data = [{"id": u.id, "username": u.username} for u in usuarios]
    return JsonResponse(usuarios_data, safe=False)
