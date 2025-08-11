# (imports permanecem os mesmos)

from unittest.mock import patch
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.urls import reverse
from app.models import Participante, Organizador, Evento, Inscricao
from django.utils import timezone
from django.contrib.messages import get_messages


class ParticipanteModelTest(TestCase):
    def test_cria_participante_com_sucesso(self):
        user = User.objects.create_user(username='participante1', password='password')
        participante = Participante.objects.create(
            user=user,
            nome='João da Silva',
            telefone='(11) 99999-8888',
            genero='M',
            cidade='São Paulo',
            cpf='12345678901'
        )
        self.assertEqual(participante.nome, 'João da Silva')
        self.assertEqual(str(participante), 'participante1')

    def test_participante_sem_user_falha(self):
        with self.assertRaises(IntegrityError):
            Participante.objects.create(nome='Sem User')


class OrganizadorModelTest(TestCase):
    def test_cria_organizador_com_sucesso(self):
        user = User.objects.create_user(username='organizador1', password='password')
        organizador = Organizador.objects.create(
            user=user,
            nome_organizador='Marquinhos',
            telefone='(11) 77777-6666',
            genero='O',
            cidade='Campinas',
            cnpj='12345678000100'
        )
        self.assertEqual(organizador.nome_organizador, 'Marquinhos')
        self.assertEqual(str(organizador), 'Marquinhos')

    def test_organizador_sem_user_falha(self):
        with self.assertRaises(IntegrityError):
            Organizador.objects.create(nome_organizador='Sem User')


class EventoModelTest(TestCase):
    def setUp(self):
        self.user_organizador = User.objects.create_user(username='organizador', password='password')
        self.organizador = Organizador.objects.create(
            user=self.user_organizador,
            nome_organizador='Org Teste',
            telefone='123',
            genero='P',
            cidade='Cidade')

        self.image_content = b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x4c\x01\x00\x3b'

    def test_cria_evento_com_sucesso(self):
        evento = Evento.objects.create(
            organizador=self.organizador,
            titulo='Meu Evento',
            descricao='Descrição do evento',
            data=timezone.now(),
            local='Local Físico',
            capacidade_max=50,
            imagem_banner=SimpleUploadedFile(name='test_image.gif', content=self.image_content, content_type='image/gif')
        )
        self.assertEqual(evento.titulo, 'Meu Evento')
        self.assertEqual(str(evento), 'Meu Evento - Local Físico')

    def test_deleta_organizador_deleta_eventos(self):
        Evento.objects.create(
            organizador=self.organizador,
            titulo='Evento 1',
            data=timezone.now(),
            local='Casa da mãe Joana',
            capacidade_max=10,
            imagem_banner=SimpleUploadedFile(name='test_image1.jpg', content=self.image_content, content_type='image/jpeg'))

        Evento.objects.create(
            organizador=self.organizador,
            titulo='Evento 2',
            data=timezone.now(),
            local='B',
            capacidade_max=10,
            imagem_banner=SimpleUploadedFile(name='test_image2.jpg', content=self.image_content, content_type='image/jpeg'))

        self.assertEqual(Evento.objects.count(), 2)
        self.organizador.delete()
        self.assertEqual(Evento.objects.count(), 0)


class InscricaoModelTest(TestCase):
    def setUp(self):
        user_organizador = User.objects.create_user(username='organizador', password='password')
        organizador = Organizador.objects.create(
            user=user_organizador,
            nome_organizador='Org Teste',
            telefone='123',
            genero='P',
            cidade='Cidade Maravilhosa')

        image_content = b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x4c\x01\x00\x3b'

        self.evento = Evento.objects.create(
            organizador=organizador,
            titulo='Evento',
            data=timezone.now(),
            local='Local',
            capacidade_max=10,
            imagem_banner=SimpleUploadedFile(name='test_image.jpg', content=image_content, content_type='image/jpeg'))

        user_participante = User.objects.create_user(username='participante', password='password')
        self.participante = Participante.objects.create(
            user=user_participante,
            nome='Part',
            telefone='123',
            genero='P',
            cidade='Cidade', cpf='123')

    def test_cria_inscricao_com_sucesso(self):
        inscricao = Inscricao.objects.create(evento=self.evento, participante=self.participante)
        self.assertEqual(inscricao.evento, self.evento)
        self.assertEqual(inscricao.participante, self.participante)
        self.assertEqual(str(inscricao), f'{self.participante.nome} - {self.evento.titulo} - {self.evento.local}')


class BaseViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_participante = User.objects.create_user(username='participante', password='password')
        self.participante = Participante.objects.create(
            user=self.user_participante,
            nome='Participante Teste',
            telefone='123',
            genero='P',
            cidade='Cidade',
            cpf='123')

        self.user_organizador = User.objects.create_user(username='organizador', password='password')
        self.organizador = Organizador.objects.create(
            user=self.user_organizador,
            nome_organizador='Org Teste',
            telefone='123',
            genero='P',
            cidade='Cidade',
            cnpj='123')

        png_content = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82'

        test_image = SimpleUploadedFile(
            name='default.png',
            content=png_content,
            content_type='image/png'
        )

        self.evento = Evento.objects.create(
            organizador=self.organizador,
            titulo='Evento de Teste',
            descricao='Desc',
            data=timezone.now() + timezone.timedelta(days=1),
            local='Local',
            capacidade_max=10,
            imagem_banner=test_image
        )


class InscricaoCreateViewTest(BaseViewTest):
    def test_get_inscricao_view_nao_permitido(self):
        self.client.login(username='participante', password='password')
        response = self.client.get(reverse('inscrever', args=[self.evento.id]))
        self.assertEqual(response.status_code, 405)  # GET não é permitido

    @patch('app.views.enviar_email_confirmacao')
    def test_inscricao_sucesso_com_participante(self, mock_email):
        self.client.login(username='participante', password='password')
        response = self.client.post(reverse('inscrever', args=[self.evento.id]))

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Inscricao.objects.filter(participante=self.participante, evento=self.evento).exists())
        mock_email.assert_called_once_with(self.participante, self.evento)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), f'Sua inscrição para o evento "{self.evento.titulo}" foi confirmada!')

    @patch('app.views.enviar_email_confirmacao')
    def test_inscricao_organizador_nao_pode_se_inscrever(self, mock_email):
        self.client.login(username='organizador', password='password')
        response = self.client.post(reverse('inscrever', args=[self.evento.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Inscricao.objects.exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Apenas usuários com perfil de participante podem fazer isso.')

    def test_inscricao_participante_nao_logado_redireciona_login(self):
        self.client.logout()
        response = self.client.post(reverse('inscrever', args=[self.evento.id]))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_inscricao_duplicada_mostra_erro(self):
        Inscricao.objects.create(participante=self.participante, evento=self.evento)
        self.client.login(username='participante', password='password')
        response = self.client.post(reverse('inscrever', args=[self.evento.id]))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Inscricao.objects.count(), 1)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Você já está inscrito(a) neste evento.')

    def test_inscricao_capacidade_maxima_atingida(self):
        self.evento.capacidade_max = 0
        self.evento.save()
        self.client.login(username='participante', password='password')
        response = self.client.post(reverse('inscrever', args=[self.evento.id]))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Inscricao.objects.count(), 0)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Desculpe, a capacidade máxima para este evento já foi atingida.')


class EventoListViewTest(BaseViewTest):
    def setUp(self):
        super().setUp()

        self.valid_image_file = SimpleUploadedFile(
            name='valid_image.png',
            content=b'GIF89a\x01\x00\x01\x00\x00\xff\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;',
            content_type='image/png'
        )

    def test_evento_list_mostra_eventos(self):
        response = self.client.get(reverse('evento-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.evento.titulo)

    def test_evento_list_filtro_titulo(self):
        evento2 = Evento.objects.create(
            organizador=self.organizador,
            titulo='Evento Diferente',
            descricao='Outra desc',
            data=timezone.now() + timezone.timedelta(days=2),
            local='Local 2',
            capacidade_max=20,
            imagem_banner=self.valid_image_file
        )

        response = self.client.get(reverse('evento-list'), {'q': 'Diferente'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Evento Diferente')
        self.assertNotContains(response, self.evento.titulo)

    def test_evento_list_filtro_data_inicio(self):
        evento_futuro = Evento.objects.create(
            organizador=self.organizador,
            titulo='Evento Futuro',
            data=timezone.now() + timezone.timedelta(days=30),
            local='Local Futuro',
            capacidade_max=50,
            imagem_banner=self.valid_image_file
        )
        data_inicio = (timezone.now() + timezone.timedelta(days=29)).strftime('%Y-%m-%d')
        response = self.client.get(reverse('evento-list'), {'data_inicio': data_inicio})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, evento_futuro.titulo)
        self.assertNotContains(response, self.evento.titulo)

    def test_evento_list_filtro_data_fim(self):
        evento_passado = Evento.objects.create(
            organizador=self.organizador,
            titulo='Evento Passado',
            data=timezone.now() - timezone.timedelta(days=30),
            local='Local Passado',
            capacidade_max=50,
            imagem_banner=self.valid_image_file
        )
        data_fim = (timezone.now() - timezone.timedelta(days=29)).strftime('%Y-%m-%d')
        response = self.client.get(reverse('evento-list'), {'data_fim': data_fim})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, evento_passado.titulo)
        self.assertNotContains(response, self.evento.titulo)

    def test_evento_list_filtro_data_invalida(self):
        data_inicio = (timezone.now() + timezone.timedelta(days=5)).strftime('%Y-%m-%d')
        data_fim = (timezone.now() + timezone.timedelta(days=1)).strftime('%Y-%m-%d')
        response = self.client.get(reverse('evento-list'), {'data_inicio': data_inicio, 'data_fim': data_fim})
        self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'A data de início não pode ser maior que a data de fim.')

    def test_evento_list_participante_ve_inscricao(self):
        self.client.login(username='participante', password='password')
        Inscricao.objects.create(participante=self.participante, evento=self.evento)
        response = self.client.get(reverse('evento-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['eventos'][0].is_inscrito)
        self.assertIsNotNone(response.context['eventos'][0].inscricao_id)

    def test_evento_list_calcula_vagas_restantes(self):
        Inscricao.objects.create(participante=self.participante, evento=self.evento)
        response = self.client.get(reverse('evento-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['eventos'][0].vagas_restantes, self.evento.capacidade_max - 1)

    def test_evento_list_organizador_nao_ve_inscricao(self):
        self.client.login(username='organizador', password='password')
        response = self.client.get(reverse('evento-list'))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(hasattr(response.context['eventos'][0], 'is_inscrito'))

    def test_evento_list_usuario_nao_logado(self):
        self.client.logout()
        response = self.client.get(reverse('evento-list'))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['is_organizador'])
        self.assertFalse(response.context['is_participante'])

    def test_evento_list_participante_sem_inscricao(self):
        self.client.login(username='participante', password='password')
        response = self.client.get(reverse('evento-list'))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['eventos'][0].is_inscrito)
        self.assertIsNone(response.context['eventos'][0].inscricao_id)


class EventoCreateViewTest(BaseViewTest):
    def test_evento_create_view_organizador_success(self):
        self.client.login(username='organizador', password='password')

        gif_content = b'GIF89a\x01\x00\x01\x00\x00\xff\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;'

        form_data = {
            'titulo': 'Novo Evento',
            'descricao': 'Descricao de teste',
            'data': timezone.now() + timezone.timedelta(days=1),
            'local': 'Local do evento',
            'capacidade_max': 20,
            'imagem_banner': SimpleUploadedFile('imagem.gif', gif_content, content_type='image/gif')
        }

        response = self.client.post(reverse('evento-create'), form_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Evento.objects.filter(titulo='Novo Evento').exists())

    def test_evento_create_view_participante_fail(self):
        self.client.login(username='participante', password='password')
        response = self.client.get(reverse('evento-create'))
        self.assertEqual(response.status_code, 302)


class EventoUpdateViewTest(BaseViewTest):
    def test_evento_update_view_organizador_success(self):
        self.client.login(username='organizador', password='password')

        gif_content = b'GIF89a\x01\x00\x01\x00\x00\xff\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;'

        form_data = {
            'titulo': 'Evento Atualizado',
            'descricao': 'Descricao atualizada',
            'data': self.evento.data,
            'local': self.evento.local,
            'capacidade_max': self.evento.capacidade_max,
            'imagem_banner': SimpleUploadedFile('imagem.gif', gif_content, content_type='image/gif') # CORRIGIDO AQUI
        }
        response = self.client.post(reverse('evento-update', args=[self.evento.id]), form_data)
        self.assertEqual(response.status_code, 302)
        self.evento.refresh_from_db()
        self.assertEqual(self.evento.titulo, 'Evento Atualizado')

    def test_evento_update_view_outro_organizador_fail(self):
        user_organizador2 = User.objects.create_user(username='organizador2', password='password')
        Organizador.objects.create(user=user_organizador2, nome_organizador='Org2', telefone='456', genero='P',
                                   cidade='Outra Cidade', cnpj='456')
        self.client.login(username='organizador2', password='password')
        response = self.client.get(reverse('evento-update', args=[self.evento.id]))
        self.assertEqual(response.status_code, 302)


class EventoDeleteViewTest(BaseViewTest):
    def test_evento_delete_view_organizador_success(self):
        self.client.login(username='organizador', password='password')
        response = self.client.post(reverse('evento-delete', args=[self.evento.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Evento.objects.filter(id=self.evento.id).exists())


class InscricaoDeleteViewTest(BaseViewTest):
    def test_inscricao_delete_view_success(self):
        self.client.login(username='participante', password='password')
        inscricao = Inscricao.objects.create(participante=self.participante, evento=self.evento)
        response = self.client.post(reverse('desinscrever', args=[inscricao.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Inscricao.objects.filter(id=inscricao.id).exists())

