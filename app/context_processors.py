from app.models import Participante, Organizador

def perfil_usuario(request):
    user = request.user
    is_organizador = False
    is_participante = False

    if user.is_authenticated:
        is_organizador = Organizador.objects.filter(user=user).exists()
        is_participante = Participante.objects.filter(user=user).exists()

    return {
        'is_organizador': is_organizador,
        'is_participante': is_participante
    }