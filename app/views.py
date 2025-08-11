import datetime
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.html import strip_tags
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from app.forms import EventoForm, ParticipanteSignUpForm, OrganizadorSignUpForm, ParticipanteForm, OrganizadorForm, \
    UserForm
from app.mixins import OrganizadorRequiredMixin, EventoOwnerRequiredMixin, ParticipanteRequiredMixin
from app.models import Evento, Organizador, Participante, Inscricao


class EventoListView(ListView):
    model = Evento
    template_name = 'eventos/evento_list.html'
    context_object_name = 'eventos'

    def get_queryset(self):
        queryset = super().get_queryset()

        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(titulo__icontains=query) |
                Q(descricao__icontains=query) |
                Q(local__icontains=query)
            )

        data_inicio = self.request.GET.get('data_inicio')
        data_fim = self.request.GET.get('data_fim')

        if data_inicio:
            queryset = queryset.filter(data__gte=data_inicio)

        if data_fim:
            queryset = queryset.filter(data__lte=data_fim)

        queryset = queryset.order_by('id')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        is_authenticated = self.request.user.is_authenticated
        organizador_usuario = None
        if is_authenticated:
            organizador_usuario = Organizador.objects.filter(user=user).first()

        context['is_organizador'] = bool(organizador_usuario)
        context['is_participante'] = Participante.objects.filter(user=self.request.user).exists() if is_authenticated else False
        context['query'] = self.request.GET.get('q', '')

        data_inicio_param = self.request.GET.get('data_inicio')
        data_fim_param = self.request.GET.get('data_fim')

        if data_inicio_param and data_fim_param:
            if data_inicio_param > data_fim_param:
                messages.error(self.request, 'A data de início não pode ser maior que a data de fim.')

        eventos_filtrados = self.get_queryset()

        eventos_com_propriedades = []
        for evento in eventos_filtrados:
            evento.vagas_restantes = evento.capacidade_max - evento.inscricao_set.count()
            evento.is_owner = (organizador_usuario == evento.organizador)

            if is_authenticated and context['is_participante']:
                try:
                    inscricao = Inscricao.objects.get(evento=evento, participante__user=user)
                    evento.is_inscrito = True
                    evento.inscricao_id = inscricao.id
                except Inscricao.DoesNotExist:
                    evento.is_inscrito = False
                    evento.inscricao_id = None

            eventos_com_propriedades.append(evento)

        context['eventos'] = eventos_com_propriedades
        return context


class EventoCreateView(LoginRequiredMixin, OrganizadorRequiredMixin, CreateView):
    model = Evento
    form_class = EventoForm
    template_name = 'eventos/evento_form.html'
    success_url = reverse_lazy('evento-list')

    def form_valid(self, form):
        form.instance.organizador = self.request.organizador_logado
        return super().form_valid(form)


class EventoUpdateView(LoginRequiredMixin, OrganizadorRequiredMixin, EventoOwnerRequiredMixin, UpdateView):
    model = Evento
    form_class = EventoForm
    template_name = 'eventos/evento_form.html'
    success_url = reverse_lazy('evento-list')

    def get_initial(self):
        initial = super().get_initial()
        if self.object:
            initial['data'] = self.object.data.strftime('%Y-%m-%dT%H:%M')
        return initial


class EventoDeleteView(LoginRequiredMixin, OrganizadorRequiredMixin, EventoOwnerRequiredMixin, DeleteView):
    model = Evento
    success_url = reverse_lazy('evento-list')


class ParticipanteSignUpView(CreateView):
    model = User
    form_class = ParticipanteSignUpForm
    template_name = 'registro/signup_participante.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        response = super().form_valid(form)
        Participante.objects.create(
            user=self.object,
            nome=form.cleaned_data.get('nome'),
            telefone=form.cleaned_data.get('telefone'),
            genero=form.cleaned_data.get('genero'),
            cidade=form.cleaned_data.get('cidade'),
            cpf=form.cleaned_data.get('cpf'),
        )
        login(self.request, self.object)
        return (response)


class ParticipanteListView(LoginRequiredMixin, ParticipanteRequiredMixin, ListView):
    model = Participante
    template_name = 'eventos/perfil_participante.html'
    context_object_name ='perfil_p'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        participante = get_object_or_404(Participante, user=self.request.user)
        minhas_inscricoes = Inscricao.objects.filter(participante=participante).order_by('-data_envio')
        total_inscricoes = minhas_inscricoes.count()

        context['participante'] = participante
        context['inscricoes'] = minhas_inscricoes
        context['total_inscricoes'] = total_inscricoes

        return context


