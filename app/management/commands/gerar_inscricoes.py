from django.contrib.auth.models import User
from django.core.management import BaseCommand
from app.models import Evento, Participante, Inscricao
from faker import Faker

class Command(BaseCommand):
    help = 'Gera participantes e inscrições falsas para eventos'

    def handle(self, *args, **kwargs):
        fake = Faker('pt_BR')

        NUM_EVENTOS = 9
        PARTICIPANTES_POR_EVENTO = 5
        TOTAL_PARTICIPANTES = NUM_EVENTOS * PARTICIPANTES_POR_EVENTO

        generos = ['Masculino', 'Feminino', 'Outro']
        eventos = Evento.objects.all()[:NUM_EVENTOS]

        if len(eventos) < NUM_EVENTOS:
            print("⚠️ Não há eventos suficientes no banco de dados.")
        else:
            participantes = []

            for i in range(TOTAL_PARTICIPANTES):
                user = User.objects.create_user(
                    username=fake.unique.user_name(),
                    email=fake.unique.email(),
                    password='senha123'
                )

                participante = Participante.objects.create(
                    user=user,
                    nome=fake.name(),
                    telefone=fake.phone_number(),
                    genero=fake.random_element(generos),
                    cidade=fake.city(),
                    cpf=fake.cpf()
                )

                participantes.append(participante)

            # Criar inscrições: 5 participantes por evento
            inscricoes = []
            for i, evento in enumerate(eventos):
                grupo = participantes[i * PARTICIPANTES_POR_EVENTO: (i + 1) * PARTICIPANTES_POR_EVENTO]
                for participante in grupo:
                    inscricoes.append(Inscricao(evento=evento, participante=participante))

            Inscricao.objects.bulk_create(inscricoes)

            print(
                f"✅ Criados {TOTAL_PARTICIPANTES} participantes e {len(inscricoes)} inscrições para {NUM_EVENTOS} eventos.")