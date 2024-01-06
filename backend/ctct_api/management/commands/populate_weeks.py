# CTCTLab/ctct_api/management/commands/populate_weeks.py
from django.core.management.base import BaseCommand
from questions.models import Week

class Command(BaseCommand):
    help = 'Populates the database with weeks'

    def handle(self, *args, **options):
        weeks_data = [
            {
                'week_number': 1,
                'start_date': '2024-01-22', # monday
                'end_date': '2024-01-28', # sunday 
                'description': 'Semana cujo foco consiste em vários aspetos do PLANEAMENTO DE CARREIRA PARA A EMPREGABILIDADE, nomeadamente: o curriculum vitae, sua importância e apresentação; a carta de motivação; a entrevista e a imagem; as redes sociais e o emprego; planeamento curricular - aspetos a considerar para melhorar o CV; o teste psicotécnico no processo de seleção e recrutamento.'
            },
            {
                'week_number': 2,
                'start_date': '2024-01-29', # monday
                'end_date': '2024-02-04', # sunday
                'description': 'Nesta semana, o foco é a GESTÃO DO TEMPO, TRABALHO EM EQUIPA E LIDERANÇA. Quanto à gestão de tempo são abordados temas como a importância do planeamento diário, objetivos SMART, o modelo de Stephen-Covey par distinguir tarefas importantes de urgentes, desperdiçadores de tempo, eficiência versus eficácia, adiamentos sistemáticos, adiamentos vs. Perfecionismo e a gestão de e-mails e redes sociais. Quanto ao trabalho em equipa são abordados temas como o trabalho colaborativo e ferramentas de edição de textos, fatores de coesão e de perturbação da equipa e escuta ativa. Quanto a questões de liderança esta disciplina irá abordar o líder e a gestão de tarefas, a gestão individual e a gestão do grupo, estilos e valor da liderança, caraterísticas de um líder e linguagem positiva.'
            },
            {
                'week_number': 3,
                'start_date': '2024-02-05', # monday
                'end_date': '2024-02-11', # sunday
                'description': 'Nesta semana, o foco é a GESTÃO DE INFORMAÇÃO E COMUNICAÇÃO, sendo abordados os seguintes temas: conceitos básicos de gestão da informação; organização e classificação de informação; gestão de documentos físicos e eletrónicos; arquivo e recuperação de informação; comunicação interpessoal e organizacional; comunicação verbal e não verbal; barreiras à comunicação e formas de as superar; técnicas de apresentação e de falar em público.'
            },
            {
                'week_number': 4,
                'start_date': '2024-02-12', # monday (13 is holiday)
                'end_date': '2024-02-18', # sunday
                'description': 'Nesta semana, o foco passa pela UTILIZAÇÃO AVANÇADA DE FOLHAS DE CÁLCULO. O uso avançado de fórmulas e funções, a formatação condicional, a criação de tabelas dinâmicas, a importação e exportação de dados, o trabalhar com várias folhas e livros, o uso de gráficos e elementos gráficos, a automatização de tarefas com macros e a segurança e partilha de dados são abordados nesta semana.'
            },
            {
                'week_number': 5,
                'start_date': '2024-02-19', # monday
                'end_date': '2024-02-25', # sunday
                'description': 'No planeamento da Época Intercalar estão definidas 5 semanas...'
            },
        ]

        for week_data in weeks_data:
            Week.objects.create(
                week_number=week_data['week_number'], 
                start_date=week_data['start_date'], 
                end_date=week_data['end_date'], 
                description=week_data['description'])

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with weeks'))