class ParticipanteUpdateView(LoginRequiredMixin, ParticipanteRequiredMixin, UpdateView):
    model = Participante
    form_class = ParticipanteForm
    template_name = 'eventos/perfil_participante_update.html'
    success_url = reverse_lazy('perfil-participante')

    def get_object(self, queryset=None):
        return get_object_or_404(Participante, user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        participante = get_object_or_404(Participante, user=self.request.user)
        minhas_inscricoes = Inscricao.objects.filter(participante=participante).order_by('-data_envio')
        total_inscricoes = minhas_inscricoes.count()

        context['participante'] = participante
        context['inscricoes'] = minhas_inscricoes
        context['total_inscricoes'] = total_inscricoes

        return context


class ParticipanteDeleteView(LoginRequiredMixin, ParticipanteRequiredMixin, DeleteView):
    model = Participante
    success_url = reverse_lazy('login')

    def get_object(self, queryset=None):
        return get_object_or_404(Participante, user=self.request.user)

    def post(self, request, *args, **kwargs):
        participante = self.get_object()
        user_to_delete = participante.user
        response = super().post(request, *args, **kwargs)
        user_to_delete.delete()

        return response


class OrganizadorSignUpView(CreateView):
    model = User
    form_class = OrganizadorSignUpForm
    template_name ='registro/signup_organizador.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        response = super().form_valid(form)
        Organizador.objects.create(
            user=self.object,
            nome_organizador=form.cleaned_data.get('nome_organizador'),
            telefone=form.cleaned_data.get('telefone'),
            genero=form.cleaned_data.get('genero'),
            cidade=form.cleaned_data.get('cidade'),
            cnpj=form.cleaned_data.get('cnpj'),
        )
        login(self.request, self.object)
        return response


class OrganizadorListView(LoginRequiredMixin, OrganizadorRequiredMixin, ListView):
    model = Organizador
    template_name = 'eventos/perfil_organizador.html'
    context_object_name = 'perfil_o'

    def get_object(self):
        return get_object_or_404(Organizador, user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        organizador = get_object_or_404(Organizador, user=self.request.user)
        meus_eventos = Evento.objects.filter(organizador=organizador).order_by('-data')
        total_eventos = meus_eventos.count()

        context['organizador'] = organizador
        context['eventos'] = meus_eventos
        context['total_eventos'] = total_eventos

        return context


class OrganizadorUpdateView(LoginRequiredMixin, OrganizadorRequiredMixin, UpdateView):
    model = Organizador
    form_class = OrganizadorForm
    template_name = 'eventos/perfil_organizador_update.html'
    success_url = reverse_lazy('perfil-organizador')

    def get_object(self):
        return get_object_or_404(Organizador, user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        organizador = get_object_or_404(Organizador, user=self.request.user)
        meus_eventos = Evento.objects.filter(organizador=organizador).order_by('-data')
        total_eventos = meus_eventos.count()

        context['organizador'] = organizador
        context['eventos'] = meus_eventos
        context['total_eventos'] = total_eventos

        return context

class OrganizadorDeleteView(LoginRequiredMixin, OrganizadorRequiredMixin, DeleteView):
    model = Organizador
    success_url = reverse_lazy('login')

    def get_object(self, queryset=None):
        return get_object_or_404(Organizador, user=self.request.user)

    def post(self, request, *args, **kwargs):
        organizador = self.get_object()
        user_to_delete = organizador.user
        response = super().post(request, *args, **kwargs)
        user_to_delete.delete()

        return response

class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'eventos/perfil_user_update.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context['is_organizador'] = hasattr(user, 'organizador')
        context['is_participante'] = hasattr(user, 'participante')

        if context['is_participante']:
            participante = get_object_or_404(Participante, user=user)
            minhas_inscricoes = Inscricao.objects.filter(participante=participante).order_by('-data_envio')
            total_inscricoes = minhas_inscricoes.count()
            context['participante'] = participante
            context['inscricoes'] = minhas_inscricoes
            context['total_inscricoes'] = total_inscricoes

        elif context['is_organizador']:
            organizador = get_object_or_404(Organizador, user=user)
            eventos_organizador = Evento.objects.filter(organizador=organizador).order_by('-data')
            total_eventos = eventos_organizador.count()

            context['organizador'] = organizador
            context['eventos'] = eventos_organizador
            context['total_eventos'] = total_eventos

        return context

    def get_success_url(self):
        user = self.request.user

        if hasattr(user, 'organizador'):
            return reverse_lazy('perfil-organizador')

        elif hasattr(user, 'participante'):
            return reverse_lazy('perfil-participante')

        return reverse_lazy('home')


def enviar_email_confirmacao(participante, evento):
    html_content = render_to_string('emails/confirmacao_inscricao.html', {
        'participante': participante,
        'evento': evento
    })

    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(
        subject='Confirmação de Inscrição no Evento',
        body=text_content,
        from_email='senac@eventoscontrole.com.br',
        to=[participante.user.email]
    )

    email.attach_alternative(html_content, "text/html")
    email.send(fail_silently=True)


class InscricaoCreateView(LoginRequiredMixin, ParticipanteRequiredMixin, View):
    def post(self, request, evento_id):
        evento = get_object_or_404(Evento, id=evento_id)

        try:
            participante = Participante.objects.get(user=request.user)
        except Participante.DoesNotExist:
            messages.error(request, 'Você precisa ter um perfil de participante para se inscrever.')
            return redirect('evento-list')

        if Inscricao.objects.filter(evento=evento, participante=participante).exists():
            messages.error(request, 'Você já está inscrito(a) neste evento.')
            return redirect('evento-list')

        inscricoes_atuais = Inscricao.objects.filter(evento=evento).count()

        if inscricoes_atuais >= evento.capacidade_max:
            messages.error(request, 'Desculpe, a capacidade máxima para este evento já foi atingida.')
            return redirect('evento-list')

        Inscricao.objects.create(
            evento=evento,
            participante=participante,
        )

        enviar_email_confirmacao(participante, evento)

        messages.success(request, f'Sua inscrição para o evento "{evento.titulo}" foi confirmada!')

        return redirect('evento-list')


class InscricaoDeleteView(LoginRequiredMixin, ParticipanteRequiredMixin, DeleteView):
    model = Inscricao
    success_url = '/eventos'


class DashboardView(LoginRequiredMixin, OrganizadorRequiredMixin, ListView):
    model = Inscricao
    template_name = 'eventos/dashboard.html'
    context_object_name = 'inscricoes'

    def get_queryset(self):
        return Inscricao.objects.filter(
            evento__organizador=self.request.organizador_logado
        ).select_related('evento', 'participante__user').order_by('-data_envio')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['eventos'] = Evento.objects.filter(
            organizador=self.request.organizador_logado
        ).order_by('-data')

        return context

class HomeView(TemplateView):
    template_name='eventos/home.html'