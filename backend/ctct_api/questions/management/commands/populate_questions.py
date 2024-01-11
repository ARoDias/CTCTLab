# ctct_api/management/commands/populate_questions.py
from django.core.management.base import BaseCommand
from questions.models import Question, Questionnaire, Option, QuestionnaireQuestion

class Command(BaseCommand):
    help = 'Populates the database with questions and questionnaires for TP3 - Quiz on ethics and plagiarism'

    def create_question(self, text):
        question = Question(question_text=text, question_type='MCQ')
        question.save()
        return question

    def create_option(self, question, text, is_correct=False):
        option = Option(question=question, option_text=text, is_correct=is_correct)
        option.save()

    def create_questionnaire(self, title, description, questions):
        questionnaire = Questionnaire(title=title, description=description)
        questionnaire.save()
        for order, question in enumerate(questions, start=1):
            QuestionnaireQuestion.objects.create(questionnaire=questionnaire, question=question, order=order)

    def handle(self, *args, **options):
        quiz_data = [
            {
                "text": "Qual é a definição correta de plágio académico?",
                "options": [
                    {"text": "a) Utilização de fontes externas de forma ética e transparente", "is_correct": False},
                    {"text": "b) Copiar e colar trechos de textos sem dar créditos ao autor original", "is_correct": True},
                    {"text": "c) Paráfrase adequada de ideias sem referenciar a fonte", "is_correct": False},
                    {"text": "d) Colaboração entre estudantes em projetos académicos", "is_correct": False},
                    {"text": "e) Utilização de citações diretas sem indicar a fonte", "is_correct": False}
                ]
            },
            {
                "text": "O que caracteriza um comportamento ético em trabalhos académicos?",
                "options": [
                    {"text": "a) Ignorar as normas estabelecidas pela instituição", "is_correct": False},
                    {"text": "b) Submeter trabalhos de outros estudantes como próprios", "is_correct": False},
                    {"text": "c) Fazer referências adequadas a todas as fontes utilizadas", "is_correct": True},
                    {"text": "d) Utilizar materiais online sem citar a fonte", "is_correct": False},
                    {"text": "e) Compartilhar ideias sem atribuir créditos aos colegas", "is_correct": False}
                ]
            },
            {
                "text": "Qual é a importância de seguir as diretrizes éticas na investigação académica?",
                "options": [
                    {"text": "a) Não é relevante, desde que o trabalho seja bem feito", "is_correct": False},
                    {"text": "b) Garante a integridade e credibilidade do trabalho académico", "is_correct": True},
                    {"text": "c) Pode ser ignorada se o resultado final for positivo", "is_correct": False},
                    {"text": "d) Facilita a obtenção de notas mais altas", "is_correct": False},
                    {"text": "e) Contribui para a competitividade entre estudantes", "is_correct": False}
                ]
            },
            {
                "text": "Como evitar o plágio em trabalhos académicos?",
                "options": [
                    {"text": "a) Não citar fontes para tornar o trabalho mais original", "is_correct": False},
                    {"text": "b) Utilizar o 'ctrl+c' e 'ctrl+v' para agilizar o processo de escrita", "is_correct": False},
                    {"text": "c) Parafrapear trechos de textos sem indicar a fonte original", "is_correct": False},
                    {"text": "d) Fazer citações diretas e indicar as fontes de maneira apropriada", "is_correct": True},
                    {"text": "e) Colaborar com outros estudantes para compartilhar ideias", "is_correct": False}
                ]
            },
            {
                "text": "O que acontece quando um estudante é apanhado cometendo plágio?",
                "options": [
                    {"text": "a) Não há consequências, pois é comum na vida acadêmica", "is_correct": False},
                    {"text": "b) Recebe elogios por conseguir informações relevantes", "is_correct": False},
                    {"text": "c) Pode ser penalizado, resultando em notas baixas ou até mesmo expulsão", "is_correct": True},
                    {"text": "d) É promovido a cargos de destaque na instituição", "is_correct": False},
                    {"text": "e) A instituição incentiva o plágio como método de aprendizagem", "is_correct": False}
                ]
            }
        ]

        created_questions = []
        for q_data in quiz_data:
            question = self.create_question(q_data["text"])
            for option in q_data["options"]:
                self.create_option(question, option["text"], option["is_correct"])
            created_questions.append(question)

        self.create_questionnaire("TP3 - Quiz sobre ética e plágio", "Um quiz focado em questões de ética e plágio no contexto académico.", created_questions)
        self.stdout.write(self.style.SUCCESS('Successfully populated the database with questions and questionnaire'))
