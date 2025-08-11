from django.contrib import messages
from django.shortcuts import redirect
from app.models import Organizador, Evento, Participante


class OrganizadorRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        organizador = Organizador.objects.filter(user=self.request.user).first()
        if not organizador:
            messages.error(self.request, "Apenas usuários com perfil de organizador podem fazer isso.")
            return redirect('home')
        request.organizador_logado = organizador
        return super().dispatch(request, *args, **kwargs)


class EventoOwnerRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        evento = Evento.objects.filter(pk=kwargs.get('pk'), organizador=request.organizador_logado).first()
        if not evento:
            messages.error(request, "Você não tem permissão para gerenciar este evento.")
            return redirect('evento-list')
        return super().dispatch(request, *args, **kwargs)


class ParticipanteRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not Participante.objects.filter(user=request.user).exists():
            messages.error(request, "Apenas usuários com perfil de participante podem fazer isso.")
            return redirect('evento-list')
        return super().dispatch(request, *args, **kwargs)