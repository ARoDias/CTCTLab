# Script to populate the database with questions and questionnaires for TP3 - Quiz on ethics and plagiarism
# Este ficheiro so funciona na root do projeto de backend
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ctct_api.settings')
django.setup()

from questions.models import Question, Questionnaire

def create_question(text, options):
    """
    Create a new question object.
    """
    question = Question(question_text=text, question_type='MCQ', options=options)
    question.save()
    return question

def create_questionnaire(title, description, questions):
    """
    Create a new questionnaire object and associate questions to it.
    """
    questionnaire = Questionnaire(title=title, description=description)
    questionnaire.save()
    questionnaire.questions.set(questions)
    questionnaire.save()

# Questions for the Quiz
quiz_questions = [
    {
        "text": "Qual é a definição correta de plágio académico?",
        "options": "a) Utilização de fontes externas de forma ética e transparente; b) Copiar e colar trechos de textos sem dar créditos ao autor original; c) Paráfrase adequada de ideias sem referenciar a fonte; d) Colaboração entre estudantes em projetos académicos; e) Utilização de citações diretas sem indicar a fonte."
    },
    # Add other questions here following the same structure
]

# Create questions and store them in a list
created_questions = [create_question(q["text"], q["options"]) for q in quiz_questions]

# Create the questionnaire
quiz_title = "TP3 - Quiz sobre ética e plágio"
quiz_description = "Um quiz focado em questões de ética e plágio no contexto académico."
create_questionnaire(quiz_title, quiz_description, created_questions)

print("Database populated with questions and questionnaire successfully.")
